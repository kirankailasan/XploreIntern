# internships/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail,  EmailMessage
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from .forms import EmployerRegisterForm, StudentRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Employer, Student
from .models import Job, Company
from .forms import JobForm, ApplicationForm, StudentProfileForm, EmployerProfileForm
from internships.models import Job, Application, Student
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse


def register(request):
    return render(request, 'internships/register.html')

def home(request):
    featured_jobs = Job.objects.filter(is_active=True)[:5]  # Display 5 featured jobs
    for job in featured_jobs:
        try:
            employer = job.company.employer  # Access Employer linked to the company (User)
            job.company_logo_url = employer.logo.url if employer.logo else None
        except Employer.DoesNotExist:
            job.company_logo_url = None

    return render(request, 'internships/home.html', {'featured_jobs': featured_jobs})

def employer_registration(request):
    if request.method == 'POST':
        form = EmployerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Employer.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                location=form.cleaned_data['location']
            )
            messages.success(request, "You have successfully registered.")
            
            # Render email HTML content
            email_content = render_to_string('internships/email/registration_success.html', {
                'user': user,
                'company_name': form.cleaned_data['company_name']
            })
            email = EmailMessage(
                'Registration Success - Welcome to XploreIntern',
                email_content,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.content_subtype = "html"  # Set the email to HTML
            email.send(fail_silently=False)
            
            return render(request, 'internships/home.html', {'show_login_modal': True})
    else:
        form = EmployerRegisterForm()
    return render(request, 'internships/employer_register.html', {'form': form})

def student_registration(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user, university=form.cleaned_data['university'], course=form.cleaned_data['course'])
            messages.success(request, "You have successfully registered." )
            # Render email HTML content
            email_content = render_to_string('internships/email/student_register_success.html', {
                'user': user,
                'university': form.cleaned_data['university']
            })
            email = EmailMessage(
                'Registration Success - Welcome to XploreIntern',
                email_content,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.content_subtype = "html"  # Set the email to HTML
            email.send(fail_silently=False)
            
            return render(request, 'internships/home.html', {'show_login_modal': True})
    else:
        form = StudentRegisterForm()
    return render(request, 'internships/student_register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                employer = user.employer
                if employer.approved:
                    login(request, user)
                    return redirect('employer_dashboard')
                else:
                    messages.error(request, 'Employer account is not approved yet.')
                    return redirect('login')
            except Employer.DoesNotExist:
                login(request, user)
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'internships/home.html')

@login_required
def employer_dashboard(request):
    employerr = Employer.objects.get(user=request.user)
    employer = Employer.objects.filter(user=request.user).first()


    if employer:
        jobs = Job.objects.filter(company=request.user)
        print(f"Number of jobs found: {len(jobs)}")
    else:
        jobs = []
    
    return render(request, 'internships/employer_dashboard.html', {'jobs': jobs , 'employerr':employer})

@login_required
def job_preview(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user)  # Ensure job belongs to the logged-in employer
    return render(request, 'internships/job_preview.html', {'job': job})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user)  # Ensure job belongs to the logged-in employer
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')  # Redirect to dashboard after editing
    else:
        form = JobForm(instance=job)
    return render(request, 'internships/edit_job.html', {'form': form, 'job': job})



@login_required
def post_job(request):
    # Get the Employer object for the logged-in user
    employer = Employer.objects.filter(user=request.user).first()

    if not employer:
        # Handle the case if the logged-in user is not an employer
        return redirect('some_error_page')  # Or show an error message

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user  # Assign the job to the employer
            job.save()
            return redirect('employer_dashboard')  # Redirect to dashboard after posting
    else:
        form = JobForm()

    return render(request, 'internships/post_job.html', {'form': form})


@login_required
def view_jobs(request):
    jobs = Job.object.all()
    return render(request, 'internships/view_jobs.html', {'jobs': jobs})




@login_required
def apply_job(request):
    # Fetch all available jobs
    jobs = Job.objects.filter(is_active=True)
    applied_job_ids = Application.objects.filter(student=request.user.student).values_list('job_id', flat=True)

    return render(request, 'internships/apply_job.html', {
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,
    })

@login_required
def full_profile(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    student = application.student
    return render(request, 'internships/full_profile.html', {'application': application, 'student': student})

 

@login_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user)
    applications = Application.objects.filter(job=job)
   
    return render(request, 'internships/view_applications.html', {'job': job, 'applications': applications})



@login_required
def search_jobs(request):
    query = request.GET.get('q', '')
    jobs = Job.objects.filter(internship_title__icontains=query)
    return render(request, 'internships/search_results.html', {'jobs': jobs, 'query': query})

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    student = Student.objects.get(user=request.user)
    employer = Employer.objects.filter(user=job.company).first()

    if student.resume:
        form = ApplicationForm(request.POST or None, request.FILES or None, initial={'resume': student.resume})
    else:
        form = ApplicationForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student
            application.job = job
            # Use the student's existing resume if no new file is uploaded
            if not form.cleaned_data['resume'] and student.resume:
                application.resume = student.resume
            application.save()
            return redirect('student_dashboard')

    return render(request, 'internships/apply_for_job.html', {'form': form, 'employer': employer, 'job': job})

@login_required
def update_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)

        if request.POST.get('remove_logo') == '1':
            student.logo.delete(save=False) 
            student.logo = None
            student.save()  # Save the change to the database
            messages.success(request, "Profile image removed successfully.")
            return redirect('update_profile')

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=student)

    profile_completion = student.profile_completion()
    return render(request, 'internships/update_profile.html', {
        'form': form,
        'profile_completion': profile_completion
    })

@login_required
def update_employ(request):
    employer = Employer.objects.get(user=request.user)
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer)

        if request.POST.get('remove_logo') == '1':
            employer.logo.delete(save=False) 
            employer.logo = None
            employer.save()  # Save the change to the database
            messages.success(request, "Profile image removed successfully.")
            return redirect('update_employ')
        
        
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm(instance=employer)

    return render(request, 'internships/update_employ.html', {
        'form': form,
    })

@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    applications = Application.objects.filter(student=student)
    

    unread_notifications = Application.objects.filter(
        student=student,
        is_read=False,  # Only unread notifications
        status__in=['accepted', 'rejected']  # Relevant statuses
    ).exists()
    

    profile_completion = student.profile_completion()
    return render(request, 'internships/student_dashboard.html', {'applications': applications, 
        'profile_completion': profile_completion, 'student' : student, 'unread_notifications': unread_notifications,})

def about(request):
    return render(request, 'internships/about.html')

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def withdraw_job(request, job_id):
    job=get_object_or_404(Job, id=job_id, company=request.user, is_active=True)
    job.is_active=False
    job.save()
    Application.objects.filter(job=job).update(status='Withdrawn')
    messages.success(request, "Job has been successfully withdrawn.")
    return redirect('employer_dashboard')

@login_required
def accept_application(request, application_id):
    
    application = get_object_or_404(Application, id=application_id)
    application.status= 'accepted'
    application.is_read= False
    application.save()
    messages.success(request, "Application accepted.")
    user = application.student.user
    email_content = render_to_string('internships/email/accept.html', {
                'user': user,
                'job_title': application.job.internship_title,
                'company_name': application.job.company_name
                
            })
    email = EmailMessage(
                subject='Congratulations! Your Application Has Been Accepted',
                body=email_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
    email.content_subtype = "html"  # Set the email to HTML
    email.send(fail_silently=False)

    return redirect('view_applications', job_id=application.job.id, )

@login_required
def reject_application(request, application_id):
    
    application = get_object_or_404(Application, id=application_id)
    application.status = 'rejected'
    application.is_read = False
    application.save()
    messages.success(request, "Application rejected.")
    user = application.student.user
    email_content = render_to_string('internships/email/reject.html', {
                'user': user,
                'job_title': application.job.internship_title,
                'company_name': application.job.company_name
            })
    email = EmailMessage(
                subject='Regarding Your Recent Internship Application',
                body=email_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
    email.content_subtype = "html"  # Set the email to HTML
    email.send(fail_silently=False)


    return redirect('view_applications', job_id=application.job.id)

def internships_list(request):
    query = request.GET.get('query', '')
    location = request.GET.get('location', '')
    company = request.GET.get('company', '')
    applied_job_ids = []

    # Check if the user is logged in and has a student profile
    if request.user.is_authenticated:
        try:
            applied_job_ids = Application.objects.filter(student=request.user.student).values_list('job_id', flat=True)
        except ObjectDoesNotExist:
            # If the user does not have a student profile, just pass an empty list for applied_job_ids
            pass

    # Filter jobs based on search inputs
    jobs = Job.objects.filter(is_active=True)
    if query:
        jobs = jobs.filter(internship_title__icontains=query)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if company:
        jobs = jobs.filter(company_name__icontains=company)

    # Add employer's logo URL to each job in the queryset
    for job in jobs:
        try:
            employer = job.company.employer  # Access Employer linked to the company (User)
            job.company_logo_url = employer.logo.url if employer.logo else None
        except Employer.DoesNotExist:
            job.company_logo_url = None

    # Pagination: show 10 internships per page
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'internships/internships_list.html', {
        'applied_job_ids': applied_job_ids,
        'page_obj': page_obj,
        'query': query,
        'location': location,
        'company': company
    })

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employer, Student, Internship, Application, Job


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def is_admin(user):
    return user.is_staff

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'internships/admin_panel/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


# Admin dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_employers = Employer.objects.count()
    total_students = Student.objects.count()
    total_internships = Job.objects.count()
    total_applications = Application.objects.count()
    return render(request, 'internships/admin_panel/dashboard.html', {
        'total_employers': total_employers,
        'total_students': total_students,
        'total_internships': total_internships,
        'total_applications': total_applications,
    })

# View and approve employers
@login_required
@user_passes_test(is_admin)
def employer_list(request):
    employers = Employer.objects.all()
    return render(request, 'internships/admin_panel/employer_list.html', {'employers': employers})

@login_required
@user_passes_test(is_admin)
def approve_employer(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    employer.approved = True
    employer.save()

    email_subject = 'Account Approved - Welcome to XploreIntern!'
    email_content = render_to_string('internships/email/approve.html', {
        'name': employer.user.username,
        'company_name': employer.company_name,
    })
    email = EmailMessage(
        email_subject,
        email_content,
        settings.EMAIL_HOST_USER,
        [employer.user.email]
    )
    email.content_subtype = 'html'  # Set the email content type to HTML
    email.send(fail_silently=False)
    return redirect('employer_list')

@login_required
@user_passes_test(is_admin)
def disapprove_employer(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    employer.approved = False
    employer.save()
    email_subject = 'Account Disapproved - XploreIntern'
    email_content = render_to_string('internships/email/disapprove.html', {
        'name': employer.user.username,
        'company_name': employer.company_name,
    })
    email = EmailMessage(
        email_subject,
        email_content,
        settings.EMAIL_HOST_USER,
        [employer.user.email]
    )
    email.content_subtype = 'html'  # Set the email content type to HTML
    email.send(fail_silently=False)
    return redirect('employer_list')

# View and manage internships
@login_required
@user_passes_test(is_admin)
def internship_list(request):
    jobs = Job.objects.all()
    return render(request, 'internships/admin_panel/internship_list.html', {'jobs': jobs})

@login_required
@user_passes_test(is_admin)
def view_employer(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    email = employer.user.email  # Fetch email from the related User model
    return render(request, 'internships/admin_panel/view_employer.html', {
        'employer': employer,
        'email': email
    })

# Other views for students, applications, and jobs...
from django.http import HttpResponseForbidden

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not allowed to access this page.")
    return wrapper

@login_required
def notifications(request):
    student = request.user.student
    notifications = Application.objects.filter(
        student=student,
        status__in=['accepted', 'rejected']  # Only fetch accepted/rejected applications
    ).order_by('-applied_on')

    notifications.update(is_read=True)
    
   
    
    return render(request, 'internships/notifications.html', {
        'notifications': notifications
    })