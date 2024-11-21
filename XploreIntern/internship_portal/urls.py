# internships/urls.py
from django.urls import path, include
from internships import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
    path('home/', views.home, name='home'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/employers/', views.employer_list, name='employer_list'),
    path('admin/employer/approve/<int:employer_id>/', views.approve_employer, name='approve_employer'),
    path('admin/internships/', views.internship_list, name='internship_list'),
    path('admin/employer/<int:employer_id>/disapprove/', views.disapprove_employer, name='disapprove_employer'),
    path('admin/employer/<int:employer_id>/', views.view_employer, name='view_employer'),
    path('register/', views.register, name='register'),
    path('register/employer/', views.employer_registration, name='employer_registration'),
    path('register/student/', views.student_registration, name='student_registration'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('post_job/', views.post_job, name='post_job'),
    path('job/<int:job_id>/', views.job_preview, name='job_preview'),  # URL for previewing job
    path('job/<int:job_id>/edit/', views.edit_job, name='edit_job'),  # URL for editing job
    path('student/apply/', views.apply_job, name='apply_job'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('job/<int:job_id>view_applications/',views.view_applications, name='view_applications'),
    path('student/update_profile/', views.update_profile, name='update_profile'),
    path('employer/update_employ/', views.update_employ, name='update_employ'),
    path('internships/', views.internships_list, name='internships_list'),
    path('about/', views.about, name='about'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('application/<int:application_id>/accept/', views.accept_application, name='accept_application'),
    path('application/<int:application_id>/reject/', views.reject_application, name='reject_application'),
    path('employer/withdraw-job/<int:job_id>/', views.withdraw_job, name='withdraw_job'),
    path('application/<int:application_id>/profile/', views.full_profile, name='full_profile'),   
    path('notifications/', views.notifications, name='notifications'),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)