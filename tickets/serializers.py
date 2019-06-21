'''
Tickets serializer module
'''
from rest_framework import serializers

from flights.serializers import FlightSerializer
from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    '''Tickets serializer'''

    class Meta:
        model = Ticket
        exclude = ('deleted_at', 'user')
        read_only_fields = ('status',)

    def create(self, validated_data):
        '''Inject the request user to the create kwargs, check for available seats'''
        if validated_data['flight'].available_seats < 1:
            raise serializers.ValidationError('This flight has no available seats')
        validated_data['user'] = self.context['user']
        return super().create(validated_data)

    def to_representation(self, instance):
        '''Add flight details to output'''
        output = super().to_representation(instance)
        output['flight'] = FlightSerializer(instance.flight).data
        return output