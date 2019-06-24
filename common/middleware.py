import logging
from django.core import exceptions
from django.http import Http404
from rest_framework import status
from rest_framework import exceptions as rest_exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)

def drf_custom_handler(exc, context):
    '''Custom DRF exception handler'''
    if isinstance(exc, (Http404, rest_exceptions.NotFound)):
        return Response({'error': 'NotFound'}, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, rest_exceptions.AuthenticationFailed):
        return Response({'error': 'Authentication Failed'}, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, exceptions.PermissionDenied):
        return Response({'error': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

    response = exception_handler(exc, context)

    if response:
        return response

    elif isinstance(exc, rest_exceptions.APIException):
        return Response({'error': exc.detail}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'error': 'InternalServerError',
        'error_description': 'An error occurred'
    }
    return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
