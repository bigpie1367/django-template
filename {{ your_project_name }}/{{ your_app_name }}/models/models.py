from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# 기본 사용자 제어를 위한 모델로, AbstractBaseUser를 상속한다
# 기본 속성 : password, last_login, is_active
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)

    USERNAME_FIELD = 'username'
