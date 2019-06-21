'''
Module for flight serializer
'''
from rest_framework import serializers

from flights.models import Flight


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ('status', 'origin', 'destination', 'departure_time',
                  'arrival_time', 'seats', 'available_seats')
        read_only_fields = ('available_seats',)
