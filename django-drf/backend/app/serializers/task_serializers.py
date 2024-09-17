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
        ]
        read_only_fields = [
            "id",
        ]
