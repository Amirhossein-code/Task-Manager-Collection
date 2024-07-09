from rest_framework import serializers
from ..models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            "id",
            "task",
            "title",
            "description",
            "resource_url",
            "resource_file",
            "created_at",
            "last_updated",
        ]
        read_only_fields = [
            "id",
            "task",
            "created_at",
            "last_updated",
        ]

    def create(self, validated_data):
        task_id = self.context["task_id"]
        if task_id is None:
            raise serializers.ValidationError("Task ID is required in the context")

        validated_data["task_id"] = task_id
        return super().create(validated_data)
