from django.db import models
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta
from .user import User


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timedelta(minutes=10)
        super(PasswordResetToken, self).save(*args, **kwargs)


"""
{
    "email": "12@gmail.com"
}
"""
