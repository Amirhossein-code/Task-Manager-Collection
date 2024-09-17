from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = "User"
