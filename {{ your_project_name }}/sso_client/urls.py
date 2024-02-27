from django.urls import path

from .views.auth_view import *
from .views.user_view import *


urlpatterns = [
    path("login", LoginView.as_view(), name="login"),

    # path("token", TokenObtainView.as_view(), name="get_token"),
    path("token/refresh", TokenRefreshView.as_view(), name="refresh_token"),
    path("token/verify", TokenVerifyView.as_view(), name="verify_token"),

    path("info/password", SSOChangePasswordView.as_view(), name="change_password")
]
