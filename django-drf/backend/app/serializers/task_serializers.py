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
        read_only_fields = ["__all__"]


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


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "start_time",
            "finish_time",
            "priority",
            "category",
        ]

    def validate(self, data):
        request = self.context["request"]
        start_time = data.get("start_time")
        finish_time = data.get("finish_time")
        category = data.get("category")

        # Validate start and finish time
        if start_time and finish_time and finish_time <= start_time:
            raise serializers.ValidationError(
                "Finish time must be later than start time."
            )

        # Validate if the category belongs to the authenticated user
        if category and category.individual != request.user.individual:
            raise serializers.ValidationError("You do not own this category.")

        return data
