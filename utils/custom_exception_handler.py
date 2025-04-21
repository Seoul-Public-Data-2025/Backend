from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        message = response.data.get('detail') \
                  or response.data.get('message') \
                  or str(response.data)

        response.data = {
            'success': False,
            'message': message
        }
    else:
        response = Response({
            'success': False,
            'message': str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
