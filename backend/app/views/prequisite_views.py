from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..models import Prequisite
from ..serializers import PrequisiteSerialzier
from ..permissions import IsOwnerOfPrequisite


class PrequisiteViewSet(ModelViewSet):
    serializer_class = PrequisiteSerialzier
    permission_classes = [IsOwnerOfPrequisite]

    def get_queryset(self):
        return Prequisite.objects.filter(
            task__id=self.kwargs["task_pk"],
            # task__individual=self.request.user.individual,
        ).all()

    def get_serializer_context(self):
        return {"task_id": self.kwargs["task_pk"]}
