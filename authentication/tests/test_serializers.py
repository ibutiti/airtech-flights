from authentication.serializers import UserSignUpSerializer
from authentication.tests.mixins import AbstractTestCase


class UserSignUpSerializerTestCase(AbstractTestCase):
    '''User sign up serializer tests'''

    def setUp(self):

        self.valid_sign_up_data = {
            'email': 'a@b.com',
            'password': 'tygh12d',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_validates(self):
        '''Test validation passes with correct data'''

        ser = UserSignUpSerializer(data=self.valid_sign_up_data)

        self.assertTrue(ser.is_valid())

    def test_validates_email(self):
        '''Test email field is validated correctly.'''

        with self.subTest('test validation fails on missing email'):

            data_email_missing = dict(**self.valid_sign_up_data)
            data_email_missing.pop('email')

            ser = UserSignUpSerializer(data=data_email_missing)

            self.assertFalse(ser.is_valid())
            self.assertIn('email', str(ser.errors))

        with self.subTest('test validation fails on empty string email'):

            data_empty_string_email = dict(**self.valid_sign_up_data)
            data_empty_string_email['email'] = ''

            ser = UserSignUpSerializer(data=data_empty_string_email)

            self.assertFalse(ser.is_valid())
            self.assertIn('email', str(ser.errors))
