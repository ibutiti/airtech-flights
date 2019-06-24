'''
Application mailer
'''
from django.conf import settings
from django.core.mail import send_mail
from django_rq import job

@job
def send_email(recipients, subject, content):
    '''Send email helper'''
    return send_mail(
        subject=subject,
        message=content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients
    )
