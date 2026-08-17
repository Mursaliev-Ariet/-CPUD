from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Employee, Employer, Resume, Vacancy
from .serializers import (
    EmployeeSerializer, EmployerSerializer,
    ResumeSerializer, VacancySerializer,
    RegisterSerializer, CustomTokenObtainPairSerializer
)

# регистрация
@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        role = 'employee' if hasattr(user, 'employee_profile') else 'employer'
        return Response({
            'message': 'Пользователь создан',
            'username': user.username,
            'role': role
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# вход через почту
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
                'role': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['employee', 'employer'],
                    description='Роль (опционально). Если не указать — определится автоматически.'
                ),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# сотрудник
@swagger_auto_schema(method='post', request_body=EmployeeSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employee_list(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        return Response(EmployeeSerializer(employees, many=True).data)
    elif request.method == 'POST':
        if hasattr(request.user, 'employee_profile'):
            return Response({'error': 'Профиль уже существует'}, status=400)
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
# посмотреть, обновить, удалить
@swagger_auto_schema(method='put',request_body=EmployeeSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({'error': 'Не найдено'}, status=404)
    if request.method in ['PUT', 'DELETE'] and employee.user != request.user:
        return Response({'error': 'Нет прав'}, status=403)
    if request.method == 'GET':
        return Response(EmployeeSerializer(employee).data)
    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=204)

# работодатель
@swagger_auto_schema(method='post', request_body=EmployerSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employer_list(request):
    if request.method == 'GET':
        employers = Employer.objects.all()
        return Response(EmployerSerializer(employers, many=True).data)
    elif request.method == 'POST':
        if hasattr(request.user, 'employer_profile'):
            return Response({'error': 'Профиль уже существует'}, status=400)
        serializer = EmployerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
# посмотреть, обновить, удалить
@swagger_auto_schema(method='put',request_body=EmployerSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employer_detail(request, pk):
    try:
        employer = Employer.objects.get(pk=pk)
    except Employer.DoesNotExist:
        return Response({'error': 'Не найдено'}, status=404)
    if request.method in ['PUT', 'DELETE'] and employer.user != request.user:
        return Response({'error': 'Нет прав'}, status=403)
    if request.method == 'GET':
        return Response(EmployerSerializer(employer).data)
    elif request.method == 'PUT':
        serializer = EmployerSerializer(employer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        employer.delete()
        return Response(status=204)

# резюме от сотрудника
@swagger_auto_schema(method='post', request_body=ResumeSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def resume_list(request):
    if request.method == 'GET':
        resumes = Resume.objects.filter(is_active=True)
        return Response(ResumeSerializer(resumes, many=True).data)
    elif request.method == 'POST':
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({'error': 'Вы не сотрудник'}, status=403)
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
# посмотреть, обновить, удалить
@swagger_auto_schema(method='put',request_body=ResumeSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def resume_detail(request, pk):
    try:
        resume = Resume.objects.get(pk=pk)
    except Resume.DoesNotExist:
        return Response({'error': 'Не найдено'}, status=404)
    if request.method in ['PUT', 'DELETE'] and resume.employee.user != request.user:
        return Response({'error': 'Нет прав'}, status=403)
    if request.method == 'GET':
        return Response(ResumeSerializer(resume).data)
    elif request.method == 'PUT':
        serializer = ResumeSerializer(resume, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        resume.delete()
        return Response(status=204)

# вакансии от работодателя
@swagger_auto_schema(method='post', request_body=VacancySerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vacancy_list(request):
    if request.method == 'GET':
        vacancies = Vacancy.objects.filter(is_active=True)
        return Response(VacancySerializer(vacancies, many=True).data)
    elif request.method == 'POST':
        try:
            employer = Employer.objects.get(user=request.user)
        except Employer.DoesNotExist:
            return Response({'error': 'Вы не работодатель'}, status=403)
        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=employer)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
# посмотреть, обновить, удалить
@swagger_auto_schema(method='put',request_body=VacancySerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def vacancy_detail(request, pk):
    try:
        vacancy = Vacancy.objects.get(pk=pk)
    except Vacancy.DoesNotExist:
        return Response({'error': 'Не найдено'}, status=404)
    if request.method in ['PUT', 'DELETE'] and vacancy.employer.user != request.user:
        return Response({'error': 'Нет прав'}, status=403)
    if request.method == 'GET':
        return Response(VacancySerializer(vacancy).data)
    elif request.method == 'PUT':
        serializer = VacancySerializer(vacancy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        vacancy.delete()
        return Response(status=204)