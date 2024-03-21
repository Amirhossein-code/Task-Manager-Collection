from django.db import models
from django.conf import settings
from .category import Category


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
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=LOW)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
