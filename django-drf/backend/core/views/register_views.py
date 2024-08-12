from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from ..serializers import (
    UserSerializer,
)


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance  # Get the newly created user instance
        serialized_user = UserSerializer(user)  # Serialize the user instance

        return Response(serialized_user.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = serializer.save()
        password = serializer.validated_data.get("password")
        user.set_password(password)
        user.save()
