from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import User
from authentication.serializers import UserSignUpSerializer


class UserSignUpViewset(ViewSet):
    '''Sign up a user to Airtech'''

    def create(self, request):
        '''POST request to sign up user'''

        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'message': 'sign up successful'},
            status=status.HTTP_201_CREATED
        )
