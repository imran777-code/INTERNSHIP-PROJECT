from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ("AI Engineer", "AI Engineer"),
    ("Data Scientist", "Data Scientist"),
    ("Web Developer", "Web Developer"),
    ("Cloud Engineer", "Cloud Engineer"),
    ("Cybersecurity Analyst", "Cybersecurity Analyst"),
    ("Data Analyst", "Data Analyst"),
    ("UI/UX Designer", "UI/UX Designer"),
    ("DevOps Engineer", "DevOps Engineer"),
    ("Product Manager", "Product Manager"),
    ("Backend Developer", "Backend Developer"),
    ("Frontend Developer", "Frontend Developer"),
    ("Mobile App Developer", "Mobile App Developer"),
    ("QA / Test Automation Engineer", "QA / Test Automation Engineer"),
    ("Blockchain Developer", "Blockchain Developer"),
    ("Game Developer", "Game Developer"),
    ("Business Analyst", "Business Analyst"),
    ("Database Administrator", "Database Administrator"),
    ("Network / Systems Administrator", "Network / Systems Administrator"),
    ("Digital Marketing Specialist", "Digital Marketing Specialist"),
    ("Technical Writer", "Technical Writer"),
]

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-input'})


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-input'})


class QuestionForm(forms.Form):
    question = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. How do I become a Data Scientist?',
            'class': 'form-input'
        })
    )


class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.docx',
            'class': 'dropzone-input',
            'id': 'file-input-resume'
        })
    )


class SkillGapForm(forms.Form):
    skill_gap_resume = forms.FileField(
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.docx',
            'class': 'dropzone-input',
            'id': 'file-input-skill-gap'
        })
    )
    skill_gap_role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class MockInterviewStartForm(forms.Form):
    interview_role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
