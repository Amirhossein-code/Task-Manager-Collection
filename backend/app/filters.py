import django_filters
from .models import Task, Category


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            "title": ["exact"],
            "category": ["exact"],
            "category__title": ["icontains"],
            "due_date": [
                "exact",
                "gte",
                "lte",
            ],  # exact, greater than or equal, less than or equal
            "priority": ["exact"],
        }


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            "title": ["icontains"],
        }
