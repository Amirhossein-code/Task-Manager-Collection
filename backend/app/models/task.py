from django.db import models
from .individual import Individual
from .category import Category


class Prequisite(models.Model):
    # Used for defining what need to be done beforehand for the task
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="task_prequisite"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    """
    # If we want to make prequisites Ordered so users can not move from the first uncompleted prequisite 
    # to mark the second one completed we can add this to the model and update the respective logic
    
    order = models.PositiveIntegerField()  

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if self.order > 1:
            previous_prerequisite = Prequisite.objects.filter(
                task=self.task, order=self.order - 1
            ).first()
            if previous_prerequisite and not previous_prerequisite.completed:
                raise ValueError(
                    "Cannot set this prerequisite to True until the previous one is completed."
                )
        super(Prequisite, self).save(*args, **kwargs)
    """


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

    def mark_all_prerequisites_completed(self):
        try:
            prerequisites = Prequisite.objects.filter(task=self)
        except Prequisite.DoesNotExist:
            # exit the function sicne there are no prequisites
            # associated with the respective Task
            return

        prerequisites.update(completed=True)

        if prerequisites.filter(completed=False).exists():
            return

        self.completed = True
        self.save()

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the instance already exists in the database
            if self.status == self.COMPLETED:
                uncompleted_prerequisites = Prequisite.objects.filter(
                    task=self, completed=False
                )
                if uncompleted_prerequisites.exists():
                    raise ValueError(
                        "Cannot mark this task as completed until all prerequisites are completed."
                    )
                if not self.archived:
                    self.archived = True
        super(Task, self).save(*args, **kwargs)
