from rest_framework import serializers
from ..models import Individual


class UpdateIndividualSerializer(serializers.ModelSerializer):
    """
    For Updating Individual
    """

    class Meta:
        model = Individual
        fields = [
            "first_name",
            "last_name",
            "phone",
            "birth_date",
            "image",
        ]


class SimpleIndividualSerializer(serializers.ModelSerializer):
    """
    Simple Read_only serializer for Individual
    """

    class Meta:
        model = Individual
        fields = [
            "id",
            "first_name",
            "last_name",
        ]
        read_only_fields = [
            "id",
            "first_name",
            "last_name",
        ]


class IndividualSerializer(serializers.ModelSerializer):
    """
    For editing the User related fields use the user endpoint provided
    in this serializer we show some of the user relatred field sbut they are read_only
    this is detailed serialzer for updating individual use Updated Individual Serializer
    """

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
            "image",
        ]
        read_only_fields = [
            "id",
            "email",
            "joined_at",
            "last_updated",
        ]
