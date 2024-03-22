from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Category
from ..serializers import CategorySerializer
from ..permissions import IsObjectOwner
from ..filters import CategoryFilter


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]

    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def get_queryset(self):
        return Category.objects.filter(individual=self.request.user.individual).all()

    def perform_create(self, serializer):
        serializer.save(individual=self.request.user.individual)
