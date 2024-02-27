from django.urls import path
from .views import *


urlpatterns = [
    path("info", GetUserInfoView.as_view(), name="get_info"),
    path("info/password", ChangePasswordView.as_view(), name="change_password")
]
