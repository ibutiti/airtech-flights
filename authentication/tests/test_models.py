from django.db.utils import IntegrityError

from authentication.models import User
from authentication.tests.mixins import AbstractTestCase



class TestUserModel(AbstractTestCase):

    def test_creates_users(self):
        '''Test user model creates users successfully'''

        self.assertEqual(User.objects.count(), 2)

    def test_creates_correct_user_types(self):
        '''Test User model creates both normal and superusers successfully.'''

        with self.subTest('Test creates superusers'):

            self.assertEqual(User.objects.filter(is_superuser=True).count(), 1)

        with self.subTest('Test creates normal users'):

            self.assertEqual(User.objects.exclude(is_superuser=True).count(), 1)

    def test_email_unique_constraint(self):
        '''Test email unique constraint is upheld.'''

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.user.email,
                first_name='first',
                last_name='last'
            )
