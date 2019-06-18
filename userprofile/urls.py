'''
User profile endpoints url configuration
'''
from django.urls import path
from rest_framework import routers

from userprofile.views import UserPassportPhotoViewset

router = routers.SimpleRouter()

router.register(r'passport-photo', UserPassportPhotoViewset, basename='passport-photo')

app_name = 'userprofile'

urlpatterns = router.urls
