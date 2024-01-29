from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    AbstractUser를 상속받아 Custom User model 정의.
    로그인 시 username 외 필드를 사용할 경우 USERNAME_FIELD를 수정.
    """
    name = models.CharField(blank=True, max_length=255, verbose_name="이름")
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    USERNAME_FIELD = 'username'
