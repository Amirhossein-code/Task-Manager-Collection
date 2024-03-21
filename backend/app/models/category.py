from django.db import models
from autoslug import AutoSlugField
from .individual import Individual


class Category(models.Model):
    # Used for categorizing tasks
    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name="task_individual"
    )
    title = models.CharField(max_length=355)
    slug = AutoSlugField(populate_from="title", unique=True, null=True, blank=True)
    image = models.ImageField(upload_to="/app/category", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "2. Categories"
