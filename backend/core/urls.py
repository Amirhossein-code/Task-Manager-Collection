from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "reset-password/",
        views.PasswordResetRequestView.as_view(),
        name="reset-password",
    ),
    path(
        "reset-password/<uuid:token>/",
        views.ResetPasswordView.as_view(),
        name="reset-password-confirm",
    ),
]
