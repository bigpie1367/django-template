from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """
    로그인을 위한 Serializer
    request body, 누락 데이터, 유저 조회 등 일련의 절차 수행
    """

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username")

        # username과 일치하는 사용자가 있는 경우
        # password를 비교하여 일치하지 않을 경우
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        # 유저가 비활성화 상태일 경우
        if not user.is_active:
            raise serializers.ValidationError("Inactive user")

        return attrs
