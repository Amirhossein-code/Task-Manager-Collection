from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Category
from ..serializers import CategorySerializer
from ..permissions import IsOwnerOrReadOnly
from ..filters import TaskFilter


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Check if the user is an admin
            return Category.objects.all()
        else:
            return Category.objects.filter(user=user).all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
