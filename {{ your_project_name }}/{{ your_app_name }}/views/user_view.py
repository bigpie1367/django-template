from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView

from .common_view import make_response
from ..serializers.user_serializer import UserSerializer

User = get_user_model()


class GetUserInfoView(APIView):
    """
    사용자 정보를 조회하기 위한 API.
    Access Token을 기반으로 해당 사용자의 정보 조회.
    """

    @check_token
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        return make_response(200, "Success get info", user_data, status.HTTP_200_OK)
