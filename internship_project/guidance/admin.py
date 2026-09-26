from django.contrib import admin
from .models import Question, ResumeCheck, SkillGapReport, MockInterviewSession

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_text', 'created_at')
    search_fields = ('question_text', 'user__username')

@admin.register(ResumeCheck)
class ResumeCheckAdmin(admin.ModelAdmin):
    list_display = ('user', 'original_filename', 'created_at')
    search_fields = ('original_filename', 'user__username')

@admin.register(SkillGapReport)
class SkillGapReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'resume_filename', 'created_at')
    search_fields = ('target_role', 'user__username')

@admin.register(MockInterviewSession)
class MockInterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'is_completed', 'created_at')
    search_fields = ('target_role', 'user__username')
