from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView

from .common_view import make_response, handle_error_response, check_token
from ..sso import (
    sync_with_sso, get_token_from_sso, verify_token_from_sso, refresh_token_from_sso
)
from ..exception import *
from ..serializers.auth_serializer import LoginSerializer

User = get_user_model()


@check_token
def login_with_token(self, request):
    user = request.user
    if user:        # 정상적인 사용자일 경우
        return user
    else:           # 부적절한 사용자일 경우
        raise NotFoundUserException()


class LoginView(APIView):
    """
    사용자 로그인을 위해 사용하는 API.
    SSO 기능 구현을 위해 최초 API 호출 시 토큰 유무 확인.
    API를 호출할 때 SSO와 사용자 정보 동기화 진행

    토큰 보유
    > JWT_SECRET_KEY를 통해 토큰 인증
    > 적합한 토큰일 시 Django Session을 통한 로그인
    > 만료 or 부적절한 토큰일 시 오류 발생

    토큰 미보유
    > username, password 정보와 일치하는 사용자 조회
    > 사용자가 존재할 경우 SSO로부터 토큰 발급
    """

    @sync_with_sso
    def post(self, request):
        # 토큰이 존재할 경우 check_token 데코레이터를 통해 토큰 디코드 & 로그인
        token = request.META.get("HTTP_AUTHORIZATION")
        if token is not None:
            user = login_with_token(self, request)
            # login(user)

            return make_response(200, "Success Login", {}, status.HTTP_200_OK)

        # 토큰이 존재하지 않을 시 로그인 진행
        # Serializer로부터 정상적으로 데이터가 반환되었을 경우 토큰 발급
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=False):
            validated_data = serializer.validated_data
            username = validated_data.get("username")
            password = validated_data.get("password")
        else:
            raise InvalidRequestBodyException(serializer.errors)

        try:
            response = get_token_from_sso(username, password)
        except Exception:
            raise SSOServerErrorException()

        if response.status_code == 200:
            access_token = response.json().get("access")
            refresh_token = response.json().get("refresh")

            tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return make_response(200, "Success Login", tokens, status.HTTP_200_OK)
        else:
            handle_error_response(response)


class TokenRefreshView(APIView):
    """
    SSO 서버로부터 토큰을 재발급하기 위한 API.
    request body의 "refresh" 데이터를 기반으로 토큰 재발급 진행.
    재발급에 사용한 Refresh Token은 발급 이후 블랙리스트에 등록됨.
    """

    def post(self, request):
        refresh_token = request.data.get("refresh_token", None)

        if refresh_token is None:
            raise MissingRequiredItemsException()

        try:
            response = refresh_token_from_sso(refresh_token)
        except Exception:
            raise SSOServerErrorException()

        if response.status_code == 200:
            access_token = response.json().get("access")
            refresh_token = response.json().get("refresh")

            tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            response = make_response(200, "Success Refresh Token", tokens, status.HTTP_200_OK)
            return response
        else:
            handle_error_response(response)


class TokenVerifyView(APIView):
    """
    SSO 서버로부터 토큰을 검증하기 위한 API.
    request body의 "token" 데이터를 기반으로 토큰 검증 진행.
    """

    def post(self, request):
        token = request.data.get("token", None)
        if token is None:
            raise MissingRequiredItemsException()

        try:
            response = verify_token_from_sso(token)
        except Exception:
            raise SSOServerErrorException()

        if response.status_code == 200:
            return make_response(200, "Valid token", {}, status.HTTP_200_OK)
        else:
            handle_error_response(response)
