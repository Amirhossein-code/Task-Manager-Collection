from rest_framework import serializers
from ..models import Prequisite


class PrequisiteSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Prequisite
        fields = [
            "id",
            "task",
            "title",
            "description",
            "completed",
            "created_at",
            "last_updated",
        ]
        read_only_fields = [
            "id",
            "task",  # ?
            "created_at",
            "last_updated",
        ]

    def create(self, validated_data):
        task_id = self.context["task_id"]
        if task_id is None:
            raise serializers.ValidationError("book slug is required in the context")

        validated_data["task_id"] = task_id
        return super().create(validated_data)
