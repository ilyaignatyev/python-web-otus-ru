"""
Отправка email через очередь задач
"""

from datetime import datetime

import django_rq
from django.contrib.auth.models import User

from education_django.settings import EMAIL_HOST_USER
from .tasks import send_email


def send_email_async(from_user: User, message: str, theme: str):
    """
    Отправляет email на контактный email и всем суперпользователям.
    :param from_user: Текущий пользователь
    :param message: Сообщение
    :param theme: Тема
    """
    admin_emails = list(User.objects.filter(is_superuser=True, email__isnull=False).values_list('email', flat=True))
    message = f'Сообщение от пользователя {from_user.get_full_name()} (email: {from_user.email})\n-----\n{message}'
    theme = f'USER MESSAGE. {theme}'

    scheduler = django_rq.get_scheduler('emails')
    scheduler.enqueue_at(datetime.utcnow(), send_email, theme, message, EMAIL_HOST_USER,
                         [EMAIL_HOST_USER] + admin_emails)
