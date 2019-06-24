'''
Ticket views
'''
from rest_framework import exceptions, status
from rest_framework import serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from common.views import CreateRetrieveDestroyViewset
from tickets.models import Ticket
from tickets.serializers import TicketSerializer


class TicketViewset(CreateRetrieveDestroyViewset):
    '''Ticket management view set'''
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_queryset(self):
        '''Restrict queryset to user's tickets'''
        return super().get_queryset().filter(user=self.request.user).all()

    def get_object(self):
        '''Fail early and return a 404 if ticket does not exist'''
        try:
            return self.get_queryset().get(id=self.kwargs.get('pk'))
        except Ticket.DoesNotExist:
            raise exceptions.NotFound

    def get_serializer_context(self):
        '''Inject the request user to the serializer context, used at model create stage'''
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class TicketStatusView(APIView):
    '''View for admins to change the status of a ticket'''
    permission_classes = (IsAdminUser,)

    def post(self, request, format=None):
        '''Change status of a ticket'''
        try:
            ticket = Ticket.objects.get(pk=request.data.get('ticket_id'))
        except Ticket.DoesNotExist:
            raise serializers.ValidationError('Ticket does not exist')

        ticket_status = request.data.get('ticket_status')

        if not ticket_status:
            raise serializers.ValidationError('Ticket status is required')

        ticket.status = ticket_status
        ticket.save()

        # notify user of ticket status change
        ticket.send_ticket_to_user(message_type='PAID')

        return Response(status=status.HTTP_204_NO_CONTENT)


    def get(self, request):
        '''Get all reserved tickets'''
        tickets = Ticket.objects.filter(status='RESERVATION').all()

        serializer = TicketSerializer(tickets, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
