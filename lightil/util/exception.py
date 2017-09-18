from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, NotAcceptable

def custom_exception_handler(exc, context):
    # Get the standard error response
    response = exception_handler(exc, context)

    if response is not None:
        response.data['detail'] = exc.detail

    return response

class ClientException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid request'
