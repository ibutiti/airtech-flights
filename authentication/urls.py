from django.urls import path
from rest_framework import routers

from authentication.views import UserLoginViewset, UserSignUpViewset

router = routers.SimpleRouter()

router.register(r'signup', UserSignUpViewset, base_name='signup')
router.register(r'login', UserLoginViewset, base_name='login')

app_name = 'authentication'

urlpatterns = router.urls
