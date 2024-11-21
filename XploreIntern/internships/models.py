# internships/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Company linked to User (employer)
    company_name = models.CharField(max_length=100)

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.FileField(upload_to='logo/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)  # Field to track approval status
    name= models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.company_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    academic_status = models.CharField(max_length=50, null=True, blank=True)
    field_of_study = models.CharField(max_length=100, null=True, blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    preferred_location = models.CharField(max_length=100, null=True, blank=True)
    internship_duration = models.CharField(max_length=50, null=True, blank=True)
    industry_interest = models.CharField(max_length=100, null=True, blank=True)
    logo = models.FileField(upload_to='logo/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    stipend_expectation = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def profile_completion(self):
        # Check each field's completion
        fields = [
            self.full_name, self.date_of_birth, self.contact_number, self.academic_status,
            self.field_of_study, self.university, self.preferred_location, self.internship_duration,
            self.industry_interest,
            self.stipend_expectation, self.skills, self.resume
        ]
        completed_fields = sum([1 for field in fields if field])
        total_fields = len(fields)
        return round((completed_fields / total_fields) * 100)

class Internship(models.Model):
    company = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[('full-time', 'Full-Time'), ('part-time', 'Part-Time')])
    deadline = models.DateField()

class Application(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=[('applied', 'Applied'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
                              default='applied')
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    

class Job(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to Employer model
    internship_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    internship_type = models.CharField(max_length=50, choices=[('Full-time', 'Full-Time'), ('Part-time', 'Part-Time'), ('Contract', 'Contract'), ('Temporary', 'Temporary')])
    experience_level = models.CharField(max_length=50, choices=[('Entry-level', 'Entry-Level'), ('Junior', 'Junior'), ('Mid-level', 'Mid-Level'), ('Senior', 'Senior'), ('Executive', 'Executive')])
    salary_range = models.CharField(max_length=100)
    benefits = models.TextField()
    summary = models.TextField()
    key_responsibilities = models.TextField()
    required_qualifications = models.TextField()
    preferred_qualifications = models.TextField(blank=True)
    skills = models.TextField()
    application_instructions = models.TextField()
    application_deadline = models.DateField()
    contact_information = models.TextField()
    company_overview = models.TextField()
    company_website = models.URLField()
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.internship_title