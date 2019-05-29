from django.core import exceptions
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    '''Custom exception handler'''

    if isinstance(exc, Http404):
        return Response({'error': 'NotFound'}, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, exceptions.PermissionDenied):
        return Response({'error': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

    elif isinstance(exc, APIException):
        return Response({'error': exc.detail}, status=status.HTTP_400_BAD_REQUEST)

    response = exception_handler(exc, context)

    if response:

        return response

    data = {
        'error': 'InternalServerError',
        'error_description': 'An error occurred'
    }

    return Response(data=data, status=exc.status_code)
