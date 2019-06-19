'''
Test setup for flight tests
'''
from django.test import TestCase
from rest_framework.test import APIClient

from common.test_mixins import TestMixin
from flights.models import Flight


class TestBase(TestCase, TestMixin):

    def setUp(self):
        '''
        Setup test variables
        '''
        self.admin_user = self.create_user(superuser=True)
        self.normal_user = self.create_user()
        self.client = APIClient()
        self.flight_data = {
            'status': 'Open',
            'origin': 'Nairobi',
            'destination': 'Kampala',
            'departure_time': '2019-06-20 21:00',
            'arrival_time': '2019-06-21 12:00',
            'seats': 200
        }
        self.flight = Flight.objects.create(**self.flight_data)
