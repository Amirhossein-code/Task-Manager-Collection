from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(null=True, blank=True, max_length=20)
    birth_date = models.DateField(null=True, blank=True, editable=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
