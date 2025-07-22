# 🚀 Resume Score Matcher using Django, ML & NLP
An AI-powered Resume Matcher that compares uploaded resumes against a dataset of job descriptions and roles. Built using Django, NLP (Sentence Transformers), and Machine Learning, this web app provides users with similarity scores and categorized job match scores.

## 🔑 Features
- Upload resumes in PDF or TXT format
- NLP-based resume cleaning and vectorization
- Cosine similarity scoring using Sentence Transformers (`all-MiniLM-L6-v2`)
- Top 5 job role matches with percentage scores
- Admin panel for viewing and managing uploaded resumes
- Role-based access for secure admin dashboard
- Responsive neon-themed frontend design

## 🛠 Tech Stack
- Django 5.2 (Web Framework)
- Python 3.11+
- Sentence Transformers
- Pandas, scikit-learn, NumPy
- PyPDF2
- HTML/CSS (Custom Neon UI)

## 🚀 Getting Started

1. Clone the repo  
   git clone https://github.com/haritha23-dee/resume-matcher.git
   cd resume-matcher

2.Create virtual environment
  python -m venv venv
  venv\Scripts\activate   # For Windows

3.Install Dependencies
  pip install -r requirements.txt

4.Run Migrations
  python manage.py migrate

5.Start development server
  python manage.py runserver

## 📁 Project Structure

resume_scoring_project/
├── matcher/                  # Django app
│   ├── templates/            # HTML templates
│   ├── static/               # Optional static files
│   ├── models.py             # Resume & Matching Models
│   ├── views.py              # Main Logic
│   └── urls.py               # App URL Routing
├── media/                    # Uploaded resumes
├── db.sqlite3                # SQLite DB
├── requirements.txt          # Project dependencies
└── manage.py                 # Django entry point

## 🔮 Future Enhancements

- Deploy on Render/Netlify/Heroku (free hosting)
- Add user authentication (login/logout)
- Allow job description uploads by HR
- Add resume parser using spaCy or docx2txt
- Switch from cosine similarity to deep semantic scoring (BERT fine-tuning)

## 🙏 Acknowledgements

- [Django Documentation](https://docs.djangoproject.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Scikit-learn](https://scikit-learn.org/)

