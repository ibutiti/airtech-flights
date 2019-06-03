from random import randint

from authentication.models import User

class TestMixin:
    """Mixin class to add in common test methods to test classes."""

    # counter to make sure helper not creating duplicate users
    user_count = 0

    @classmethod
    def create_user(cls, superuser=False):
        """Create a user"""

        cls.user_count += 1
        name = f'testuser-{1000 + cls.user_count}'
        email = f'{name}@example.com'
        if superuser:

            user = User.objects.create_superuser(
                email=email,
                first_name=name,
                last_name=name[::-1]
            )

        else:

            user = User.objects.create_user(
                email=email,
                first_name=name,
                last_name=name[::-1]
            )

        return user
