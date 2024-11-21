# internships/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Employer, Student
from .models import Job, Application
from django.utils.timezone import now

class EmployerRegisterForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class StudentRegisterForm(UserCreationForm):
    university = forms.CharField(max_length=100)
    course = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'internship_title', 'company_name', 'location', 'internship_type', 
            'experience_level', 'salary_range', 'benefits', 'summary', 
            'key_responsibilities', 'required_qualifications', 'preferred_qualifications', 
            'skills', 'application_instructions', 'application_deadline', 
            'contact_information', 'company_overview', 'company_website'
        ]
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date', 'min': now().strftime('%Y-%m-%d')})
        }
       

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume'] 
        resume = forms.FileField(
            required=False,
            widget=forms.ClearableFileInput(attrs={'class': 'file-input'}),
    )

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'logo', 'full_name', 'date_of_birth', 'contact_number', 'academic_status',
            'field_of_study', 'university', 'preferred_location', 'internship_duration',
            'industry_interest',
            'stipend_expectation', 'skills', 'resume'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

   

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = [
             'logo', 'name', 'contact_number', 'location', 'company_name', 'description'
        ]
   