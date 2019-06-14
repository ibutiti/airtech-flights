from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from authentication.models import User
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

        # shouldn't raise a DoesNotExistError
        new_user = User.objects.get(email=self.valid_data['email'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], 'Sign up successful')

        with self.subTest('Test sets user password'):
            self.assertTrue(new_user.check_password('strong one'))

        with self.subTest('Test creates the right kind of user'):
            self.assertFalse(new_user.is_superuser)
            self.assertFalse(new_user.is_staff)

        with self.subTest('Test sets attributes correctly'):
            data = dict(**self.valid_data)
            data.pop('password')
            for attrib, value in data.items():
                self.assertEqual(getattr(new_user, attrib), value)
            self.assertTrue(new_user.is_active)
            self.assertFalse(new_user.verified_email)

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

        with self.subTest('Test rejects any missing required fields'):

            _fields = ('first_name', 'last_name', 'email', 'password')

            for name in _fields:
                data = dict(**self.valid_data)
                data.pop(name)

                response = self.client.post(self.url, data=data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(
                    f"'{name}': ['This field is required.']",
                    str(response.json())
                )


class UserLoginViewsetTestCase(AbstractTestCase):
    '''User login tests'''

    def setUp(self):
        super().setUp()
        self.url = reverse('authentication:login-list')
        self.client = APIClient()
        password = 'some password'
        self.user.set_password(password)
        self.user.save()
        self.valid_credentials = {
            'email': self.user.email,
            'password': password
        }

    def test_logs_in_with_valid_credentials(self):
        '''Test logs in with valid credentials'''

        response = self.client.post(self.url, data=self.valid_credentials)

        token = Token.objects.get(user=self.user).key

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(token, response.json().get('token'))
        self.assertIn('Login successful', str(response.json()))
