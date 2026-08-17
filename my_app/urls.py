from django.urls import path
from .views import (
    register,
    CustomTokenObtainPairView,
    employee_list, employee_detail,
    employer_list, employer_detail,
    resume_list, resume_detail,
    vacancy_list, vacancy_detail
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('employees/', employee_list, name='employee-list'),
    path('employees/<int:pk>/', employee_detail, name='employee-detail'),

    path('employers/', employer_list, name='employer-list'),
    path('employers/<int:pk>/', employer_detail, name='employer-detail'),

    path('resumes/', resume_list, name='resume-list'),
    path('resumes/<int:pk>/', resume_detail, name='resume-detail'),

    path('vacancies/', vacancy_list, name='vacancy-list'),
    path('vacancies/<int:pk>/', vacancy_detail, name='vacancy-detail'),
]