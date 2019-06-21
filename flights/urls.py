'''
Flights endpoints url configuration
'''
from django.urls import path
from rest_framework import routers

from flights.views import FlightViewSet

router = routers.SimpleRouter()

router.register(r'', FlightViewSet, basename='flight')

app_name = 'flight'

urlpatterns = router.urls
