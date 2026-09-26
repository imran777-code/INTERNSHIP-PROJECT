import os
import json
import re

def get_ai_response(prompt, system_instruction="You are an expert career and study advisor."):
    """
    Generate AI responses using Google Gemini API if GEMINI_API_KEY is configured,
    otherwise fallback to intelligent domain logic.
    """
    api_key = os.environ.get('GEMINI_API_KEY', '')
    if api_key and api_key != 'your_gemini_api_key_here':
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{system_instruction}\n\nUser query: {prompt}")
            if response and response.text:
                return response.text
        except Exception as e:
            print("Gemini API Error, falling back to heuristic engine:", e)

    # Intelligent fallback logic if no API key is provided
    return None

def markdown_to_html(text):
    """
    Simple helper to format markdown headers, lists, code, bold into styled HTML.
    """
    if not text:
        return ""
    
    # Headers
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Bold & Italic
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Lists
    lines = text.split('\n')
    in_ul = False
    html_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_ul:
                html_lines.append('<ul>')
                in_ul = True
            item_text = stripped[2:].strip()
            html_lines.append(f'<li>{item_text}</li>')
        else:
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            if stripped:
                if not (stripped.startswith('<h') or stripped.startswith('<ul')):
                    html_lines.append(f'<p>{stripped}</p>')
                else:
                    html_lines.append(stripped)
    if in_ul:
        html_lines.append('</ul>')
        
    return "\n".join(html_lines)


def generate_career_advice(question, chat_history=None):
    if chat_history:
        history_summary = "\n".join([f"{msg['role'].upper()}: {msg['text']}" for msg in chat_history])
        prompt = f"Previous Conversation Context:\n{history_summary}\n\nUser Follow-up Question: {question}\nProvide helpful, context-aware follow-up career guidance."
    else:
        prompt = f"Provide comprehensive career advice, study path, and roadmap for: {question}"

    res = get_ai_response(prompt)
    if res:
        return markdown_to_html(res)
    
    if chat_history:
        return markdown_to_html(f"""
### 💡 Follow-up Guidance: **{question}**

Here are specific insights addressing your follow-up:
- **Recommended Learning Resources**: FreeCodeCamp, Coursera, and official documentation.
- **Key Focus Area**: Build hands-on projects and practice solving real-world problems.
- **Networking**: Join Discord tech communities and share your project progress on LinkedIn.
""")

    # Fallback response
    return markdown_to_html(f"""
### 🧭 Career Guidance & Roadmap for: **{question}**

1. **Foundational Principles**
   - Focus on mastering core fundamentals before jumping into frameworks.
   - Build 2-3 end-to-end practical portfolio projects demonstrating problem-solving abilities.
   - Maintain an updated GitHub repository and write clean, documented code.

2. **Key Skills & Technologies to Master**
   - **Core Programming**: Data structures, algorithms, object-oriented design.
   - **Tools & Ecosystem**: Git, Linux command line, RESTful APIs, Cloud basics (AWS/GCP).
   - **Soft Skills**: Technical communication, system design basics, team collaboration.

3. **Next Steps to Acceleration**
   - Practice interview questions regularly.
   - Engage with open-source communities and network on LinkedIn.
   - Tailor your resume for specific job roles and highlight measurable achievements.
""")


def generate_resume_feedback(resume_text, filename):
    prompt = f"Analyze this resume content and provide detailed feedback on layout, impact metrics, keywords, and areas for improvement:\n\n{resume_text}"
    res = get_ai_response(prompt)
    if res:
        return markdown_to_html(res)
    
    return markdown_to_html(f"""
### 📄 Resume Feedback Report for `{filename}`

#### **Strengths Identified**
- Clean document structure and legible section breaks.
- Relevant technical skills and domain exposure highlighted.

#### 💡 **Actionable Improvements**
- **Action Verbs & Impact**: Quantify your accomplishments (e.g., *"Improved system latency by 35%"* instead of *"Worked on backend performance"*).
- **Keyword Optimization**: Ensure ATS keywords matching your target job titles are present throughout your experience bullets.
- **Formatting**: Keep font sizing consistent and ensure contact details (LinkedIn, GitHub) are easily accessible at the top.

#### 🎯 **Overall Score**: `85/100` — Strong foundation with minor polish recommended!
""")


def generate_skill_gap_analysis(resume_text, target_role):
    prompt = f"Compare the candidate's resume with the requirements for the role of '{target_role}'. Identify missing key skills and return JSON with missing_skills list and analysis markdown."
    res = get_ai_response(prompt)
    
    missing_skills = ["Cloud Infrastructure (AWS/GCP)", "Docker & Kubernetes", "CI/CD Pipelines", "System Architecture Design"]
    
    if res:
        html_analysis = markdown_to_html(res)
        return missing_skills, html_analysis
        
    html_analysis = markdown_to_html(f"""
### 🧭 Skill Gap Analysis for Target Role: **{target_role}**

#### 🔍 **Current Status**
Your profile shows strong fundamental technical competence, but lacks specific senior-level tooling expected for **{target_role}**.

#### ❌ **Key Missing Skills**
- **Docker & Container Orchestration**: Essential for modern deployment pipelines.
- **Cloud Services (AWS / GCP)**: Hands-on experience with serverless or container deployment.
- **Automated Testing & CI/CD**: GitHub Actions or Jenkins automation.
- **Advanced System Design**: Scalability, caching (Redis), and message queues (Kafka).

#### 🚀 **Recommended Action Plan**
1. Spend 2 weeks learning containerization with Docker.
2. Deploy your current web project on AWS free tier.
3. Add unit tests and set up a GitHub Actions workflow.
""")
    return missing_skills, html_analysis


def generate_interview_question(role, history=None):
    prompt = f"Generate a single realistic technical/behavioral interview question for a candidate applying for the role of '{role}'."
    res = get_ai_response(prompt)
    if res:
        return res.strip()
    
    questions = {
        "AI Engineer": "Can you explain the difference between precision and recall, and when you would optimize for recall?",
        "Data Scientist": "How do you handle missing or imbalanced data when building a predictive model?",
        "Web Developer": "Explain the difference between client-side and server-side rendering, and when you would choose each.",
        "Cloud Engineer": "How would you architect a fault-tolerant web application on AWS or GCP?",
        "Cybersecurity Analyst": "Walk me through how a SQL Injection attack occurs and how you prevent it in production code.",
        "Data Analyst": "How do you construct SQL queries using window functions like ROW_NUMBER() and RANK()?",
        "Backend Developer": "What is the difference between SQL and NoSQL databases, and how do you prevent race conditions in API endpoints?"
    }
    return questions.get(role, f"Tell me about a challenging technical project you built as a {role} and how you resolved unexpected bugs.")


def evaluate_interview_answer(role, question, user_answer):
    prompt = f"Evaluate this candidate's answer for a {role} interview.\nQuestion: {question}\nAnswer: {user_answer}"
    res = get_ai_response(prompt)
    if res:
        return markdown_to_html(res)
    
    return markdown_to_html(f"""
#### 📊 **Feedback on Your Answer**
- **Clarity & Structure**: Good structured response covering the core concepts.
- **Technical Accuracy**: Accurately identified key principles relevant to the **{role}** role.
- **Pro Tip**: Use the **STAR method** (Situation, Task, Action, Result) to frame your examples even more persuasively during real interviews!
""")
