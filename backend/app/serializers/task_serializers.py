from rest_framework import serializers
from ..models import Task


class DetailedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "individual",
            "start_time",
            "finish_time",
            "priority",
            "status",
            "category",
            "image",
            "archived",
            "created_at",
            "last_updated",
        ]
        read_only_fields = [
            "id",
            "individual",
            "created_at",
            "last_updated",
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "category",
            "start_time",
            "finish_time",
            "archived",
        ]
        read_only_fields = [
            "id",
        ]


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "category",
            "start_time",
            "finish_time",
            "image",
        ]
        read_only_fields = [
            "id",
        ]


# 1@gmail.com

# LLL909055
