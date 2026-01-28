from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        return None

    details = response.data
    message = "Validation error" if response.status_code == 400 else "Request failed"

    response.data = {
        "error": {
            "code": response.status_code,
            "message": message,
            "details": details,
        }
    }
    return response
