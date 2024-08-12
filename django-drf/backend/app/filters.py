import django_filters
from .models import Task, Category


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            "title": ["exact"],
        }


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            "title": ["icontains"],
        }
