'''
Ticket related background jobs
'''
import datetime
import logging

from django_rq import job

from common.mailer import send_email
from tickets.models import Ticket

logger = logging.getLogger(__name__)

@job
def send_flight_reminders():
    '''
    Send email reminders to users with tickets that are departing in 24 hours
    '''
    logger.info('Sending out email reminders')
    time_cutoff = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    tickets = Ticket.objects.filter(
        status='PAID',
        flight__departure_time__lte=time_cutoff,
        reminder_sent=False).all()

    if not tickets:
        return

    for ticket in tickets:
        ticket.send_ticket_to_user(message_type='REMINDER')
        ticket.reminder_sent = True
        ticket.save()
