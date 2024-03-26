from ..models import user
from rest_framework import serializers


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def save(self, user):
        user.set_password(self.validated_data.get("password"))
        user.save()
