
from rest_framework.exceptions import APIException


# 400 Bad Request
class InvalidRequestException(APIException):
    status_code = 400

    def __init__(self, detail=None, *args, **kwargs):
        detail = {
            "code": 40001,
            "message": "Invalid request",
            "result": detail if detail is not None else {"is_success": False}
        }

        super().__init__(detail=detail, *args, **kwargs)


class InvalidRequestBodyException(APIException):
    status_code = 400

    def __init__(self, detail=None, *args, **kwargs):
        detail = {
            "code": 40002,
            "message": "Invalid request body",
            "result": detail if detail is not None else {"is_success": False}
        }

        super().__init__(detail=detail, *args, **kwargs)


class MissingRequiredItemsException(APIException):
    status_code = 400
    default_detail = {
        "code": 40003,
        "message": "Missing Required Items",
        "result": {"is_success": False}
    }


class InvalidUsernameException(APIException):
    status_code = 400
    default_detail = {
        "code": 40004,
        "message": "Invalid username",
        "result": {"is_success": False}
    }


class InvalidPasswordException(APIException):
    status_code = 400
    default_detail = {
        "code": 40005,
        "message": "Invalid password",
        "result": {"is_success": False}
    }


class InvalidConfirmPasswordException(APIException):
    status_code = 400
    default_detail = {
        "code": 40006,
        "message": "Invalid confirm_password",
        "result": {"is_success": False}
    }


# 401 Unauthorized
class InvalidTokenException(APIException):
    status_code = 401

    def __init__(self, detail=None, *args, **kwargs):
        detail = {
            "code": 40301,
            "message": "Invalid token",
            "result": detail if detail is not None else {"is_success": False}
        }

        super().__init__(detail=detail, *args, **kwargs)


class TokenExpiredException(APIException):
    status_code = 401
    default_detail = {
        "code": 40102,
        "message": "Token is expired",
        "result": {"is_success": False}
    }


class FailedTokenDecodeException(APIException):
    status_code = 401
    default_detail = {
        "code": 40103,
        "message": "Token decode error",
        "result": {"is_success": False}
    }


# 403 Forbidden
class InactiveUserException(APIException):
    status_code = 403
    default_detail = {
        "code": 40301,
        "message": "User is inactive",
        "result": {"is_success": False}
    }


class InvalidHeaderException(APIException):
    status_code = 403
    default_detail = {
        "code": 40302,
        "message": "Invalid header",
        "result": {"is_success": False}
    }


# 404
class NotFoundUserException(APIException):
    status_code = 404
    default_detail = {
        "code": 40402,
        "message": "user not found",
        "result": {"is_success": False}
    }


# 500
class SSOServerErrorException(APIException):
    status_code = 500
    default_detail = {
        "code": 50001,
        "message": "SSO Server error",
        "result": {"is_success": False}
    }
