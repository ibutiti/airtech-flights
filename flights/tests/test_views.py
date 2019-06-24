'''
Flight endpoint tests
'''
from unittest import mock
from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from flights.models import Flight
from flights.tests.mixin import TestBase


class FlightViewsetTestCase(TestBase):
    '''
    Flight view set test case
    '''

    def setUp(self):
        '''Setup test case'''
        super().setUp()
        self.client.force_authenticate(user=self.admin_user)
        self.url = reverse('flight:flight-list')

# Test GET Many

    def test_get_flights_unauthenticated(self):
        '''Test unauthenticated users can get flights'''
        client = APIClient()

        response = client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(str(self.flight.id), response.data[0]['id'])

    def test_get_flights_admin_authenticated(self):
        '''Test authenticated admins can get flights'''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(str(self.flight.id), response.data[0]['id'])

    def test_get_flights_nonadmin_authenticated(self):
        '''Test authenticated non admins can get flights'''
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(str(self.flight.id), response.data[0]['id'])


# Test GET One
    def test_get_flight_by_id_unauthenticated(self):
        '''Test unauthenticated users can get a single flight by id'''
        client = APIClient()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.flight.id))

    def test_get_flight_by_id_admin_authenticated(self):
        '''Test authenticated admin can get a single flight by id'''
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.flight.id))

    def test_get_flight_by_id_nonadmin_authenticated(self):
        '''Test authenticated non admins can get flight by id'''
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.flight.id))

# Test POST

    def test_create_flight_success(self):
        '''Test authenticated admin can create a flight'''
        initial_count = Flight.objects.count()

        response = self.client.post(self.url, data=self.flight_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['origin'], self.flight_data['origin'])
        self.assertEqual(Flight.objects.count(), initial_count+1)

    def test_create_flight_unauthenticated_fails(self):
        '''Test unauthenticated user cannot create a flight'''
        client = APIClient()
        initial_count = Flight.objects.count()

        response = client.post(self.url, data=self.flight_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_create_flight_authenticated_non_admin_fails(self):
        '''Test authenticated non admin user cannot create a flight'''
        self.client.force_authenticate(user=self.normal_user)
        initial_count = Flight.objects.count()

        response = self.client.post(self.url, data=self.flight_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('You do not have permission to perform this action', str(response.data))
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_create_no_payload(self):
        '''Test create without payload fails'''
        initial_count = Flight.objects.count()

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_create_missing_required_field(self):
        '''Test create fails if required field is not present'''
        initial_count = Flight.objects.count()
        required_fields = ('origin', 'destination', 'departure_time', 'arrival_time')

        for field in required_fields:
            with self.subTest(f'Test create fails when {field} is not in payload'):
                del self.flight_data[field]

                response = self.client.post(self.url, data=self.flight_data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(Flight.objects.count(), initial_count)
                self.assertIn(field, str(response.data))
                self.assertIn('This field is required', str(response.data))

# Test PUT
    @mock.patch('flights.models.send_email', mock.MagicMock(return_value=None))
    def test_full_update_flight_success(self):
        '''Test authenticated admin can full update a flight'''
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = self.client.put(url, data=self.flight_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['origin'], self.flight_data['origin'])
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_full_update_flight_fails_with_nonexistent_flight(self):
        '''Test authenticated admin full update fails on a nonexistent flight'''
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': str(uuid4())})

        response = self.client.patch(url, data=self.flight_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('NotFound', str(response.data))
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_full_update_flight_unauthenticated_fails(self):
        '''Test unauthenticated user cannot full update a flight'''
        client = APIClient()
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = client.put(url, data=self.flight_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_full_update_flight_authenticated_non_admin_fails(self):
        '''Test authenticated non admin user cannot full update a flight'''
        self.client.force_authenticate(user=self.normal_user)
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = self.client.put(url, data=self.flight_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('You do not have permission to perform this action', str(response.data))
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_full_update_no_payload(self):
        '''Test full update without payload fails'''
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_full_update_missing_required_field(self):
        '''Test full update fails if required field is not present'''
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})
        required_fields = ('origin', 'destination', 'departure_time', 'arrival_time')

        for field in required_fields:
            with self.subTest(f'Test full update fails when {field} is not in payload'):
                del self.flight_data[field]

                response = self.client.put(url, data=self.flight_data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(Flight.objects.count(), initial_count)
                self.assertIn(field, str(response.data))
                self.assertIn('This field is required', str(response.data))

# Test PATCH

    @mock.patch('flights.models.send_email', mock.MagicMock(return_value=None))
    def test_partial_update_flight_success(self):
        '''Test authenticated admin can partial update a flight'''
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})
        flight_data = {'origin': 'Mombasa'}

        response = self.client.patch(url, data=flight_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['origin'], flight_data['origin'])
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_partial_update_flight_fails_with_nonexistent_flight(self):
        '''Test authenticated admin partial update fails on a nonexistent flight'''
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': str(uuid4())})
        flight_data = {'origin': 'Mombasa'}

        response = self.client.patch(url, data=flight_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('NotFound', str(response.data))
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_partial_update_flight_unauthenticated_fails(self):
        '''Test unauthenticated user cannot partial update a flight'''
        client = APIClient()
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})
        flight_data = {'origin': 'Mombasa'}

        response = client.patch(url, data=flight_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_partial_update_flight_authenticated_non_admin_fails(self):
        '''Test authenticated non admin user cannot partial update a flight'''
        self.client.force_authenticate(user=self.normal_user)
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})
        flight_data = {'origin': 'Mombasa'}

        response = self.client.patch(url, data=flight_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('You do not have permission to perform this action', str(response.data))
        self.assertEqual(Flight.objects.count(), initial_count)

# Test DELETE

    def test_delete_flight_success(self):
        '''Test authenticated admin can delete a flight'''
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Flight.objects.count(), initial_count-1)

    def test_delete_flight_fails_with_nonexistent_flight(self):
        '''Test authenticated admin delete fails on a nonexistent flight'''
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': str(uuid4())})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('NotFound', str(response.data))
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_delete_flight_unauthenticated_fails(self):
        '''Test unauthenticated user cannot delete a flight'''
        client = APIClient()
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Flight.objects.count(), initial_count)

    def test_delete_flight_authenticated_non_admin_fails(self):
        '''Test authenticated non admin user cannot delete a flight'''
        self.client.force_authenticate(user=self.normal_user)
        initial_count = Flight.objects.count()
        url = reverse('flight:flight-detail', kwargs={'pk': self.flight.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('You do not have permission to perform this action', str(response.data))
        self.assertEqual(Flight.objects.count(), initial_count)
