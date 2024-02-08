from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Task
from ..serializers import TaskSerializer
from ..permissions import IsOwnerOrReadOnly


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Check if the user is an admin
            return Task.objects.all()
        else:
            return Task.objects.filter(user=user).all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
