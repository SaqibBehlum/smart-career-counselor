from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from PIL import Image
import pytesseract
from docx import Document
import requests
from openai import OpenAI

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

with open('data/jobs_dataset.json', 'r') as f:
    JOBS_DATA = json.load(f)

with open('data/skills_dataset.json', 'r') as f:
    SKILLS_DATA = json.load(f)

# ========================================



# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'docx', 'doc', 'txt'}



# GROQ API - FREE & FAST (Meta Llama)

GROQ_API_KEY = "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"

# Initialize Groq client
groq_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def query_groq_llama(prompt, max_tokens=300):
    """Query Groq API - FREE Meta Llama"""
    try:
        print(f"Calling Groq Llama...")
        
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Fast & Free
            messages=[
                {"role": "system", "content": "You are a professional career counselor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content
        print(f"Groq response: {bot_response[:100]}...")
        return bot_response
        
    except Exception as e:
        print(f"Groq error: {e}")
        return f"Error: {str(e)}"
def extract_text_from_pdf(filepath):
    """Extract text from PDF"""
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""

def extract_text_from_image(filepath):
    """Extract text from image using Tesseract OCR"""
    try:
        print(f"Reading image with OCR: {filepath}")
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        print(f"Extracted text: {text[:100]}...")
        return text
    except Exception as e:
        print(f"Image OCR error: {e}")
        print("Note: Make sure Tesseract is installed. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        return ""

def extract_text_from_docx(filepath):
    """Extract text from DOCX"""
    try:
        doc = Document(filepath)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return ""

def extract_text_from_txt(filepath):
    """Extract text from TXT"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"TXT extraction error: {e}")
        return ""

def extract_text_from_file(filepath, filename):
    """Smart text extraction based on file type"""
    ext = filename.rsplit('.', 1)[1].lower()
    
    print(f"Extracting text from {ext} file: {filename}")
    
    if ext == 'pdf':
        return extract_text_from_pdf(filepath)
    elif ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
        return extract_text_from_image(filepath)
    elif ext in ['docx', 'doc']:
        return extract_text_from_docx(filepath)
    elif ext == 'txt':
        return extract_text_from_txt(filepath)
    else:
        return ""

def extract_skills_from_text(text):
    """Extract skills from resume text"""
    text_lower = text.lower()
    found_skills = []
    
    for category, skills in SKILLS_DATA.items():
        for skill in skills:
            if skill.lower() in text_lower:
                found_skills.append({
                    'skill': skill,
                    'category': category
                })
    
    return found_skills

def extract_experience_years(text):
    """Extract years of experience from resume"""
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'experience[:\s]*(\d+)\+?\s*years?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    return 0

def recommend_jobs(user_skills, experience_years):
    """Recommend jobs based on skills using ML similarity"""
    if not user_skills:
        return []
    
    user_skill_names = [s['skill'] for s in user_skills]
    user_skill_text = ' '.join(user_skill_names)
    
    job_recommendations = []
    
    for job in JOBS_DATA:
        job_skills_text = ' '.join(job['required_skills'])
        
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform([user_skill_text, job_skills_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            matching_skills = set(user_skill_names) & set(job['required_skills'])
            match_percentage = (len(matching_skills) / len(job['required_skills'])) * 100
            
            exp_match = experience_years >= job.get('min_experience', 0)
            
            if similarity > 0.1 or match_percentage > 20:
                job_recommendations.append({
                    'title': job['title'],
                    'company': job['company'],
                    'salary': job['salary'],
                    'required_skills': job['required_skills'],
                    'match_percentage': round(match_percentage, 2),
                    'similarity_score': round(similarity * 100, 2),
                    'experience_match': exp_match,
                    'min_experience': job.get('min_experience', 0)
                })
        except:
            continue
    
    job_recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
    return job_recommendations[:10]

def identify_skill_gaps(user_skills, target_job):
    """Identify missing skills for a target job"""
    user_skill_names = [s['skill'].lower() for s in user_skills]
    
    for job in JOBS_DATA:
        if job['title'].lower() == target_job.lower():
            required_skills = [s.lower() for s in job['required_skills']]
            missing_skills = [s for s in required_skills if s.lower() not in user_skill_names]
            return {
                'has_skills': [s for s in required_skills if s.lower() in user_skill_names],
                'missing_skills': missing_skills,
                'job_details': job
            }
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume upload - SUPPORTS ALL FILE TYPES!"""
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"\n{'='*60}")
        print(f"Processing file: {filename}")
        print(f"{'='*60}")
        
        resume_text = extract_text_from_file(filepath, filename)
        
        if not resume_text:
            return jsonify({'error': 'Could not extract text from file'}), 400
        
        print(f"Extracted {len(resume_text)} characters")
        
        skills = extract_skills_from_text(resume_text)
        print(f"Found {len(skills)} skills")
        
        experience = extract_experience_years(resume_text)
        print(f"Experience: {experience} years")
        
        session['user_skills'] = skills
        session['experience_years'] = experience
        session['resume_text'] = resume_text
        
        recommendations = recommend_jobs(skills, experience)
        print(f"Generated {len(recommendations)} job recommendations")
        
        return jsonify({
            'success': True,
            'skills': skills,
            'experience': experience,
            'recommendations': recommendations,
            'file_type': filename.rsplit('.', 1)[1].lower()
        })
    
    return jsonify({'error': f'Invalid file format. Supported: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

@app.route('/skill-gap-analysis', methods=['POST'])
def skill_gap_analysis():
    """Analyze skill gaps for target job"""
    data = request.json
    target_job = data.get('target_job')
    
    user_skills = session.get('user_skills', [])
    
    if not user_skills:
        return jsonify({'error': 'Please upload resume first'}), 400
    
    gap_analysis = identify_skill_gaps(user_skills, target_job)
    
    if gap_analysis:
        return jsonify(gap_analysis)
    else:
        return jsonify({'error': 'Job not found'}), 404

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot - Uses Groq API (Meta Llama - FREE!)"""
    data = request.json
    message = data.get('message', '')
    
    try:
        user_skills = session.get('user_skills', [])
        experience = session.get('experience_years', 0)
        
        # Build prompt
        prompt = f"""User Profile:
- Skills: {', '.join([s['skill'] for s in user_skills[:10]]) if user_skills else 'Not provided'}
- Experience: {experience} years

User Question: {message}

Provide helpful career advice in 2-3 short paragraphs."""

        print(f"User asked: {message}")
        
        # Call Groq API
        bot_response = query_groq_llama(prompt, max_tokens=300)
        
        return jsonify({
            'response': bot_response,
            'timestamp': datetime.now().strftime('%H:%M')
        })
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/interview-prep', methods=['POST'])
def interview_prep():
    """Generate interview questions using Hugging Face"""
    data = request.json
    job_role = data.get('job_role', '')
    
    try:
        prompt = f"""Generate 5 interview questions for a {job_role} position.

Requirements:
- Mix technical and behavioral questions
- Number each question (1-5)
- Add a brief tip after each

Interview Questions for {job_role}:"""
        
        print(f"Generating interview questions for: {job_role}")
        
        questions = query_groq_llama(prompt, max_tokens=400)
        
        return jsonify({
            'questions': questions
        })
        
    except Exception as e:
        print(f"Interview prep error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-jobs')
def get_jobs():
    """Get all available jobs"""
    return jsonify(JOBS_DATA)

if __name__ == '__main__':
    app.run(debug=True)