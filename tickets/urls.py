'''
Tickets endpoints url configuration
'''
from django.urls import path
from rest_framework import routers

from tickets.views import TicketViewset

router = routers.SimpleRouter()

router.register(r'', TicketViewset, basename='ticket')

app_name = 'ticket'

urlpatterns = router.urls
