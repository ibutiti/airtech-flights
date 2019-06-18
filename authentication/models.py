from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from rest_framework.authtoken.models import Token

from common.models import BaseModel

class CustomUserManager(UserManager):
    """Override custom user manager"""

    def _create_token(self, user):
        """Helper method to create a user token on user creation."""

        return Token.objects.create(user=user)


    def create_user(self, email, first_name, last_name, password=None):

        if not email:
            raise ValueError('Users must have an email address')
        normalized_email = self.normalize_email(email)
        user = self.model(
            email=normalized_email,
            username=normalized_email,
            first_name=first_name.strip(),
            last_name=last_name.strip()
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        self._create_token(user)

        return user

    def create_superuser(self, email, first_name, last_name, password=None):

        user = self.create_user(email, first_name, last_name, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def get_by_natural_key(self, email):

        return self.get(email=email)


class User(AbstractUser, BaseModel):

    email = CIEmailField(
        unique=True,
        null=False,
        blank=False
    )
    first_name = models.CharField(
        null=False,
        blank=False,
        max_length=50
    )
    last_name = models.CharField(
        null=False,
        blank=False,
        max_length=50
    )
    verified_email = models.BooleanField(
        default=False
    )

    # configs
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    EMAIL_FIELD = 'email'

    objects = CustomUserManager()

    @property
    def full_name(self):

        return self.get_full_name()

    def delete(self):
        '''Before user soft delete, delete any saved passport photo'''
        self.delete_passport_photo()
        super().delete()

    def hard_delete(self, **kwargs):
        '''Before user hard delete, delete any saved passport photo'''
        self.delete_passport_photo()
        super().hard_delete(**kwargs)

    def delete_passport_photo(self):
        '''Passport photo delete helper that executes'''
        try:
            self.passport_photo.delete()
        except User.passport_photo.RelatedObjectDoesNotExist:
            pass

    def __str__(self):
        return self.email
