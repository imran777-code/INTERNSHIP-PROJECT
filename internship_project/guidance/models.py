from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    answer_text = models.TextField()
    messages = models.JSONField(default=list)  # list of {'role': 'user'|'assistant', 'text': html/text}
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.question_text[:30]}"


class ResumeCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_checks')
    resume_file = models.FileField(upload_to='resumes/')
    original_filename = models.CharField(max_length=255)
    feedback_html = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.original_filename}"


class SkillGapReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_gaps')
    target_role = models.CharField(max_length=100)
    resume_filename = models.CharField(max_length=255)
    missing_skills = models.JSONField(default=list)
    analysis_html = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.target_role}"


class MockInterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mock_interviews')
    target_role = models.CharField(max_length=100)
    current_question = models.TextField(blank=True, default='')
    qna_history = models.JSONField(default=list)  # [{'question': ..., 'user_answer': ..., 'feedback': ...}]
    is_completed = models.BooleanField(default=False)
    summary_html = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.target_role} ({'Completed' if self.is_completed else 'Active'})"
