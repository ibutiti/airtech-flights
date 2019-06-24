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
        exclude = ('deleted_at', 'user', 'reminder_sent')
        read_only_fields = ('status',)

    def create(self, validated_data):
        '''Inject the request user to the create kwargs, check for available seats'''
        if validated_data['flight'].available_seats < 1:
            raise serializers.ValidationError('This flight has no available seats')
        if not validated_data['flight'].status == 'Open':
            raise serializers.ValidationError('This flight is not open for booking')
        validated_data['user'] = self.context['user']
        ticket = super().create(validated_data)
        ticket.send_ticket_to_user(message_type=ticket.status)
        return ticket

    def to_representation(self, instance):
        '''Add flight details to output'''
        output = super().to_representation(instance)
        output['flight'] = FlightSerializer(instance.flight).data
        return output
