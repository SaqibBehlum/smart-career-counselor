# Smart Career Counselor - AI/ML Capstone Project

## 🎯 Project Overview

Smart Career Counselor is a comprehensive AI-powered career guidance platform that combines Machine Learning and Chatbot technology to help users:
- Analyze resumes and extract skills using NLP
- Get personalized job recommendations using ML similarity algorithms
- Identify skill gaps for target jobs
- Chat with an AI career counselor (Groq)
- Prepare for interviews with AI-generated questions

## ✨ Key Features

### 1. **Resume Analysis (AI/ML)**
- PDF resume parsing and text extraction
- Automated skill extraction using NLP
- Experience years detection from resume text
- Skills categorization by domain

### 2. **Job Recommendation System (ML)**
- TF-IDF vectorization for skill matching
- Cosine similarity calculation between user skills and job requirements
- Match percentage computation
- Experience-based filtering

### 3. **Skill Gap Analysis**
- Compare user skills against target job requirements
- Visual representation of skills you have vs skills you need
- Personalized learning recommendations

### 4. **AI Career Counselor Chatbot**
- Integration with Anthropic Claude API
- Context-aware career advice
- Interview preparation tips
- Resume improvement suggestions
- Job search strategies

### 5. **Interview Preparation**
- AI-generated interview questions for specific roles
- Mix of technical and behavioral questions
- Answer tips and guidance

## 🛠️ Technologies Used

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Web framework
- **PyPDF2** - PDF text extraction
- **scikit-learn** - Machine Learning (TF-IDF, Cosine Similarity)
- **NumPy** - Numerical computations
- **Anthropic API** - AI chatbot integration

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern gradient designs
- **JavaScript (ES6+)** - Interactivity
- **Fetch API** - Asynchronous requests

### Machine Learning Components
- **TF-IDF Vectorizer** - Text feature extraction
- **Cosine Similarity** - Job matching algorithm
- **NLP** - Skill extraction from resume text

## 📁 Project Structure

```
smart-career-counselor/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── data/
│   ├── jobs_dataset.json      # Job listings database (20 jobs)
│   └── skills_dataset.json    # Skills categorized by domain
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── script.js          # Frontend JavaScript
│   └── uploads/               # Uploaded resume storage
├── templates/
│   └── index.html             # Main HTML template
└── models/                     # (Optional) For saved ML models
```

## 🚀 Installation & Setup

### Step 1: Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Groq API key (https://console.groq.com/keys)

### Step 2: Install Dependencies

Open terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

If you encounter any issues, install packages individually:

```bash
pip install Flask==3.0.0
pip install anthropic==0.41.0
pip install PyPDF2==3.0.1
pip install scikit-learn==1.5.2
pip install numpy==2.1.3
```

### Step 3: Get Your Groq API Key

1. Go to  https://console.groq.com/keys
2. Sign up or log in
3. Create a new API key
4. Copy the key (Start)

### Step 4: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 5: Use the Application

1. Open your browser and go to `http://localhost:5000`
2. Enter your Claude API key when prompted (it will be saved locally)
3. Upload your resume (PDF format)
4. Explore features!

## 💡 How to Use

### 1. Upload Resume
- Click the upload area or drag-and-drop your PDF resume
- Wait for AI to analyze your skills and experience
- View extracted skills and job recommendations

### 2. View Job Recommendations
- Automatically generated after resume upload
- Shows match percentage for each job
- Color-coded match indicators (Green: 70%+, Yellow: 50-69%, Red: <50%)

### 3. Skill Gap Analysis
- Enter a target job title (e.g., "Data Scientist")
- Click "Analyze" to see:
  - Skills you already have ✅
  - Skills you need to learn ❌
  - Personalized recommendations

### 4. Chat with AI Counselor
- Ask career-related questions
- Get interview tips
- Request resume improvement advice
- Discuss career paths and strategies

### 5. Interview Preparation
- Enter the job role you're preparing for
- Get 5 relevant interview questions
- Includes technical and behavioral questions
- Tips for answering each question

## 🧠 ML/AI Components Explained

### 1. Skill Extraction (NLP)
```python
# Uses pattern matching and keyword detection
# Compares resume text against skills database
# Returns categorized skills with confidence
```

### 2. Job Matching Algorithm
```python
# TF-IDF Vectorization: Converts skills to numerical vectors
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([user_skills, job_skills])

# Cosine Similarity: Calculates similarity score (0-1)
similarity = cosine_similarity(user_vector, job_vector)

# Match Percentage: Based on overlapping skills
match_percentage = (matching_skills / total_required) * 100
```

### 3. Chatbot Integration
```python
# Uses Groq API
# Sends context about user profile
# Receives intelligent career advice
client.messages.create(
    model="llama-3.1-8b-instant"
    messages=[{"role": "user", "content": query}]
)
```

## 📊 Sample Datasets

### Jobs Dataset (20 roles)
- Full Stack Developer
- Data Scientist
- Machine Learning Engineer
- DevOps Engineer
- Cloud Architect
- And 15 more...

### Skills Dataset (200+ skills across 14 categories)
- Programming Languages
- Web Development
- Data Science & ML
- Cloud & DevOps
- Design
- And more...

## 🎨 Features Showcase

1. **Modern UI/UX**
   - Gradient color schemes
   - Smooth animations
   - Responsive design
   - Interactive elements

2. **Real-time Analysis**
   - Instant resume processing
   - Live job matching
   - Dynamic skill visualization

3. **AI-Powered Insights**
   - Contextual career advice
   - Personalized recommendations
   - Interview question generation

## 🔧 Customization

### Add More Jobs
Edit `data/jobs_dataset.json`:
```json
{
  "title": "Your Job Title",
  "company": "Company Name",
  "salary": "$X - $Y",
  "required_skills": ["Skill1", "Skill2", ...],
  "min_experience": 2
}
```

### Add More Skills
Edit `data/skills_dataset.json`:
```json
{
  "Category Name": ["Skill1", "Skill2", "Skill3"]
}
```

### Customize Styling
Edit `static/css/style.css` to change:
- Colors (CSS variables at top)
- Fonts
- Layout
- Animations

## 📝 API Endpoints

- `POST /upload-resume` - Upload and analyze resume
- `POST /skill-gap-analysis` - Analyze skill gaps
- `POST /chat` - Send message to AI chatbot
- `POST /interview-prep` - Generate interview questions
- `GET /get-jobs` - Retrieve all jobs

## 🐛 Troubleshooting

### Issue: API Key Not Working
- Ensure you have a valid Groq API key
- Check if you have API credits
- Verify the key is correctly copied

### Issue: Resume Upload Fails
- Make sure file is in PDF format
- Check file size (max 16MB)
- Ensure PDF is not encrypted

### Issue: No Skills Extracted
- Resume might not contain recognizable skills
- Try a different resume format
- Check if skills are in the skills database

### Issue: Dependencies Installation Error
- Update pip: `pip install --upgrade pip`
- Use Python 3.8+
- Install packages one by one

## 🎓 Learning Outcomes

This project demonstrates:
1. **Backend Development** - Flask, REST APIs, file handling
2. **Machine Learning** - TF-IDF, cosine similarity, NLP
3. **AI Integration** - Working with external AI APIs
4. **Frontend Development** - Modern HTML/CSS/JS
5. **Full-Stack Development** - Connecting frontend and backend
6. **Data Processing** - PDF parsing, text extraction
7. **Algorithm Implementation** - Recommendation systems

## 🚀 Future Enhancements

- [ ] User authentication and profiles
- [ ] Resume template generation
- [ ] Job application tracking
- [ ] Salary prediction using ML
- [ ] Network graph of skills
- [ ] Email notifications for matching jobs
- [ ] Cover letter generation
- [ ] LinkedIn profile optimizer
- [ ] Mock interview simulator

## 📄 License

This is a capstone project for educational purposes.

## 👨‍💻 Author

Created as an AI/ML Capstone Project demonstrating:
- Machine Learning algorithms
- Natural Language Processing
- AI chatbot integration
- Full-stack web development

## 🙏 Acknowledgments

- Groq API
- Flask framework
- scikit-learn library
- All open-source contributors

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with sample resumes
4. Verify API key is valid

**Happy Career Counseling! 🎯**
