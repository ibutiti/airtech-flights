from rest_framework import routers
from authentication.views import UserSignUpViewset

router = routers.SimpleRouter()

router.register(r'signup', UserSignUpViewset, base_name='signup')
app_name = 'authentication'
urlpatterns = router.urls
