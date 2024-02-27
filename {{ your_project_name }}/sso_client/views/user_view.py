from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView

from .common_view import make_response, check_token
from ..sso import *
from ..exception import *
from ..serializers.user_serializer import PasswordSerializer

User = get_user_model()


class SSOChangePasswordView(APIView):
    """
    사용자의 비밀번호를 변경하기 위한 API.
    토큰을 기반으로 사용자 정보를 확인한 뒤 비밀번호 변경.
    프로젝트 DB 내 비밀번호를 변경한 뒤 SSO로 동기화
    """

    @sync_with_sso
    @check_token
    def patch(self, request):
        user = request.user

        context = {"user": user}

        serializer = PasswordSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serialized_data = serializer.validated_data

            new_password = serialized_data.get("new_password")
            user.set_password(new_password)
            user.save()

            # SSO 동기화
            response = update_user_password_with_sso(user, serialized_data)

            if response.status_code == 200:
                return make_response(200, "Success Change Password", {}, status.HTTP_200_OK)
            else:
                handle_error_response(response)
        else:
            raise InvalidRequestBodyException(serializer.errors)

        return make_response(200, "Success Change Password", {}, status.HTTP_200_OK)
