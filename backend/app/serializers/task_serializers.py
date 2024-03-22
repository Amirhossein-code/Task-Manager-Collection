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
        ]
        read_only_fields = [
            "id",
        ]
