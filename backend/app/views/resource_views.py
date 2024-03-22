from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..models import Resource
from ..serializers import ResourceSerializer
from ..permissions import IsOwnerOfTaskForeignModels


class ResourceViewSet(ModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfTaskForeignModels]

    def get_queryset(self):
        return Resource.objects.filter(
            task__id=self.kwargs["task_pk"],
            task__individual=self.request.user.individual,
        ).all()

    def get_serializer_context(self):
        return {"task_id": self.kwargs["task_pk"]}
