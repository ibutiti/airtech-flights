from django.db import models

from common.mailer import send_email
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
        default=0,
        null=False,
        blank=False
    )

    @property
    def available_seats(self):
        '''Number of available seats on the flight'''
        return self.seats - self.tickets.count()

    @property
    def flight_number(self):
        '''5 Character flight number'''
        return str(self.id)[:5]

    @property
    def flight_details(self):
        '''Helper to create a human friendly flight detail representation'''
        return (f'Flight Number: {self.flight_number}\nOrigin: {self.origin}\n'
                f'Departure Time: {str(self.departure_time)}\nDestination: {self.destination}\n'
                f'Arrival Time: {str(self.arrival_time)}\nFlight status: {self.status}'
        )

    def __str__(self):
        return f'Flight {self.flight_number} {str(self.departure_time)}: {self.origin} -> {self.destination}'

    def save(self, *args, **kwargs):
        '''Send status updates to ticket holders'''
        super().save(*args, **kwargs)
        subject = 'Airtech: Updates to your flight'
        tickets = self.tickets.all()
        if tickets:
            users = set([ticket.user for ticket in self.tickets.all()])
            for user in users:
                send_email.delay(
                    subject=subject,
                    content=f'Hey {user.full_name},\nYour flight has been updated. Here are the new details:\n{self.flight_details}',
                    recipients=[user.email]
                )
