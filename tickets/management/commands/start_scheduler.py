'''
Management command to enqueue scheduled jobs
'''
import logging

import django_rq

from django_rq.management.commands import rqscheduler

from tickets.jobs import send_flight_reminders

scheduler = django_rq.get_scheduler()
log = logging.getLogger(__name__)

scheduled_jobs = [
    {
        'cron_string': '0/30 * * * *',  # Run every half hour
        'func': send_flight_reminders
    },
]

def clear_scheduled_jobs():
    # Delete any existing jobs in the scheduler when the app starts up
    log.info('Clearing existing scheduled jobs')
    for job in scheduler.get_jobs():
        log.debug("Deleting scheduled job %s", job)
        job.delete()

def register_scheduled_jobs():
    # scheduling jobs here
    log.info('Creating new scheduled jobs')
    for job in scheduled_jobs:
        scheduler.cron(
            job['cron_string'],
            func=job['func']
        )

class Command(rqscheduler.Command):
    def handle(self, *args, **kwargs):
        # This is necessary to prevent dupes
        clear_scheduled_jobs()
        register_scheduled_jobs()
        super(Command, self).handle(*args, **kwargs)
