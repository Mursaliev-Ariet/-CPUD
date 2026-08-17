from django.contrib import admin
from .models import Employee, Employer, Resume, Vacancy

# ===== СОТРУДНИК (Employee) =====
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'email', 'city']
    search_fields = ['full_name', 'phone', 'email']
    list_filter = ['city']

# ===== РАБОТОДАТЕЛЬ (Employer) =====
@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'phone', 'email', 'address']
    search_fields = ['company_name', 'phone', 'email']
    list_filter = ['address']

# ===== РЕЗЮМЕ (Resume) =====
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'employee', 'desired_salary', 'employment_type', 'is_active', 'created_at']
    search_fields = ['title', 'employee__full_name', 'skills']
    list_filter = ['is_active', 'employment_type', 'created_at']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

# ===== ВАКАНСИЯ (Vacancy) =====
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'employer', 'location', 'salary_from', 'salary_to', 'employment_type', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'employer__company_name']
    list_filter = ['is_active', 'employment_type', 'experience_required', 'created_at']
    readonly_fields = ['created_at']
    ordering = ['-created_at']