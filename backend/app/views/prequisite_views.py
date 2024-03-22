from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..models import Prequisite
from ..serializers import PrequisiteSerialzier


class PrequisiteViewSet(ModelViewSet):
    serializer_class = PrequisiteSerialzier
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Prequisite.objects.filter(task__id=self.kwargs["task_pk"]).all()

    def get_serializer_context(self):
        return {"task_id": self.kwargs["task_pk"]}
