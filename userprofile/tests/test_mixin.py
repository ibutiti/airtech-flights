'''
Test setup for user profile tests
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
        self.photo_data = {
            'filename': 'test_photo.jpg',
            'photo_url': 'https://bucket.s3.com/passport_photos/test_photo.jpg'
        }
        self.user_with_photo = self.create_user(photo_data=self.photo_data)
        self.user_no_photo = self.create_user()
        self.test_photo = self.create_image(filename='test_photo1.jpg')
        self.non_photo_file = open('./LICENSE', 'rb')
