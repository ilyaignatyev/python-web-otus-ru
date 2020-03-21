"""
Задачи
"""

import logging

from django.core.mail import send_mail
from django_rq import job


@job('emails')
def send_email(theme: str, message: str, from_email: str, emails: list):
    """
    Отправляет email
    :param theme: Тема
    :param message: Сообщение
    :param from_email: От кого
    :param emails: Список адресатов
    """
    try:
        send_mail(theme, message, from_email, emails, fail_silently=False)
    except Exception as ex:
        logger = logging.getLogger('education_app.send_email')
        logger.error(f'Error while sending email: theme: {theme}, message: {message}, from_email: {from_email}, '
                     f'emails: {emails}, ERROR: {str(ex)}')
