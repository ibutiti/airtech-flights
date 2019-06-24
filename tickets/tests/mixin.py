'''
Test setup for ticket tests
'''
from django.test import TestCase
from rest_framework.test import APIClient

from common.test_mixins import TestMixin


class TestBase(TestCase, TestMixin):

    def setUp(self):
        '''
        Setup test variables
        '''
        self.client = APIClient()
        self.user = self.create_user()
        self.user2 = self.create_user()
        self.flight = self.create_flight(
            origin='Nairobi',
            destination='Kampala',
            seats=2
        )
        self.ticket = self.create_ticket(
            flight=self.flight,
            user=self.user,
            status='RESERVATION'
        )
