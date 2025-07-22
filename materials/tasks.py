from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from users.models import User


@shared_task
def send_inform_about_update_course(email):
    """Отправляется сообщение студенту о том, что курс обновлен."""
    send_mail("Новое обновление", "Курс обновлен", EMAIL_HOST_USER, [email])


@shared_task()
def is_active_login():
    today = timezone.now().today().date()
    users = User.objects.filter(
        last_login__isnull=False, last_login__lt=today - timezone.timedelta(days=30)
    )
    if users:
        for user in users:
            user.is_active = False
