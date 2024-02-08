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
        user = self.request.user
        if user.is_staff:  # Check if the user is an admin
            return Task.objects.all()
        else:
            return Task.objects.filter(user=user).all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
