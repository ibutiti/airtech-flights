'''
User profile serializers module
'''
from rest_framework import serializers

from userprofile.models import PassportPhoto


class PassportPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PassportPhoto
        fields = ('id', 'file')
        read_only_fields = ('id',)

    def create(self, validated_data):
        '''Inject the request user to the create kwargs'''
        validated_data['user'] = self.context['user']

        return super().create(validated_data)

    def update(self, instance, validated_data):
        '''Delete existing photo before save'''
        instance.file.delete(save=False)
        return super().update(instance, validated_data)
