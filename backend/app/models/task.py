from django.db import models
from .individual import Individual
from .category import Category
# from .prequisite import Prequisite


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

    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name="task_individual"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=LOW)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    image = models.ImageField(upload_to="app/task/", null=True, blank=True)

    archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # def mark_all_prerequisites_completed(self):
    #     prerequisites = Prequisite.objects.filter(task=self)
    #     prerequisites.update(completed=True)
    #     for prerequisite in prerequisites:
    #         prerequisite.completed = True
    #         prerequisite.save()
    #     if prerequisites.filter(completed=False).exists() == False:
    #         self.completed = True
    #         self.save()

    # def mark_all_prerequisites_completed(self):
    #     try:
    #         prerequisites = Prequisite.objects.filter(task=self)
    #     except Prequisite.DoesNotExist:
    #         # exit the function sicne there are no prequisites
    #         # associated with the respective Task
    #         return

    #     prerequisites.update(completed=True)

    #     if prerequisites.filter(completed=False).exists():
    #         return

    #     self.completed = True
    #     self.save()

    def save(self, *args, **kwargs):
        if self.completed:
            # uncompleted_prerequisites = Prequisite.objects.filter(
            #     task=self, completed=False
            # )
            # if uncompleted_prerequisites.exists():
            #     raise ValueError(
            #         "Cannot mark this task as completed until all prerequisites are completed."
            #     )
            if not self.archived:
                self.archived = True
        super(Task, self).save(*args, **kwargs)
