from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from authentication.models import User


class UserBaseSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('email',)

    def validate(self, data):
        '''Validate sign up data.'''

        for field in self.get_fields().keys():
            if not data.get(field):
                raise serializers.ValidationError(f'{field} is required')
        super().validate(data)

        return data


class UserSignUpSerializer(UserBaseSerializer):
    '''Serializer for user sign up operation'''

    class Meta:

        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):

        return User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
