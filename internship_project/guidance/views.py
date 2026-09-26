import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages

from .forms import (
    UserSignupForm, UserLoginForm, QuestionForm, 
    ResumeUploadForm, SkillGapForm, MockInterviewStartForm, ROLE_CHOICES
)
from .models import Question, ResumeCheck, SkillGapReport, MockInterviewSession
from .pdf_utils import extract_text_from_file
from .ai_service import (
    generate_career_advice, generate_resume_feedback, 
    generate_skill_gap_analysis, generate_interview_question, 
    evaluate_interview_answer
)

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('index')
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
    else:
        form = UserLoginForm(request)
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def index_view(request):
    # Fetch recent items for user
    recent_questions = Question.objects.filter(user=request.user)[:5]
    recent_resumes = ResumeCheck.objects.filter(user=request.user)[:5]
    recent_skill_gaps = SkillGapReport.objects.filter(user=request.user)[:5]
    active_interview = MockInterviewSession.objects.filter(user=request.user, is_completed=False).first()

    # Calculate explored waypoints count
    explored = 0
    if Question.objects.filter(user=request.user).exists(): explored += 1
    if ResumeCheck.objects.filter(user=request.user).exists(): explored += 1
    if SkillGapReport.objects.filter(user=request.user).exists(): explored += 1
    if MockInterviewSession.objects.filter(user=request.user).exists(): explored += 1
    
    explored_percent = int((explored / 4) * 100)

    context = {
        'roles': [r[0] for r in ROLE_CHOICES],
        'recent_questions': recent_questions,
        'recent_resumes': recent_resumes,
        'recent_skill_gaps': recent_skill_gaps,
        'active_interview': active_interview,
        'explored_count': explored,
        'explored_percent': explored_percent,
        'active_tab': request.GET.get('tab', 'tab-dashboard')
    }
    return render(request, 'index.html', context)


@login_required
def ask_view(request):
    if request.method == 'POST':
        question_text = request.POST.get('question', '').strip()
        if question_text:
            answer_html = generate_career_advice(question_text)
            messages_list = [
                {'role': 'user', 'text': question_text},
                {'role': 'assistant', 'text': answer_html}
            ]
            q_obj = Question.objects.create(
                user=request.user,
                question_text=question_text,
                answer_text=answer_html,
                messages=messages_list
            )
            context = {
                'roles': [r[0] for r in ROLE_CHOICES],
                'asked_question': q_obj,
                'active_tab': 'tab-advisor'
            }
            return render(request, 'index.html', context)
    return redirect('/?tab=tab-advisor')


@login_required
def ask_followup_view(request, question_id):
    q_obj = get_object_or_404(Question, id=question_id, user=request.user)
    if request.method == 'POST':
        followup_text = request.POST.get('followup_question', '').strip()
        if followup_text:
            history = q_obj.messages or [
                {'role': 'user', 'text': q_obj.question_text},
                {'role': 'assistant', 'text': q_obj.answer_text}
            ]
            followup_html = generate_career_advice(followup_text, chat_history=history)
            
            history.append({'role': 'user', 'text': followup_text})
            history.append({'role': 'assistant', 'text': followup_html})
            
            q_obj.messages = history
            q_obj.save()

    context = {
        'roles': [r[0] for r in ROLE_CHOICES],
        'asked_question': q_obj,
        'active_tab': 'tab-advisor'
    }
    return render(request, 'index.html', context)


@login_required
def resume_view(request):
    if request.method == 'POST' and request.FILES.get('resume_file'):
        file_obj = request.FILES['resume_file']
        resume_check = ResumeCheck(
            user=request.user,
            resume_file=file_obj,
            original_filename=file_obj.name
        )
        resume_check.save()
        
        extracted_text = extract_text_from_file(resume_check.resume_file.path)
        feedback_html = generate_resume_feedback(extracted_text, file_obj.name)
        
        resume_check.feedback_html = feedback_html
        resume_check.save()

        context = {
            'roles': [r[0] for r in ROLE_CHOICES],
            'resume_result': resume_check,
            'active_tab': 'tab-resume'
        }
        return render(request, 'index.html', context)
    return redirect('/?tab=tab-resume')


@login_required
def skill_gap_view(request):
    if request.method == 'POST' and request.FILES.get('skill_gap_resume'):
        file_obj = request.FILES['skill_gap_resume']
        target_role = request.POST.get('skill_gap_role', 'Software Engineer')
        
        # Save file to media temporarily
        file_path = os.path.join(settings.MEDIA_ROOT, 'resumes', file_obj.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
                
        extracted_text = extract_text_from_file(file_path)
        missing_skills, analysis_html = generate_skill_gap_analysis(extracted_text, target_role)

        report = SkillGapReport.objects.create(
            user=request.user,
            target_role=target_role,
            resume_filename=file_obj.name,
            missing_skills=missing_skills,
            analysis_html=analysis_html
        )

        context = {
            'roles': [r[0] for r in ROLE_CHOICES],
            'skill_gap_result': report,
            'active_tab': 'tab-skillgap'
        }
        return render(request, 'index.html', context)
    return redirect('/?tab=tab-skillgap')


@login_required
def interview_start_view(request):
    if request.method == 'POST':
        role = request.POST.get('interview_role', 'Software Engineer')
        first_q = generate_interview_question(role)
        
        # Deactivate any previous open interview session
        MockInterviewSession.objects.filter(user=request.user, is_completed=False).update(is_completed=True)
        
        session = MockInterviewSession.objects.create(
            user=request.user,
            target_role=role,
            current_question=first_q,
            qna_history=[]
        )
        context = {
            'roles': [r[0] for r in ROLE_CHOICES],
            'interview_session': session,
            'active_tab': 'tab-interview'
        }
        return render(request, 'index.html', context)
    return redirect('/?tab=tab-interview')


@login_required
def interview_answer_view(request, session_id):
    session = get_object_or_404(MockInterviewSession, id=session_id, user=request.user)
    if request.method == 'POST':
        user_answer = request.POST.get('user_answer', '').strip()
        if user_answer and not session.is_completed:
            feedback = evaluate_interview_answer(session.target_role, session.current_question, user_answer)
            
            history = session.qna_history or []
            history.append({
                'question': session.current_question,
                'user_answer': user_answer,
                'feedback': feedback
            })
            session.qna_history = history
            
            if len(history) >= 3:
                session.is_completed = True
                session.summary_html = f"<p>Great job! You have completed 3 questions for <strong>{session.target_role}</strong> mock interview.</p>"
                session.current_question = ""
            else:
                session.current_question = generate_interview_question(session.target_role, history)
            
            session.save()

    context = {
        'roles': [r[0] for r in ROLE_CHOICES],
        'interview_session': session,
        'active_tab': 'tab-interview'
    }
    return render(request, 'index.html', context)


@login_required
def history_view(request):
    user = request.user
    questions = Question.objects.filter(user=user)
    resumes = ResumeCheck.objects.filter(user=user)
    skill_gaps = SkillGapReport.objects.filter(user=user)
    interviews = MockInterviewSession.objects.filter(user=user)

    total_q = questions.count()
    total_r = resumes.count()
    total_s = skill_gaps.count()
    total_i = interviews.count()
    total_activities = total_q + total_r + total_s + total_i

    context = {
        'questions': questions,
        'resumes': resumes,
        'skill_gaps': skill_gaps,
        'interviews': interviews,
        'total_activities': total_activities,
        'total_q': total_q,
        'total_r': total_r,
        'total_s': total_s,
        'total_i': total_i,
    }
    return render(request, 'history.html', context)


@login_required
def download_report_view(request, report_type, item_id):
    """
    Download a formatted text/markdown summary of any history item.
    """
    filename = f"trailmark_{report_type}_{item_id}.txt"
    content = ""
    
    if report_type == 'question':
        item = get_object_or_404(Question, id=item_id, user=request.user)
        content = f"TRAILMARK - QUESTION REPORT\nDate: {item.created_at}\nQuestion: {item.question_text}\n\nAnswer:\n{item.answer_text}"
    elif report_type == 'resume':
        item = get_object_or_404(ResumeCheck, id=item_id, user=request.user)
        content = f"TRAILMARK - RESUME REVIEW\nDate: {item.created_at}\nFile: {item.original_filename}\n\nFeedback:\n{item.feedback_html}"
    elif report_type == 'skillgap':
        item = get_object_or_404(SkillGapReport, id=item_id, user=request.user)
        content = f"TRAILMARK - SKILL GAP REPORT\nTarget Role: {item.target_role}\nDate: {item.created_at}\nMissing Skills: {', '.join(item.missing_skills)}\n\nAnalysis:\n{item.analysis_html}"
    elif report_type == 'interview':
        item = get_object_or_404(MockInterviewSession, id=item_id, user=request.user)
        content = f"TRAILMARK - MOCK INTERVIEW\nTarget Role: {item.target_role}\nDate: {item.created_at}\n\nQ&A History:\n"
        for i, qna in enumerate(item.qna_history, 1):
            content += f"\nQ{i}: {qna['question']}\nYour Answer: {qna['user_answer']}\nFeedback:\n{qna['feedback']}\n{'-'*40}\n"

    response = HttpResponse(content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
