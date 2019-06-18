'''
Module for flight serializer
'''
from rest_framework import serializers

from flights.models import Flight


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        exclude = ('deleted_at',)
