from rest_framework import serializers
from .models import Individual


class UpdateIndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = [
            "first_name",
            "last_name",
            "phone",
            "birth_date",
        ]


class IndividualSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Individual
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "phone",
            "joined_at",
            "last_updated",
        ]
        read_only_fields = [
            "id",
            "email",
            "joined_at",
            "last_updated",
        ]
