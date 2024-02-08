from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        ]

    def validate(self, attrs):
        """
        Make sure no one registers
        """
        raise serializers.ValidationError("Registration is closed.")


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]


class SecureUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "username",
            "first_name",
            "last_name",
        ]


# Note for adding additional fields for user creation
# we should not support fields outside the user model here like the fields in author model
# but if that is the case and we want to we should do so in the front end
# how? first post the details related to User model then additional fields in another post method
# for adding fields here they need to be redefiened which is not a good practice
# So we are going to pay the cost of sending 2 calls to the endpoint to have perfectly set up end points that do not interfere with each other
