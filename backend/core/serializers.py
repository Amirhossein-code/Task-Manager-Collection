from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
        ]


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def save(self, user):
        user.set_password(self.validated_data.get("password"))
        user.save()
