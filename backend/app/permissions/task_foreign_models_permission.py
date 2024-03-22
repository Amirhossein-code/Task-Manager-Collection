from rest_framework.permissions import BasePermission
from ..models import Task


class IsOwnerOfTaskForeignModels(BasePermission):
    message = "You must be the owner of this task or prequisite to access."

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the prequisite related to the task
        return obj.task.individual == request.user.individual
