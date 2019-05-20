from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from authentication.models import User

class CustomUserAdmin(UserAdmin):
    model = User

admin.site.register(User, CustomUserAdmin)
