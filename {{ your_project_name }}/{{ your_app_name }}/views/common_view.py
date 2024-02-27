from rest_framework.response import Response


def make_response(code, message, result, http_status):
    return Response({
        "code": int(code),
        "message": message,
        "result": result
    }, http_status
    )
