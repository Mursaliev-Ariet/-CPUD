from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    birth_date = models.DateField(null=True, verbose_name='Дата рождения')

    def __str__(self):
        return self.full_name


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255, verbose_name='Название компании')
    company_description = models.TextField(verbose_name='Описание компании')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    website = models.URLField(blank=True, verbose_name='Сайт')

    def __str__(self):
        return self.company_name


class Resume(models.Model):
    EMPLOYMENT_TYPES = [
        ('full_time', 'Полная занятость'),
        ('part_time', 'Частичная занятость'),
        ('remote', 'Удалённая работа'),
        ('internship', 'Стажировка'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='resumes',
        verbose_name='Сотрудник'
    )
    title = models.CharField(max_length=200, verbose_name='Желаемая должность')
    skills = models.TextField(verbose_name='Навыки')
    experience = models.TextField(verbose_name='Опыт работы')
    education = models.TextField(verbose_name='Образование')
    desired_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Желаемая зарплата'
    )
    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPES,
        default='full_time',
        verbose_name='Тип занятости'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    def __str__(self):
        return f"Резюме {self.employee.full_name} - {self.title}"


class Vacancy(models.Model):
    EMPLOYMENT_TYPES = [
        ('full_time', 'Полная занятость'),
        ('part_time', 'Частичная занятость'),
        ('remote', 'Удалённая работа'),
        ('internship', 'Стажировка'),
    ]

    EXPERIENCE_CHOICES = [
        ('no_exp', 'Без опыта'),
        ('1-3', '1-3 года'),
        ('5+', 'Более 5 лет'),
    ]

    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Работодатель'
    )
    title = models.CharField(max_length=200, verbose_name='Должность')
    description = models.TextField(verbose_name='Описание')
    requirements = models.TextField(verbose_name='Требования')
    salary_from = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Зарплата от'
    )
    salary_to = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Зарплата до'
    )
    location = models.CharField(max_length=255, verbose_name='Местоположение')
    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPES,
        default='full_time',
        verbose_name='Тип занятости'
    )
    experience_required = models.CharField(
        max_length=50,
        choices=EXPERIENCE_CHOICES,
        default='no_exp',
        verbose_name='Требуемый опыт'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f"{self.title} - {self.employer.company_name}"