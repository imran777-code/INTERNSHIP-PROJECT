from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('ask/', views.ask_view, name='ask'),
    path('ask/followup/<int:question_id>/', views.ask_followup_view, name='ask_followup'),
    path('resume/', views.resume_view, name='resume'),
    path('skill-gap/', views.skill_gap_view, name='skill_gap'),
    path('interview/start/', views.interview_start_view, name='interview_start'),
    path('interview/answer/<int:session_id>/', views.interview_answer_view, name='interview_answer'),
    
    path('history/', views.history_view, name='history'),
    path('download/<str:report_type>/<int:item_id>/', views.download_report_view, name='download_report'),
]
