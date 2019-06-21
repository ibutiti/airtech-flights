'''
Flight ticket model
'''
from django.db import models

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
