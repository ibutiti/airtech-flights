'''
Flight ticket model
'''
from django.db import models

from common.mailer import send_email
from common.models import BaseModel
from common.utils import ChoiceEnum


class TicketStatus(ChoiceEnum):
    '''Ticket status choices'''
    reservation = 'RESERVATION'
    paid = 'PAID'


class Ticket(BaseModel):
    '''Model for flight tickets'''
    flight = models.ForeignKey(
        'flights.flight',
        null=False,
        blank=False,
        related_name='tickets',
        on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(
        'authentication.user',
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING
    )
    status = models.CharField(
        default=TicketStatus.reservation.value,
        choices=TicketStatus.choices(),
        null=False,
        blank=False,
        max_length=32
    )
    reminder_sent = models.BooleanField(default=False)

    def send_ticket_to_user(self, message_type):
        '''Utility to send the ticket to the user'''
        message_mapping = {
            'RESERVATION': 'Your flight reservation has been made. Please make full payment to confirm the booking.',
            'PAID': 'Your flight reservation has been confirmed.',
            'REMINDER': 'Heads up! Your flight below leaves soon!'
        }
        content = f'Hey {self.user.full_name},\n{message_mapping[message_type]}\n{self.flight.flight_details}'
        send_email.delay(
            recipients=[self.user.email],
            subject='Airtech: Your Flight Ticket',
            content=content
        )
