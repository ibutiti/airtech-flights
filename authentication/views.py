from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import User
from authentication.serializers import UserSignUpSerializer


class UserSignUpViewset(ViewSet):
    '''Sign up a user to Airtech'''

    def create(self, request):
        '''Sign up and create a user account'''

        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'message': 'Sign up successful'},
            status=status.HTTP_201_CREATED
        )


class UserLoginViewset(ViewSet):
    '''Login a user'''

    def create(self, request):
        '''Login a user'''
        data = request.data
        if not data.get('email'):
            raise ValidationError('Email is required')

        if not data.get('password'):
            raise ValidationError('Password is required')
        # validate password and retrieve token
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise AuthenticationFailed

        if user.check_password(data.get('password')):
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                'message': 'Login successful',
                'token': token.key
            }
            return Response(data=data, status=status.HTTP_200_OK)

        raise AuthenticationFailed
