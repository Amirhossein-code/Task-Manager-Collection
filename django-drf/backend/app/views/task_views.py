from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Task
from ..serializers import TaskSerializer, CreateTaskSerializer, DetailedTaskSerializer
from ..permissions import IsObjectOwner
from ..filters import TaskFilter


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]

    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTaskSerializer
        if self.action == "retrieve":
            return DetailedTaskSerializer
        return TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(individual=self.request.user.individual).all()

    def perform_create(self, serializer):
        serializer.save(individual=self.request.user.individual)
