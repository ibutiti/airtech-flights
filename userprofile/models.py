'''
Module for user profile models
'''
from django.db import models

from common.models import BaseModelHardDelete


class PassportPhoto(BaseModelHardDelete):
    '''
    Model class for user passport photos
    '''
    user = models.OneToOneField(
        to='authentication.User',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='passport_photo'
    )
    file = models.ImageField(
        null=False,
        blank=False,
        height_field='image_height',
        width_field='image_width',
        upload_to='passport_photos'
    )
    image_height = models.CharField(
        null=True,
        blank=True,
        max_length=16
    )
    image_width = models.CharField(
        null=True,
        blank=True,
        max_length=16
    )

    def delete(self, **kwargs):
        '''Delete the image file on S3 before deleting the instance'''
        self.delete_photo(save=False)
        super().delete(**kwargs)

    def delete_photo(self, save):
        '''Delete the image file from S3'''
        self.file.delete(save=save)

    def __str__(self):
        return self.file.name
