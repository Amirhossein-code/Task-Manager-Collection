from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "user",
            "title",
            "slug",
        ]
        read_only_fields = ["user"]
