from django.db import models
from autoslug import AutoSlugField
from django.conf import settings


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=355)
    slug = AutoSlugField(populate_from="title", unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "2. Categories"
