# matcher/resume_model.py
import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

# Load and preprocess job dataset
df = pd.read_csv('matcher/kaggle_sample.csv', encoding='latin1')

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

df['combined'] = df['Role'].astype(str) + " " + df['Description'].astype(str) + " " + df['Skills'].astype(str)
df['combined'] = df['combined'].apply(clean_text)

model = SentenceTransformer('all-MiniLM-L6-v2')
job_vectors = model.encode(df['combined'].tolist(), show_progress_bar=False)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + " "
    return text

def get_top_matches(resume_path):
    if resume_path.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_path)
    else:
        with open(resume_path, 'r', encoding='utf-8') as f:
            resume_text = f.read()

    resume_text_cleaned = clean_text(resume_text)
    resume_vector = model.encode([resume_text_cleaned])[0]
    similarity_scores = cosine_similarity([resume_vector], job_vectors)[0]
    normalized_scores = (similarity_scores - similarity_scores.min()) / (similarity_scores.max() - similarity_scores.min()) * 100
    normalized_scores = normalized_scores.round(2)

    results = pd.DataFrame({
        'Role': df['Role'],
        'Score (%)': (similarity_scores * 100).round(2)
    })

    results = results.drop_duplicates(subset='Role')

    def label_category(score):
        if score >= 80:
            return "Category 1"
        elif score >= 60:
            return "Category 2"
        elif score >= 40:
            return "Category 3"
        else:
            return "Category 4"

    results['Category'] = results['Score (%)'].apply(label_category)
    results = results.sort_values(by='Score (%)', ascending=False).reset_index(drop=True)

    return results.head(5)
