from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Vacancy, Resume
from .telegram_utils import send_telegram_message_with_button

@receiver(post_save, sender=Vacancy)
def vacancy_created_notification(sender, instance, created, **kwargs):
    if created:
        company = instance.employer.company_name if instance.employer else "Не указана"
        description = (instance.description or '')[:200]
        phone = (instance.employer.phone or '')[:200]
        message = f"""
<b>📢 Новая вакансия!</b>

<b>📌 Должность:</b> {instance.title}
<b>🏢 Компания:</b> {company}
<b>💰 Зарплата:</b> от {instance.salary_from} до {instance.salary_to} ₽
<b>📍 Город:</b> {instance.location}

<b>📝 Описание:</b>
<b>📞 Связаться:</b> {phone}
{description}
        """
        send_telegram_message_with_button(
            text=message,
            button_text="Подробнее",
            button_url=f"https://ваш-сайт.ру/vacancy/{instance.id}/",
            chat_id=settings.CHAT_ID_VACANCY
        )

@receiver(post_save, sender=Resume)
def resume_created_notification(sender, instance, created, **kwargs):
    if created:
        full_name = instance.employee.full_name if instance.employee else "Не указан"
        skills = (instance.skills or '')[:200]
        experience = (instance.experience or '')[:200]
        phone = (instance.employee.phone or '')[:200]
        message = f"""
<b>📄 Новое резюме!</b>

<b>📌 Желаемая должность:</b> {instance.title}
<b>👤 Сотрудник:</b> {full_name}
<b>💰 Желаемая зарплата:</b> {instance.desired_salary} ₽
<b>📋 Навыки:</b> {skills}
<b>📝 Опыт:</b> {experience}
<b>📞 Связаться:</b> {phone}
        """
        send_telegram_message_with_button(
            text=message,
            button_text="🔗 Подробнее",
            button_url=f"https://ваш-сайт.ру/resume/{instance.id}/",
            chat_id=settings.CHAT_ID_RESUME
        )