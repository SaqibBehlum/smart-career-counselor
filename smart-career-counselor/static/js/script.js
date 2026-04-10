// Removed API_KEY variable since it's hardcoded in backend

// Setup on page load
window.onload = () => {
    setupEventListeners();
};

function setupEventListeners() {
    // Upload area click
    const uploadArea = document.getElementById('uploadArea');
    const resumeInput = document.getElementById('resumeInput');
    
    uploadArea.addEventListener('click', () => {
        resumeInput.click();
    });
    
    // File selection
    resumeInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            uploadResume(e.target.files[0]);
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--border)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border)';
        
        if (e.dataTransfer.files.length > 0) {
            uploadResume(e.dataTransfer.files[0]);
        }
    });
    
    // Chat enter key
    document.getElementById('chatInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Smooth scrolling for nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
                
                // Update active link
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });
}

async function uploadResume(file) {
    const allowedExtensions = ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'docx', 'doc', 'txt'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
        showToast('Please upload a valid file (PDF, Image, DOCX, TXT)', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('resume', file);
    
    showLoading(true);
    
    try {
        const response = await fetch('/upload-resume', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySkills(data.skills, data.experience, data.recommendations);
            showToast('Resume analyzed successfully!', 'success');
        } else {
            showToast(data.error || 'Failed to analyze resume', 'error');
        }
    } catch (error) {
        showToast('Error uploading resume: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function displaySkills(skills, experience, recommendations) {
    // Show results container
    const resultsContainer = document.getElementById('skillsResult');
    resultsContainer.style.display = 'block';
    
    // Update stats
    document.getElementById('totalSkills').textContent = skills.length;
    document.getElementById('experienceYears').textContent = experience;
    document.getElementById('matchedJobs').textContent = recommendations.length;
    
    // Display skills
    const skillsGrid = document.getElementById('skillsGrid');
    skillsGrid.innerHTML = '';
    
    // Group skills by category
    const skillsByCategory = {};
    skills.forEach(skill => {
        if (!skillsByCategory[skill.category]) {
            skillsByCategory[skill.category] = [];
        }
        skillsByCategory[skill.category].push(skill.skill);
    });
    
    Object.keys(skillsByCategory).forEach(category => {
        const categorySkills = skillsByCategory[category];
        categorySkills.forEach(skill => {
            const skillTag = document.createElement('span');
            skillTag.className = 'skill-tag';
            skillTag.innerHTML = `<span>✓</span> ${skill}`;
            skillsGrid.appendChild(skillTag);
        });
    });
    
    // Display job recommendations
    displayJobRecommendations(recommendations);
    
    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

function displayJobRecommendations(jobs) {
    const jobsContainer = document.getElementById('jobsContainer');
    
    if (jobs.length === 0) {
        jobsContainer.innerHTML = '<div class="empty-state"><p>No matching jobs found. Try updating your resume with more skills.</p></div>';
        return;
    }
    
    jobsContainer.innerHTML = '';
    
    jobs.forEach(job => {
        const jobCard = document.createElement('div');
        jobCard.className = 'job-card';
        
        const matchColor = job.match_percentage >= 70 ? 'var(--success)' : 
                          job.match_percentage >= 50 ? 'var(--warning)' : 'var(--danger)';
        
        jobCard.innerHTML = `
            <h3 class="job-title">${job.title}</h3>
            <p class="job-company">🏢 ${job.company}</p>
            <p class="job-salary">💰 ${job.salary}</p>
            <span class="job-match" style="background: ${matchColor}">
                ${job.match_percentage}% Match
            </span>
            ${job.experience_match ? 
                '<span class="job-match" style="background: var(--success); margin-left: 0.5rem;">✓ Experience Match</span>' : 
                `<span class="job-match" style="background: var(--warning); margin-left: 0.5rem;">⚠ ${job.min_experience}+ years needed</span>`
            }
            <div class="job-skills">
                ${job.required_skills.slice(0, 6).map(skill => 
                    `<span class="job-skill">${skill}</span>`
                ).join('')}
                ${job.required_skills.length > 6 ? `<span class="job-skill">+${job.required_skills.length - 6} more</span>` : ''}
            </div>
        `;
        
        jobsContainer.appendChild(jobCard);
    });
}

async function analyzeSkillGap() {
    const targetJob = document.getElementById('targetJobInput').value.trim();
    
    if (!targetJob) {
        showToast('Please enter a target job title', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/skill-gap-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ target_job: targetJob })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showToast(data.error, 'error');
            return;
        }
        
        displaySkillGap(data);
    } catch (error) {
        showToast('Error analyzing skill gap: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function displaySkillGap(data) {
    const resultContainer = document.getElementById('skillGapResult');
    
    const hasSkillsHtml = data.has_skills.map(skill => 
        `<span class="skill-has">✓ ${skill}</span>`
    ).join('');
    
    const missingSkillsHtml = data.missing_skills.map(skill => 
        `<span class="skill-missing">✗ ${skill}</span>`
    ).join('');
    
    resultContainer.innerHTML = `
        <h3>Analysis for: ${data.job_details.title}</h3>
        <p style="margin-bottom: 1.5rem; color: var(--gray);">
            ${data.job_details.company} | ${data.job_details.salary}
        </p>
        
        <div class="skills-section">
            <h4>✅ Skills You Have (${data.has_skills.length})</h4>
            <div class="skills-list">
                ${hasSkillsHtml || '<p>No matching skills found</p>'}
            </div>
        </div>
        
        <div class="skills-section">
            <h4>❌ Skills You Need to Learn (${data.missing_skills.length})</h4>
            <div class="skills-list">
                ${missingSkillsHtml || '<p>You have all required skills!</p>'}
            </div>
        </div>
        
        <div style="margin-top: 2rem; padding: 1rem; background: rgba(99, 102, 241, 0.1); border-radius: 8px;">
            <h4 style="color: var(--primary); margin-bottom: 0.5rem;">📚 Recommendation</h4>
            <p>
                ${data.missing_skills.length === 0 ? 
                    'Congratulations! You have all the required skills for this role. Consider applying!' :
                    `Focus on learning these ${data.missing_skills.length} missing skills to improve your chances. You can ask our AI counselor for learning resources!`
                }
            </p>
        </div>
    `;
    
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    input.value = '';
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message
                // API key is hardcoded in backend
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (data.error) {
            console.error('Chat error:', data.error);
            addMessageToChat('Sorry, I encountered an error: ' + data.error, 'bot');
        } else {
            addMessageToChat(data.response, 'bot');
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        console.error('Error sending message:', error);
        addMessageToChat('Sorry, I encountered an error. Please try again.', 'bot');
    }
}

function addMessageToChat(message, type) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'user' ? 'user-message' : 'bot-message';
    
    const avatar = type === 'user' ? '👤' : '🤖';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <p>${message.replace(/\n/g, '<br>')}</p>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'bot-message typing-indicator';
    typingDiv.id = 'typing-' + Date.now();
    
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <p>Typing...</p>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return typingDiv.id;
}

function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

async function generateInterviewQuestions() {
    const jobRole = document.getElementById('interviewJobInput').value.trim();
    
    if (!jobRole) {
        showToast('Please enter a job role', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/interview-prep', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                job_role: jobRole
                // API key is hardcoded in backend
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showToast(data.error, 'error');
        } else {
            document.getElementById('interviewQuestions').innerHTML = 
                `<h4>Interview Questions for ${jobRole}</h4><p>${data.questions.replace(/\n/g, '<br>')}</p>`;
        }
    } catch (error) {
        showToast('Error generating questions: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function showLoading(show) {
    document.getElementById('loadingOverlay').style.display = show ? 'block' : 'none';
}

function showToast(message, type) {
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.textContent = message;
    statusDiv.className = `upload-status ${type}`;
    statusDiv.style.display = 'block';
    
    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 5000);
}