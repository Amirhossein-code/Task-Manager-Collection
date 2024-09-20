from django.conf import settings
from django.db import models


class Individual(models.Model):
    # User profile: used to store data about the user not required for authentication
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Extra User Data
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True, editable=True)

    phone = models.CharField(max_length=20, null=True, blank=True)

    # Time Stamps
    joined_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Individual"
