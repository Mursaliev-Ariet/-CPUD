from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Employee, Employer, Resume, Vacancy

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['user']

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'
        read_only_fields = ['user']

class ResumeSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['employee', 'created_at']

class VacancySerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='employer.company_name', read_only=True)

    class Meta:
        model = Vacancy
        fields = '__all__'
        read_only_fields = ['employer', 'created_at']

# регистрация
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=['employee', 'employer'], write_only=True)

    full_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)

    company_name = serializers.CharField(required=False, allow_blank=True)
    company_description = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    website = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role',
                  'full_name', 'phone', 'city',
                  'company_name', 'company_description', 'address', 'website']

    def validate(self, data):
        role = data.get('role')
        if role == 'employee':
            if not data.get('full_name'):
                raise serializers.ValidationError({'full_name': 'Это поле обязательно для сотрудника'})
            if not data.get('phone'):
                raise serializers.ValidationError({'phone': 'Это поле обязательно для сотрудника'})
            if data.get('company_name') or data.get('company_description') or data.get('address') or data.get('website'):
                data.pop('company_name', None)
                data.pop('company_description', None)
                data.pop('address', None)
                data.pop('website', None)
        elif role == 'employer':
            if not data.get('company_name'):
                raise serializers.ValidationError({'company_name': 'Это поле обязательно для работодателя'})
            if not data.get('phone'):
                raise serializers.ValidationError({'phone': 'Это поле обязательно для работодателя'})
            if not data.get('address'):
                raise serializers.ValidationError({'address': 'Это поле обязательно для работодателя'})
            if not data.get('full_name'):
                raise serializers.ValidationError({'full_name': 'Это поле обязательно для работодателя'})
            if not data.get('city'):
                raise serializers.ValidationError({'city': 'Это поле обязательно для работодателя'})
        else:
            raise serializers.ValidationError({'role': 'Неверная роль'})
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        email = validated_data.get('email', '')
        username = validated_data.get('username', email.split('@')[0])

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data.pop('password')
        )

        if role == 'employee':
            Employee.objects.create(
                user=user,
                full_name=validated_data.get('full_name', ''),
                phone=validated_data.get('phone', ''),
                email=email,
            )
        elif role == 'employer':
            Employer.objects.create(
                user=user,
                company_name=validated_data.get('company_name', ''),
                company_description=validated_data.get('company_description', ''),
                phone=validated_data.get('phone', ''),
                email=email,
                address=validated_data.get('address', ''),
                city=validated_data.get('city', ''),
                full_name=validated_data.get('full_name', ''),
                website=validated_data.get('website', '')
            )

        return user

# выбор роли
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        requested_role = attrs.get('role')

        if not email or not password:
            raise serializers.ValidationError('Email и пароль обязательны')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь с таким email не найден')

        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')

        # Проверка роли
        if requested_role:
            if requested_role == 'employee' and not hasattr(user, 'employee_profile'):
                raise serializers.ValidationError('Вы не зарегистрированы как сотрудник')
            if requested_role == 'employer' and not hasattr(user, 'employer_profile'):
                raise serializers.ValidationError('Вы не зарегистрированы как работодатель')
            final_role = requested_role
        else:
            final_role = 'employee' if hasattr(user, 'employee_profile') else 'employer'

        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': final_role
        }