from random import randint

from authentication.models import User

class TestMixin:

    @staticmethod
    def create_user():
        """Create a user"""
        username = f'testuser-{randint(1, 1000)}'
        email = f'{username}@example.com'
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name='John',
            last_name='DeMethew'
        )
        return user
