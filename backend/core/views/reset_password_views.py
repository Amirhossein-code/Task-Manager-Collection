from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from ..models import User
from ..serializers import (
    ResetPasswordSerializer,
)
from ..models import PasswordResetToken


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
