from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        """
        주어진 이름, 비밀번호 등 개인정보로 User 인스턴를 생성한다.
        """
        if not username:
            raise ValueError('User must have username')

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        주어진 이름, 비밀번호 등 개인정보로 User 인스턴스를 생성한다.
        최상위 사용자이므로 권한을 부여한다.
        """
        user = self.create_user(
            username=username,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    기본 사용자 제어를 위한 모델로, AbstractBaseUser를 상속받는다.
    기본 속성으로 password, last_login, is_active를 보유한다.
    필요에 따라 username 필드를 email과 같은 필드로 대체할 수 있다.
    """
    username = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(default=timezone.now())

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['',]

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
        ordering = ('username', )

    def __str__(self):
        return self.username
