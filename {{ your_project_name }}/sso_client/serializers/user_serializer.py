from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User 객체를 json 형태로 반환하기위한 Serializer
    """

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'password', 'fullname', 'email', 'birth',
            'phone', 'department', 'grade'
        ]


class PasswordSerializer(serializers.Serializer):
    """
    비밀번호 변경을 위한 Serializer
    """

    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # 변경할 비밀번호 일치여부 확인
        if new_password != confirm_password:
            raise serializers.ValidationError('Invalid confirm password')

        user = self.context.get("user")

        if not user.check_password(current_password):
            raise serializers.ValidationError('Invalid password')

        return attrs
