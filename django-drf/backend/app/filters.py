import django_filters
from django_filters import rest_framework as filters
from .models import Task, Category


class TaskFilter(django_filters.FilterSet):
    category = filters.CharFilter(field_name="category__title", lookup_expr="icontains")
    priority = filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES)

    class Meta:
        model = Task
        fields = {
            "title": ["icontains"],
            "priority": ["exact"],
            "status": ["exact"],
            "category": ["exact"],
        }


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            "title": ["icontains"],
        }
