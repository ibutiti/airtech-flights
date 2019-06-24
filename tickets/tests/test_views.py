'''
Ticket endpoint tests
'''
from unittest import mock
from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tickets.models import Ticket
from tickets.tests.mixin import TestBase


class TicketViewsetTestCase(TestBase):
    '''
    Ticket view set test case
    '''

    def setUp(self):
        '''Setup test case'''
        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('ticket:ticket-list')
        self.payload = {'flight': str(self.flight.id)}

# Test GET many

    def test_get_tickets_success(self):
        '''Test authenticated user can get their tickets'''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_tickets_unauthenticated(self):
        '''Test get tickets while not authenticated fails'''
        client = APIClient()

        response = client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_get_another_user_tickets(self):
        '''Test user cannot get another user's tickets'''
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

# Test GET one

    def test_get_ticket_by_id_success(self):
        '''Test user can get their ticket by id'''
        url = reverse('ticket:ticket-detail', kwargs={'pk': str(self.ticket.id)})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(str(self.ticket.id), str(response.data))


    def test_get_ticket_by_id_unauthenticated_fails(self):
        '''Test user cannot get a ticket by id when not authenticated'''
        url = reverse('ticket:ticket-detail', kwargs={'pk': str(self.ticket.id)})
        client = APIClient()

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn(str(self.ticket.id), str(response.data))

    def test_get_another_user_ticket_by_id_fails(self):
        '''Test an authenticated user cannot get another user's ticket by id'''
        url = reverse('ticket:ticket-detail', kwargs={'pk': str(self.ticket.id)})
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn(str(self.ticket.id), str(response.data))

# Test POST

    @mock.patch('tickets.models.send_email', mock.MagicMock(return_value=None))
    def test_create_ticket_success(self):
        '''Test an authenticated user can create a flight successfully when seats available'''
        initial_seats_count = self.flight.available_seats

        response = self.client.post(self.url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(str(self.flight.id), str(response.data))

        with self.subTest('Test reduces the number of available seats in the flight'):
            self.assertEqual(self.flight.available_seats, initial_seats_count-1)


    def test_create_ticket_unauthenticated_fails(self):
        '''Test a unauthenticated user cannot create a ticket'''
        initial_seats_count = self.flight.available_seats
        client = APIClient()

        response = client.post(self.url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn(str(self.flight.id), str(response.data))

        with self.subTest('Test does not reduce the number of available seats in the flight'):
            self.assertEqual(self.flight.available_seats, initial_seats_count)

    @mock.patch('flights.models.send_email', mock.MagicMock(return_value=None))
    def test_create_ticket_fails_when_flight_has_no_seats(self):
        '''Test creating a ticket on a flight with no seats fails'''
        self.flight.seats = 1
        self.flight.save()
        initial_seats_count = self.flight.available_seats

        response = self.client.post(self.url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This flight has no available seats', str(response.data))

        with self.subTest('Test does not reduce the number of available seats in the flight'):
            self.assertEqual(self.flight.available_seats, initial_seats_count)

    @mock.patch('flights.models.send_email', mock.MagicMock(return_value=None))
    def test_create_ticket_fails_when_flight_is_not_open(self):
        '''Test creating a ticket on a non open flight fails'''
        self.flight.status = 'Closed'
        self.flight.save()
        initial_seats_count = self.flight.available_seats

        response = self.client.post(self.url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This flight is not open for booking', str(response.data))

        with self.subTest('Test does not reduce the number of available seats in the flight'):
            self.assertEqual(self.flight.available_seats, initial_seats_count)

    def test_create_ticket_on_nonexistent_flight_fails(self):
        '''Test creating a ticket on a nonexistent fight fails'''
        response = self.client.post(self.url, data={'flight': str(uuid4())})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('does not exist', str(response.data))

    def test_create_ticket_no_flight_in_body_fails(self):
        '''Test creating a ticket with no flight in body fails'''
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field is required', str(response.data))

# Test DELETE

    def test_delete_success(self):
        '''Test user can delete their ticket'''
        initial_ticket_count = Ticket.objects.count()
        initial_available_seat_count = self.flight.available_seats
        url = reverse('ticket:ticket-detail', kwargs={'pk': str(self.ticket.id)})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ticket.objects.count(), initial_ticket_count-1)

        with self.subTest('Test increases the number of available seats'):
            self.assertEqual(self.flight.available_seats, initial_available_seat_count+1)


    def test_delete_nonexistent_ticket_fails(self):
        '''Test deleting a nonexistent ticket fails'''
        initial_ticket_count = Ticket.objects.count()
        url = reverse('ticket:ticket-detail', kwargs={'pk': str(uuid4())})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Ticket.objects.count(), initial_ticket_count)

    def test_delete_other_users_ticket_fails(self):
        '''Test deleting another user's ticket fails'''
        initial_ticket_count = Ticket.objects.count()
        initial_available_seat_count = self.flight.available_seats
        url = reverse('ticket:ticket-detail', kwargs={'pk': str(self.ticket.id)})
        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Ticket.objects.count(), initial_ticket_count)

        with self.subTest('Test increases the number of available seats'):
            self.assertEqual(self.flight.available_seats, initial_available_seat_count)
