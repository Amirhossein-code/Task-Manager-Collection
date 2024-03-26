from ..models import user
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = user
        fields = [
            "id",
            "email",
            "password",
        ]
