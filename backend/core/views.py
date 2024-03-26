from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from django.utils import timezone
from .models import User
from .serializers import (
    UserSerializer,
    RequestPasswordResetSerializer,
    ResetPasswordSerializer,
)
from .models import PasswordResetToken
from .utils import send_reset_password_email


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response("User registered successfully", status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = serializer.save()
        password = serializer.validated_data.get("password")
        user.set_password(password)
        user.save()


class PasswordResetRequestView(GenericAPIView):
    """
    When a registered user wants to set a new password because the old one is forgotten,
    they first post their email. If the email is registered, a reset password
    link with a token is emailed to the user.
    """

    serializer_class = RequestPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("User with the given email not found")

        token = PasswordResetToken.objects.create(user=user)
        send_reset_password_email(email, token.token)

        return Response(
            "Password reset link sent successfully. Check your email.",
            status=status.HTTP_200_OK,
        )



class ResetPasswordView(APIView):
    """
    After the user clicks on the url sent to their email
    they are redirected to an endpoint with the token avaiable in the url
    here we authenticate the token and ask the user to enter new password
    then we update the password and user can login with this password
    """

    def post(self, request, token):
        try:
            password_reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response("Invalid token", status=status.HTTP_400_BAD_REQUEST)
        if password_reset_token.expires_at < timezone.now:
            return Response("Token Expired")

        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = password_reset_token.user
            user.set_password(serializer.validated_data.get("password"))
            user.save()
            password_reset_token.delete()
            return Response("Password reset successfully", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
