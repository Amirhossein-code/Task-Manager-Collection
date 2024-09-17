from django.core.exceptions import ValidationError
from django.db import models

from .category import Category
from individual.models import Individual


class Task(models.Model):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    PRIORITY_CHOICES = [
        (LOW, "low"),
        (MEDIUM, "medium"),
        (HIGH, "high"),
    ]

    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    POSTPONED = "Postponed"

    STATUS_CHOICES = [
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (POSTPONED, "Postponed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=LOW)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS
    )

    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name="task_individual"
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()  # Call the parent's clean method
        if self.start_time and self.finish_time and self.finish_time <= self.start_time:
            raise ValidationError("Finish time must be later than start time.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure that clean is called before saving
        super(Task, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Tasks"
