'''
Commonly used test utilities
'''
import datetime

from io import BytesIO
from unittest import mock

from django.core.files import File
from django.core.files.storage import Storage
from PIL import Image

from authentication.models import User
from flights.models import Flight
from tickets.models import Ticket
from userprofile.models import PassportPhoto

class TestMixin:
    """Mixin class to add in common test methods to test classes."""

    # counter to make sure helper not creating duplicate users
    user_count = 0

    @classmethod
    def create_user(cls, superuser=False, photo_data=None):
        """Helper function to generate testing users

        :param superuser: whether the user should be a superuser, defaults to False
        :type superuser: bool, optional
        :param passport_photo_data: dict with photo_url and filename keys to mock with.
                                    If this is None, user created without a passport photo,
                                    defaults to None
        :type passport_photo_data: dict, optional
        :return: A new user with the above attributes if given
        :rtype: User
        """
        cls.user_count += 1
        name = f'testuser-{1000 + cls.user_count}'
        email = f'{name}@example.com'
        if superuser:
            user = User.objects.create_superuser(
                email=email,
                first_name=name,
                last_name=name[::-1]
            )
        else:
            user = User.objects.create_user(
                email=email,
                first_name=name,
                last_name=name[::-1]
            )

        if photo_data:
            cls.create_passport_photo(user, **photo_data)

        return user

    @classmethod
    def create_image(cls, filename):
        '''Create an image object'''
        tmp_img_file = BytesIO()
        image = Image.new('RGB', (600, 600))
        image.save(tmp_img_file, format='jpeg')
        tmp_img_file.name = filename
        tmp_img_file.width = 600
        tmp_img_file.height = 600
        tmp_img_file.seek(0)
        file = File(tmp_img_file)
        return file

    @classmethod
    def patch_s3_storage(cls, photo_url):
        '''Create an S3 storage mock patch'''
        storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
        storage_mock.url = mock.MagicMock(name='url')
        storage_mock.url.return_value = photo_url
        storage_mock.__str__.return_value = photo_url
        return mock.patch('django.core.files.storage.default_storage._wrapped', storage_mock)


    @classmethod
    def create_passport_photo(cls, user, photo_url, filename):
        '''
        Create a passport photo for the given user with the above filename and url in memory
        '''
        image = cls.create_image(filename=filename)

        photo = PassportPhoto.objects.create(
            user=user,
            file=image
            )
        return photo


    @classmethod
    def create_flight(cls, origin, destination, seats, departure_time=None, arrival_time=None, status='Open'):
        '''
        Helper to create a flight
        '''
        now = datetime.datetime.now(datetime.timezone.utc)
        if not departure_time:
            departure_time = now + datetime.timedelta(hours=12)

        if not arrival_time:
            arrival_time = now + datetime.timedelta(hours=24)

        return Flight.objects.create(
            origin=origin,
            destination=destination,
            seats=seats,
            departure_time=departure_time,
            arrival_time=arrival_time,
            status=status
        )


    @classmethod
    def create_ticket(cls, flight, user, status):
        return Ticket.objects.create(
            flight=flight,
            user=user,
            status=status
        )
