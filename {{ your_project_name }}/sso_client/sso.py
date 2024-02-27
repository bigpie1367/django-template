
import requests
import environ
from functools import wraps

from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .exception import *
from .views.common_view import handle_error_response

from {{ your_app_name }}.models import Department, Grade

User = get_user_model()
env = environ.Env()

SSO_URL = env("SSO_URL")
CLIENT_KEY = env("CLIENT_KEY")


def get_token_from_sso(username, password):
    """
    username, password를 매개변수로 받아 SSO 서버로 요청
    SSO 서버는 DB 내 사용자를 검증한 뒤 Token 발행
    """
    target_url = f"{SSO_URL}/auth/token"

    headers = {"CLIENT-KEY": CLIENT_KEY}

    body = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(target_url, headers=headers, json=body)
        return response
    except Exception:
        raise SSOServerErrorException()


def refresh_token_from_sso(refresh_token):
    """
    refresh_token을 매개변수로 받아 SSO 서버로 토큰 재발급 요청.
    """
    target_url = f"{SSO_URL}/auth/token/refresh"

    headers = {"CLIENT-KEY": CLIENT_KEY}

    body = {
        "refresh": refresh_token
    }

    try:
        response = requests.post(target_url, headers=headers, json=body)
        return response
    except Exception:
        raise SSOServerErrorException()


def verify_token_from_sso(token):
    """
    token을 매개변수로 받아 SSO 서버로 토큰 검증 요청.
    """
    target_url = f"{SSO_URL}/auth/token/verify"

    headers = {"CLIENT-KEY": CLIENT_KEY}

    body = {
        "token": token
    }

    try:
        response = requests.post(target_url, headers=headers, json=body)
        return response
    except Exception:
        raise SSOServerErrorException()


def sync_with_sso(func):
    """
    SSO 서버로부터 모든 사용자 데이터를 가져와 프로젝트 내 유저 모델을 업데이트
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if args and isinstance(args[0], HttpRequest):
            request = args[0]

        # SSO 서버의 사용자 목록을 가져오는 API endpoint
        target_url = f"{SSO_URL}/user"

        headers = {"CLIENT-KEY": CLIENT_KEY}

        try:
            # SSO 서버로부터 사용자 목록을 가져옴
            response = requests.get(target_url, headers=headers)
            sso_users = response.json()["result"]

            # 내 유저 모델에 SSO 서버에서 가져온 사용자 데이터 업데이트
            for sso_user in sso_users:
                username = sso_user.get('username')

                # 사용자가 이미 존재하는지 확인하고 생성 또는 업데이트
                user, created = User.objects.get_or_create(
                    username=username
                )

                # 사용자 모델의 모든 필드에 대해 자동으로 setattr로 값을 업데이트
                for field, value in sso_user.items():
                    if hasattr(user, field):
                        if field == "department":
                            department = Department.objects.get(display_name=value)
                            user.department_id = department
                        elif field == "grade":
                            grade = Grade.objects.get(display_name=value)
                            user.grade_id = grade
                        else:
                            setattr(user, field, value)

                user.save()

        except requests.exceptions.RequestException:
            raise SSOServerErrorException()

        return func(*args, **kwargs)

    return wrapper


def update_user_password_with_sso(user, data):
    """
    token을 매개변수로 받아 SSO 서버로 토큰 검증 요청.
    """
    target_url = f"{SSO_URL}/user/password"

    headers = {"CLIENT-KEY": CLIENT_KEY}

    body = {
        "user": user.username,
        "current_password": data.get("current_password"),
        "new_password": data.get("new_password"),
        "confirm_password": data.get("confirm_password")
    }

    try:
        response = requests.patch(target_url, headers=headers, json=body)
    except Exception:
        raise SSOServerErrorException()

    if response.status_code == 200:
        return response
    else:
        handle_error_response(response)
