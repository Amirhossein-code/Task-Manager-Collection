from rest_framework.permissions import BasePermission
from ..models import Prequisite


class IsOwnerOfPrequisite(BasePermission):
    message = "You must be the owner of this task or prequisite to access."

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user is the owner of the prequisite related to the task
        task_pk = view.kwargs.get("task_pk")
        prequisite_pk = view.kwargs.get(
            "pk"
        )  # Assuming 'pk' is the primary key of the Prequisite
        try:
            prequisite = Prequisite.objects.get(pk=prequisite_pk)
            return prequisite.task.individual == request.user.individual
        except Prequisite.DoesNotExist:
            return False
