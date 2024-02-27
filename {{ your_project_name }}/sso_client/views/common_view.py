import os
import jwt
from functools import wraps

from rest_framework.response import Response

from django.contrib.auth import get_user_model

from ..exception import *

User = get_user_model()


def make_response(code, message, result, http_status):
    if not result:
        if http_status and 200 <= http_status < 300:
            result = {'is_success': True}
        else:
            result = {'is_success': False}

    response = Response({
        "code": int(code),
        "message": message,
        "result": result
    }, http_status
    )

    return response


def check_token(func):
    """
    JWT_SECRET_KEY를 통해 적절한 토큰인지 검증
    이후 decoding된 payload를 반환
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        jwt_secret_key = os.getenv("JWT_SECRET_KEY")

        if token:
            try:
                token_payload = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])

                user = User.objects.filter(username=token_payload['username']).first()
                if user is None:
                    raise NotFoundUserException()

                request.user = user

                return func(self, request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                raise TokenExpiredException()
            except jwt.DecodeError:
                raise FailedTokenDecodeException()
        else:
            raise InvalidTokenException()

    return wrapper
