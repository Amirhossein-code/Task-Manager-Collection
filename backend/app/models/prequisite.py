from django.db import models
from .task import Task


class Prequisite(models.Model):
    # Used for defining what need to be done beforehand for the task
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="task_prequisite"
    )
    title = models.CharField(max_length=True)
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
