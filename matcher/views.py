import os
import re
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import joblib

from django.shortcuts import render
from django.conf import settings
from .models import Resume, ResumeMatch

# ✅ Clean up raw text (removes URLs, emails, phone numbers, special characters, etc.)
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s\.\#\+]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ✅ Load and preprocess job descriptions dataset
job_csv_path = os.path.join(settings.BASE_DIR, 'matcher', 'kaggle_sample.csv')
df = pd.read_csv(job_csv_path, encoding='latin1')

# ✅ Combine job role, description, and skills into a single text
df['combined'] = df['Role'].astype(str) + ' ' + df['Description'].astype(str) + ' ' + df['Skills'].astype(str)
df['combined'] = df['combined'].apply(clean_text)

# ✅ Load or compute sentence embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
vector_path = os.path.join(settings.BASE_DIR, 'matcher', 'job_vectors.pkl')

if os.path.exists(vector_path):
    job_vectors = joblib.load(vector_path)
else:
    job_vectors = model.encode(df['combined'].tolist(), show_progress_bar=True)
    joblib.dump(job_vectors, vector_path)

# ✅ Extract text from a PDF resume
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + " "
    return text

# ✅ Assign category label based on score
def label_category(score):
    if score >= 80:
        return "Category 1"
    elif score >= 60:
        return "Category 2"
    elif score >= 40:
        return "Category 3"
    else:
        return "Category 4"

# ✅ Upload and process resume
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume_file'):
        uploaded_file = request.FILES['resume_file']
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()

        # ✅ Only allow PDF or TXT files
        if file_ext not in ['.pdf', '.txt']:
            return render(request, 'matcher/upload.html', {
                'error': "❌ Please upload a valid resume file (PDF or TXT only)."
            })

        # ✅ Save the uploaded file to media folder
        media_resume_dir = os.path.join(settings.MEDIA_ROOT, 'resumes')
        os.makedirs(media_resume_dir, exist_ok=True)
        saved_file_path = os.path.join(media_resume_dir, uploaded_file.name)
        
        with open(saved_file_path, 'wb+') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)

        # ✅ Extract text based on file type
        try:
            if file_ext == '.pdf':
                resume_text = extract_text_from_pdf(saved_file_path)
            else:
                with open(saved_file_path, 'r', encoding='utf-8') as f:
                    resume_text = f.read()
        except Exception as e:
            return render(request, 'matcher/upload.html', {
                'error': f"❌ Error reading file: {str(e)}"
            })

        # ✅ Clean, encode, and calculate similarity scores
        resume_cleaned = clean_text(resume_text)
        resume_vector = model.encode([resume_cleaned], convert_to_numpy=True)[0]
        similarity_scores = cosine_similarity([resume_vector], job_vectors)[0]

        # ✅ Create results DataFrame
        results_df = pd.DataFrame({
            'Role': df['Role'],
            'Score': similarity_scores
        }).drop_duplicates(subset='Role')

        results_df['Score'] = results_df['Score'].apply(lambda x: round(float(x * 100), 2))
        results_df['Category'] = results_df['Score'].apply(label_category)
        top_matches = results_df.sort_values(by='Score', ascending=False).head(5)
        results = top_matches.to_dict(orient='records')

        # ✅ Save Resume model entry
        resume_instance = Resume.objects.create(
            name=uploaded_file.name,
            file='resumes/' + uploaded_file.name
        )

        # ✅ Save top 5 matches in ResumeMatch table
        for match in results:
            ResumeMatch.objects.create(
                resume=resume_instance,
                role=match['Role'],
                score=match['Score'],
                category=match['Category']
            )

        return render(request, 'matcher/results.html', {
            'results': results,
            'filename': uploaded_file.name
        })

    return render(request, 'matcher/upload.html')

from django.shortcuts import render

def home(request):
    return render(request,'matcher/home.html')