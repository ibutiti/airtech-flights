from rest_framework import routers

from authentication.views import (
    UserLoginViewset,
    UserSignUpViewset
)

router = routers.SimpleRouter()

router.register(r'login', UserLoginViewset, basename='login')
router.register(r'signup', UserSignUpViewset, basename='signup')

app_name = 'authentication'

urlpatterns = router.urls
