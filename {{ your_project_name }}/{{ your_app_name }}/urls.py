from django.urls import path, include
from .views import user_view


urlpatterns = [
    path("user", user_view.UserDetail.as_view()),
]
