from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "individual",
            "title",
            "slug",
            "image",
        ]
        read_only_fields = [
            "id",
            "individual",
            "slug",
        ]
