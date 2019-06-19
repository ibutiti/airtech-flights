from django.db.utils import IntegrityError

from authentication.models import User
from authentication.tests.mixins import AbstractTestCase
from userprofile.models import PassportPhoto


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

    def test_user_model_properties(self):
        '''Test model properties'''
        with self.subTest('Test string representation'):
            self.assertEqual(str(self.user), self.user.email)
        with self.subTest('Test full name property'):
            self.assertEqual(self.user.full_name, f'{self.user.first_name} {self.user.last_name}')
        with self.subTest('Test manager get by natural key returns user by email input'):
            self.assertEqual(User.objects.get_by_natural_key(email=self.user.email), self.user)

    def test_deletes_passport_photo_during_soft_delete(self):
        '''Test deletes passport photo before soft delete'''
        user = self.create_user(photo_data={'filename': 'test.jpeg', 'photo_url': 'https://file.example.com/test.jpeg'})
        initial_photo_count = PassportPhoto.objects.count()

        user.delete()

        self.assertEqual(PassportPhoto.objects.count(), initial_photo_count-1)

    def test_deletes_passport_photo_during_hard_delete(self):
        '''Test deletes passport photo before hard delete'''
        user = self.create_user(
            photo_data={'filename': 'test.jpeg', 'photo_url': 'https://file.example.com/test.jpeg'})
        initial_photo_count = PassportPhoto.objects.count()

        user.hard_delete()

        self.assertEqual(PassportPhoto.objects.count(), initial_photo_count-1)

    def test_email_unique_constraint(self):
        '''Test email unique constraint is upheld.'''

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.user.email,
                first_name='first',
                last_name='last'
            )
