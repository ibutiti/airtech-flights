from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.tests.mixins import AbstractTestCase


class UserSignupViewsetTestCase(AbstractTestCase):
    '''User sign up view tests'''

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.valid_data = {
            "email": "c@b.com",
            "password": "strong one",
            "first_name": "name",
            "last_name": "last"
        }
        self.url = reverse('authentication:signup-list')

    def test_creates_user_successfully(self):
        '''Test valid request body creates user successfully'''

        response = self.client.post(self.url, data=self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], 'sign up successful')

    def test_validates_signup_data(self):
        '''Test request body validated and errors raised accordingly.'''

        with self.subTest('Test rejects duplicate email'):

            data = dict(**self.valid_data)
            data['email'] = self.user.email

            response = self.client.post(self.url, data=data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                str(response.json()),
                "{'error': {'email': ['user with this email already exists.']}}"
            )

        with self.subTest('Test rejects invalid email'):

            data = dict(**self.valid_data)
            data['email'] = 'not an email'

            response = self.client.post(self.url, data=data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                str(response.json()),
                "{'error': {'email': ['Enter a valid email address.']}}"
            )

        with self.subTest('Test rejects any missing fields'):

            name_fields = ('first_name', 'last_name', 'email', 'password')

            for name in name_fields:
                data = dict(**self.valid_data)
                data.pop(name)

                response = self.client.post(self.url, data=data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(
                    f"'{name}': ['This field is required.']",
                    str(response.json())
                )
