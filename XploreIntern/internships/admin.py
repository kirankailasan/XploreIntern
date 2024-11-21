

from django.contrib import admin
from .models import Employer, Student, Job, Internship, Application

@admin.action(description='Approve selected employers')
def approve_employers(modeladmin, request, queryset):
    queryset.update(approved=True)

@admin.action(description='Disapprove selected employers')
def disapprove_employers(modeladmin, request, queryset):
    queryset.update(approved=False)

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'location', 'approved')
    actions = [approve_employers, disapprove_employers]
    list_filter = ('approved',)
    search_fields = ('user__username', 'company_name')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'university', 'course', 'contact_number')
    search_fields = ('user__username', 'full_name', 'university', 'course')

class JobAdmin(admin.ModelAdmin):
    list_display = ('internship_title', 'company_name', 'location', 'is_active')
    search_fields = ('internship_title', 'company_name')
    list_filter = ('is_active', 'experience_level')

class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'type', 'deadline')
    search_fields = ('title', 'company__company_name')
    list_filter = ('type',)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'applied_on', 'status')
    list_filter = ('status',)
    search_fields = ('student__user__username', 'job__internship_title')


admin.site.register(Employer, EmployerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Internship, InternshipAdmin)
admin.site.register(Application, ApplicationAdmin)

class UnapprovedEmployerFilter(admin.SimpleListFilter):
    title = 'approval status'
    parameter_name = 'approved'

    def lookups(self, request, model_admin):
        return (
            ('approved', 'Approved'),
            ('not_approved', 'Not Approved'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'approved':
            return queryset.filter(approved=True)
        elif self.value() == 'not_approved':
            return queryset.filter(approved=False)
        return queryset

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'location', 'approved')
    actions = [approve_employers, disapprove_employers]
    list_filter = ('approved', UnapprovedEmployerFilter)
    search_fields = ('user__username', 'company_name')

class JobInline(admin.TabularInline):
    model = Job
    extra = 0  # No extra empty forms in inline display

class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'location', 'approved')
    actions = [approve_employers, disapprove_employers]
    list_filter = ('approved', UnapprovedEmployerFilter)
    search_fields = ('user__username', 'company_name')
    inlines = [JobInline]

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'university', 'course', 'contact_number')
    search_fields = ('user__username', 'full_name', 'university', 'course')
    inlines = [ApplicationInline]
