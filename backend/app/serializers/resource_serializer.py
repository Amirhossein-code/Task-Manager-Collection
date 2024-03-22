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
            "resource_file",
            "resource_url",
            "created_at",
            "last_updated",
        ]
        read_only_fields = [
            "id",
            "task",  # ?
            "created_at",
            "last_updated",
        ]
