'''
User profile endpoint tests
'''
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from userprofile.tests.test_mixin import TestBase


class UserProfileViewsetTestCase(TestBase):
    '''
    User profile viewset test case
    '''

    def setUp(self):
        '''Setup test case'''
        super().setUp()
        self.client.force_authenticate(user=self.user_no_photo)
        self.url = reverse('userprofile:passport-photo-list')

# Test POST

    def test_create_with_unauthenticated_user(self):
        '''Test add photo as an unauthenticated user.'''
        client = APIClient()
        response = client.post(self.url, data={'file': self.test_photo})
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', str(response_data))

    def test_create_success(self):
        '''Test adds passport photo successfully'''
        response = self.client.post(self.url, data={'file': self.test_photo})
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.test_photo.name, str(response_data))

    def test_create_twice(self):
        '''Test add passport photo to user with a passport photo already'''
        self.client.force_authenticate(self.user_with_photo)

        response = self.client.post(self.url, data={'file': self.test_photo})
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A passport photo already exists. Use the PUT endpoint to replace it.',
                      str(response_data))

    def test_create_no_payload(self):
        '''Test add photo with no photo payload'''
        response = self.client.post(self.url)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No file was submitted', str(response_data))

    def test_create_non_photo_file(self):
        '''Test add photo with a non photo file in payload'''
        response = self.client.post(self.url, data={'file': self.non_photo_file})
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Upload a valid image', str(response_data))


# Test PUT

    def test_replace_photo_success(self):
        '''Test replacing a photo success'''
        self.client.force_authenticate(self.user_with_photo)
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = self.client.put(url, data={'file': self.test_photo})
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.test_photo.name.split('.')[0], str(response_data))

    def test_replace_photo_unauthenticated(self):
        '''Test replacing a photo when not authenticated'''
        client = APIClient()
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = client.put(url, data={'file': self.test_photo})
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', str(response_data))

    def test_replace_another_users_photo(self):
        '''Test replacing another user's photo fails'''
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = self.client.put(url, data={'file': self.test_photo})
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('NotFound', str(response_data))

    def test_replace_photo_no_photo_in_payload(self):
        '''Test replacing a photo with no photo'''
        self.client.force_authenticate(self.user_with_photo)
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = self.client.put(url)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No file was submitted', str(response_data))

    def test_replace_photo_with_non_photo(self):
        '''Test replacing a photo with a non photo file'''
        self.client.force_authenticate(self.user_with_photo)
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = self.client.put(url, data={'file': self.non_photo_file})
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Upload a valid image', str(response_data))


# Test DELETE

    def test_delete_photo_success(self):
        '''Test deleting a photo success'''
        self.client.force_authenticate(self.user_with_photo)
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_photo_unauthenticated(self):
        '''Test deleting a photo when not authenticated'''
        client = APIClient()
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = client.delete(url)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', str(response_data))

    def test_delete_another_users_photo(self):
        '''Test deleting another user's photo fails'''
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = self.client.delete(url)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('NotFound', str(response_data))

# Test GET

    def test_get_passport_photo_success(self):
        '''Test a successful get of a passport photo'''
        self.client.force_authenticate(self.user_with_photo)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user_with_photo.passport_photo.file.name.split('.')[0], str(response.data))

    def get_passport_photo_fails_when_unauthenticated(self):
        '''Test get photo when not authenticated'''
        client = APIClient()

        response = client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided', str(response.data))

    def get_passport_photo_when_user_has_none(self):
        '''Test get passport photo when a user has none'''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('{}', str(response.data))

    def test_get_passport_photo_via_id_success(self):
        '''Test get passport photo via its id success'''
        self.client.force_authenticate(self.user_with_photo)
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user_with_photo.passport_photo.file.name.split('.')[0], str(response.data))

    def test_get_another_users_photo(self):
        '''Test get another user's photo fails'''
        url = reverse('userprofile:passport-photo-detail',
                      kwargs={'pk': self.user_with_photo.passport_photo.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('NotFound', str(response.data))
