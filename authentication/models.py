from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CIEmailField
from django.db import models


class User(AbstractUser):

    email = CIEmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(null=False, blank=False, max_length=50)
    last_name = models.CharField(null=False, blank=False, max_length=50)
    verified_email = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email
