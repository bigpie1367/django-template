"""
SSO User, Department, Grade를 위한 모델 파일
SSO 서버를 사용할 경우 실제 사용할 프로젝트의 models.py에 추가
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    """
    User 테이블 department에 매핑
    """
    identifier = models.CharField(
        max_length=10,
        verbose_name="부서식별자"
    )
    display_name = models.CharField(
        max_length=10,
        verbose_name="부서명"
    )

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = "부서"


class Grade(models.Model):
    """
    User 테이블 Grade에 매핑
    """
    identifier = models.CharField(
        max_length=10,
        verbose_name="직급식별자"
    )
    display_name = models.CharField(
        max_length=10,
        verbose_name="직급명"
    )

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = "직급"


class User(AbstractUser):
    """
    AbstractUser를 상속받아 Custom User model 정의.
    기록인 시 username 외 필드를 사용할 경우 USERNAME_FIELD를 수정.
    first_name, last_name 필드 각각이 아닌 name 이라는 필드로 통합관리.
    상세 속성은 migrations/0001_initial.py 내에서 확인 가능.
    """

    first_name = None  # type: ignore
    last_name = None  # type: ignore

    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="ID"
    )
    fullname = models.CharField(
        max_length=255,
        verbose_name="이름"
    )
    email = models.EmailField(
        max_length=50,
        verbose_name="이메일"
    )
    birth = models.CharField(
        max_length=50,
        verbose_name="생년월일"
    )
    phone = models.CharField(
        max_length=30,
        null=True,
        verbose_name="전화번호"
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL,
        null=True, verbose_name="부서"
    )
    grade = models.ForeignKey(
        Grade, on_delete=models.SET_NULL,
        null=True, verbose_name="직급"
    )

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "사용자"
