from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordResetToken


def send_reset_password_email(email, token):
    reset_password_link = f"{settings.FRONTEND_URL}/reset-password/{token}"
    send_mail(
        "Password Reset",
        f"Click the link to reset your password: {reset_password_link}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
