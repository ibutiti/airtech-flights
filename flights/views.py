'''
Flight views
'''
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from flights.models import Flight
from flights.permissions import FlightPermissions
from flights.serializers import FlightSerializer


class FlightViewSet(ModelViewSet):
    '''Flight management view set'''
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    permission_classes = (FlightPermissions,)
