from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from ..serializers import (
    RequestPasswordResetSerializer,
)
from ..models import PasswordResetToken, User
from ..utils import send_reset_password_email


class RequestPasswordResetView(GenericAPIView):
    """
    When a registered user wants to set a new password,
    they first post their email. If the email is registered, a reset password
    link with a token is emailed to the user.
    """

    serializer_class = RequestPasswordResetSerializer
    permission_classes = [AllowAny]

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
