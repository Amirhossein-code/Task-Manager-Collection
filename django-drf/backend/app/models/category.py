from django.db import models
from individual.models import Individual


class Category(models.Model):
    # Used for categorizing tasks
    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name="task_category"
    )
    title = models.CharField(max_length=355)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "2. Categories"
