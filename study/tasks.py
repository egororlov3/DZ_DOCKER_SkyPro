from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

User = get_user_model()


@shared_task
def send_subscription_confirmation_email(user_email, course_title):
    subject = f"Подтверждение подписки на курс: {course_title}"
    message = f"Здравствуйте! Вы подписались на обновления курса '{course_title}'. Вы будете получать уведомления об изменениях материалов."
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)


@shared_task
def send_unsubscribe_confirmation_email(user_email, course_title):
    subject = f"Вы отписались от курса: {course_title}"
    message = f"Здравствуйте! Вы успешно отписались от обновлений курса '{course_title}'."
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)


@shared_task
def deactivate_inactive_users():
    # Получаем текущую дату
    now = timezone.now()
    # Вычисляем дату, когда пользователь должен был зайти
    inactive_since = now - timedelta(days=30)

    # Получаем всех пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(last_login__lt=inactive_since, is_active=True)

    # Деактивируем их
    inactive_users.update(is_active=False)

    return f'Deactivated {inactive_users.count()} users.'
