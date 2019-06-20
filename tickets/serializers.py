'''
Tickets serializer module
'''
from rest_framework import serializers

from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    '''Tickets serializer'''

    class Meta:
        model = Ticket
        exclude = ('deleted_at',)
        read_only_fields = ('status', 'user')
