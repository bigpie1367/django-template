from django.http import Http404
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotAuthenticated


class ExceptionHandlingStrategy:
    @staticmethod
    def handle(exc, context, response):
        raise NotImplementedError(
            "Each strategy must implement a handle method")


# 400 Bad Request
class ValidationErrorHandlingStrategy(ExceptionHandlingStrategy):
    @staticmethod
    def handle(exc, context, response):
        response.data = {
            'error': 'Validation Error',
            'error_message': 'Validation Error',
        }
        response.status_code = 400
        response.data['detail'] = exc.__dict__['detail']
        return response


# 403 Not Authenticated
class NotAuthenticatedHandlingStrategy(ExceptionHandlingStrategy):
    @staticmethod
    def handle(exc, context, response):
        response.data = {
            'error': 'Not Authenticated',
            'error_message': 'NotAuthenticated',
        }

        response.status_code = 403
        return response


class JWTExpiredHandlingStrategy(ExceptionHandlingStrategy):
    @staticmethod
    def handle(exc, context, response):
        response.data = {
            'error': 'Token Expired',
            'error_message': 'Your token has expired.',
        }
        response.status_code = 403

        return response


class JWTInvalidHandlingStrategy(ExceptionHandlingStrategy):
    @staticmethod
    def handle(exc, context, response):
        response.data = {
            'error': 'Token Invalid',
            'error_message': 'Your token Invalid.',
        }

        response.status_code = 403
        return response


# 404 Not Found
class NotFoundHandlingStrategy(ExceptionHandlingStrategy):
    @staticmethod
    def handle(exc, context, response):
        response.data = {
            'error': 'Not Found',
            'error_message': 'The requested resource was not found',
        }

        response.status_code = 404
        return response


# 500 Internal Server Error
class ServerErrorHandlingStrategy(ExceptionHandlingStrategy):
    @staticmethod
    def handle(exc, context, response):
        response = Response()
        response.data = {
            'error': 'ServerError',
            'error_message': 'Internal Server Error',
        }

        response.status_code = 500
        response.data['body'] = str(exc)
        return response


class ExceptionHandlingStrategyFactory:
    """
    발생한 Exception과 이를 처리할 전략을 매핑하기 위함.
    매핑되는 전략이 없을 경우 500(Internal Server Error) 처리.
    필요에 따라 상기 Class와 같이 예외 처리를 위한 Class 구현.
    """

    strategy_map = {
        ValidationError: ValidationErrorHandlingStrategy,
        NotAuthenticated: NotAuthenticatedHandlingStrategy,
        InvalidToken: JWTInvalidHandlingStrategy,
        Http404: NotFoundHandlingStrategy,
    }

    @staticmethod
    def get_strategy(exc, response):
        print("exc : ", exc, type(exc))
        strategy = ExceptionHandlingStrategyFactory.strategy_map.get(type(exc))
        if not strategy and (not response or response.status_code == 500):
            strategy = ServerErrorHandlingStrategy

        return strategy


def handle_exception(exc, context):
    response = exception_handler(exc, context)

    strategy = ExceptionHandlingStrategyFactory.get_strategy(exc, response)
    if strategy:
        return strategy.handle(exc, context, response)

    return response
