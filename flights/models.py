from django.db import models

from common.models import BaseModel


class Flight(BaseModel):
    '''
    Model for flight data
    '''
    status = models.CharField(
        default='Open',
        null=True,
        blank=True,
        max_length=16
    )
    origin = models.CharField(
        null=False,
        blank=False,
        max_length=16
    )
    destination = models.CharField(
        null=False,
        blank=False,
        max_length=16
    )
    departure_time = models.DateTimeField(
        null=False,
        blank=False
    )
    arrival_time = models.DateTimeField(
        null=False,
        blank=False
    )
    seats = models.IntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Flight {str(self.id)[:5]} {str(self.departure_time)}: {self.origin} -> {self.destination}'
