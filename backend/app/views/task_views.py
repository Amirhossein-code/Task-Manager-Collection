from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Task
from ..serializers import TaskSerializer
from ..permissions import IsOwnerOrReadOnly
from ..filters import CategoryFilter


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def get_queryset(self):
        return Task.objects.filter(individual=self.request.user.individual).all()

    def perform_create(self, serializer):
        serializer.save(individual=self.request.user.individual)
