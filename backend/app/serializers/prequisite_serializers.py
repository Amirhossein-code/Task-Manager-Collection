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
