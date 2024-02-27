from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView

from sso_client.sso import sync_with_sso
from sso_client.views.common_view import check_token
from sso_client.views.user_view import SSOChangePasswordView

from .common_view import make_response
from ..serializers.user_serializer import UserSerializer

User = get_user_model()


class GetUserInfoView(APIView):
    """
    사용자 정보를 조회하기 위한 API.
    Access Token을 기반으로 해당 사용자의 정보 조회.
    """

    @sync_with_sso
    @check_token
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        return make_response(200, "Success get info", user_data, status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    사용자의 비밀번호를 변경하기 위한 API.
    Access Token을 기반으로 사용자 정보 조회 후 비밀번호 변경.
    별도의 추가기능이 없어 SSO Client에 정의된 ChangePasswordSSOView 사용.
    """

    def patch(self, request):
        sso_change_password_view = SSOChangePasswordView()

        response = sso_change_password_view.patch(request)
        return response
