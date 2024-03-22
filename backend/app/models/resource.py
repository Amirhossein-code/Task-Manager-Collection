from django.db import models
from .task import Task


class Resource(models.Model):
    """
    A resource maybe a file or a url to a website/weblog/video/...
    Or maybe the user want to save a file with the url of the website the file was downloaded

    So it can serve 3 types of resource handling
    file,url and both
    """

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="task_resource"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=True, null=True, blank=True)
    resource_file = models.FileField(upload_to="app/resources/", null=True, blank=True)

    # Charfield intentionallty used instead of Url field
    resource_url = models.CharField(max_length=555, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
