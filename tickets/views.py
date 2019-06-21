'''
Ticket views
'''
from rest_framework import exceptions

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
