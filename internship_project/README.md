# Trailmark — AI Career & Study Guidance Assistant

Trailmark is an AI-powered career companion designed to help students, developers, and professionals navigate tech career paths, review resumes, identify skill gaps, and practice mock interviews.

---

## 🌟 Key Features

1. **AI Career Advisor**:
   - Ask any career or study-related question.
   - Receive structured advice, study roadmaps, and course recommendations.

2. **Resume Review**:
   - Drag-and-drop resume upload (PDF / DOCX support).
   - Instant AI evaluation highlighting strengths, key improvement areas, and impact metrics.

3. **Skill Gap Analysis**:
   - Upload your resume and select a target role (e.g., AI Engineer, Data Scientist, Web Developer, Cloud Engineer).
   - Get a missing skills breakdown and a prioritized learning plan.

4. **Mock Interview Simulator**:
   - Interactive role-tailored interview practice.
   - Instant feedback on every response evaluated using technical criteria and the STAR methodology.

5. **Personal Activity History & PDF/Text Reports**:
   - Visual dashboard tracking explored waypoints, activity breakdown, and skill gap trends.
   - Download past Q&A sessions, resume reviews, skill gap reports, and mock interview transcripts.

6. **Theme & Dark Mode Support**:
   - Native dark/light mode toggle with theme memory.

---

## 🛠️ Tech Stack & Setup

- **Backend**: Python 3.x, Django 4.2+
- **Database**: SQLite3
- **PDF/DOCX Extraction**: `pypdf`, `python-docx`
- **AI Engine**: Google Gemini API (`google-generativeai`) with intelligent local fallback logic
- **Frontend**: Responsive HTML5, Vanilla CSS3 (Custom Design System), JavaScript ES6

---

## 🚀 Local Installation & Setup

1. **Clone or Open Project Directory**:
   ```bash
   cd E:\3-2\LABS\internship\project
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables** (Optional for Gemini API):
   Create a `.env` file or export your `GEMINI_API_KEY`:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser / Admin Account** (Optional):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Dev Server**:
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 📂 Project Structure

```
project/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── trailmark/            # Main Django Configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── guidance/             # Main Application App
    ├── models.py         # Question, ResumeCheck, SkillGapReport, MockInterview
    ├── views.py          # Application Controllers
    ├── ai_service.py     # Gemini AI & Fallback Logic
    ├── pdf_utils.py      # Resume Parser (PDF/DOCX)
    ├── forms.py          # Authentication & Tool Forms
    ├── templates/        # HTML Layouts (index, history, login, signup)
    └── urls.py
```
