"""
Sample Resume Generator
Creates a test resume PDF for the Smart Career Counselor project
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

def create_sample_resume():
    """Create a sample resume PDF for testing"""
    
    # Create output directory if it doesn't exist
    os.makedirs('sample_resumes', exist_ok=True)
    
    filename = 'sample_resumes/john_doe_resume.pdf'
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Add name and title
    elements.append(Paragraph("JOHN DOE", title_style))
    elements.append(Paragraph("Full Stack Developer", styles['Normal']))
    elements.append(Paragraph("john.doe@email.com | +1-555-0123 | LinkedIn: johndoe", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Professional Summary
    elements.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    summary = """
    Experienced Full Stack Developer with 3 years of experience in designing and developing 
    web applications. Proficient in React, Node.js, Python, and MongoDB. Strong background 
    in Machine Learning and AI integration. Passionate about creating efficient, scalable, 
    and user-friendly applications.
    """
    elements.append(Paragraph(summary, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Skills
    elements.append(Paragraph("TECHNICAL SKILLS", heading_style))
    skills_text = """
    <b>Programming Languages:</b> JavaScript, Python, Java, TypeScript, SQL<br/>
    <b>Web Technologies:</b> React, Node.js, Express, HTML, CSS, REST API, GraphQL<br/>
    <b>Databases:</b> MongoDB, PostgreSQL, MySQL, Redis<br/>
    <b>Cloud & DevOps:</b> AWS, Docker, Kubernetes, Git, CI/CD, Jenkins<br/>
    <b>Machine Learning:</b> TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy<br/>
    <b>Tools & Others:</b> Figma, Agile, Scrum, JIRA, Testing
    """
    elements.append(Paragraph(skills_text, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Experience
    elements.append(Paragraph("WORK EXPERIENCE", heading_style))
    
    elements.append(Paragraph("<b>Senior Full Stack Developer</b> - Tech Innovations Inc.", styles['Normal']))
    elements.append(Paragraph("January 2022 - Present (3 years)", styles['Normal']))
    exp1 = """
    • Developed and maintained full-stack web applications using React and Node.js<br/>
    • Implemented machine learning models for predictive analytics using Python and TensorFlow<br/>
    • Collaborated with cross-functional teams in Agile environment<br/>
    • Optimized database queries resulting in 40% performance improvement<br/>
    • Deployed applications on AWS using Docker and Kubernetes
    """
    elements.append(Paragraph(exp1, styles['Normal']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Junior Developer</b> - StartUp Solutions", styles['Normal']))
    elements.append(Paragraph("June 2020 - December 2021 (1.5 years)", styles['Normal']))
    exp2 = """
    • Built responsive web interfaces using HTML, CSS, and JavaScript<br/>
    • Integrated REST APIs and managed MongoDB databases<br/>
    • Participated in code reviews and testing processes<br/>
    • Learned and applied best practices in software development
    """
    elements.append(Paragraph(exp2, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Education
    elements.append(Paragraph("EDUCATION", heading_style))
    elements.append(Paragraph("<b>Bachelor of Science in Computer Science</b>", styles['Normal']))
    elements.append(Paragraph("University of Technology - Graduated 2020", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Projects
    elements.append(Paragraph("PROJECTS", heading_style))
    projects = """
    <b>E-Commerce Platform:</b> Built a full-stack e-commerce site with React, Node.js, and MongoDB. 
    Implemented payment gateway integration and real-time inventory management.<br/><br/>
    <b>AI Chatbot:</b> Developed an AI-powered customer service chatbot using Python, NLP, and 
    machine learning. Integrated with company website using REST API.<br/><br/>
    <b>Task Management App:</b> Created a collaborative task management application with real-time 
    updates using React, Firebase, and Material-UI.
    """
    elements.append(Paragraph(projects, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Certifications
    elements.append(Paragraph("CERTIFICATIONS", heading_style))
    certs = """
    • AWS Certified Developer - Associate<br/>
    • Machine Learning Specialization - Coursera<br/>
    • Full Stack Web Development - Udemy
    """
    elements.append(Paragraph(certs, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    print(f"Sample resume created: {filename}")
    return filename

if __name__ == "__main__":
    try:
        create_sample_resume()
        print("\n✅ Sample resume generated successfully!")
        print("📁 Location: sample_resumes/john_doe_resume.pdf")
        print("💡 You can use this resume to test the application!")
    except ImportError:
        print("\n⚠️  reportlab is not installed.")
        print("To generate sample PDF, run: pip install reportlab")
        print("However, this is optional - you can use any PDF resume for testing!")
