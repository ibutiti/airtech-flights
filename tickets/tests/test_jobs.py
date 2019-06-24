'''
Background jobs tests
'''
from unittest import mock

from tickets.jobs import send_flight_reminders
from tickets.tests.mixin import TestBase


class TicketJobsTestCase(TestBase):
    '''
    Ticket background jobs tests
    '''

    @mock.patch('tickets.models.send_email.delay')
    def test_send_email_reminder_background_job(self, send_email_mock):
        '''Test sends reminders'''
        self.ticket.status = 'PAID'
        self.ticket.save()

        send_email_mock.return_value = None

        send_flight_reminders()

        send_email_mock.assert_called()
        send_email_mock.assert_called_with(
            recipients=[self.ticket.user.email],
            subject='Airtech: Your Flight Ticket',
            content=f'Hey {self.ticket.user.full_name},\nHeads up! Your flight below leaves soon!\n{self.ticket.flight.flight_details}'
        )

    @mock.patch('tickets.models.send_email.delay')
    def test_send_email_reminder_background_job_ignores_unpaid_tickets(self, send_email_mock):
        '''Test sends reminders'''
        send_email_mock.return_value = None

        send_flight_reminders()

        send_email_mock.assert_not_called()
