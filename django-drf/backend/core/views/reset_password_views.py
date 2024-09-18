from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import PasswordResetToken
from ..serializers import (
    ResetPasswordSerializer,
)


class ResetPasswordView(GenericAPIView):
    """
    After the user clicks on the url sent to their email
    they are redirected to an endpoint with the token avaiable in the url
    here we authenticate the token and ask the user to enter new password
    then we update the password and user can login with this password
    """

    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password")
        try:
            password_reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response("Invalid token", status=status.HTTP_400_BAD_REQUEST)
        if password_reset_token.expires_at < timezone.now():
            return Response("Token Expired", status=status.HTTP_400_BAD_REQUEST)

        user = password_reset_token.user
        user.set_password(password)
        user.save()

        password_reset_token.delete()

        return Response("Password reset successful", status=status.HTTP_200_OK)
