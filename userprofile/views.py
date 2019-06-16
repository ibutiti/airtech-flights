'''
User profile views module
'''
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from userprofile.models import PassportPhoto
from userprofile.serializers import PassportPhotoSerializer


class UserPassportPhotoViewset(ModelViewSet):
    '''Viewset for user passport photos'''

    parser_classes = (MultiPartParser,)
    serializer_class = PassportPhotoSerializer
    queryset = PassportPhoto.objects.all()

    def get_queryset(self):
        '''Filter the queryset by user to make sure we only return the user's photo'''
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user).all()

    def get_object(self):
        '''Fail early and return a 404 if passport photo doesn't exist'''
        return get_object_or_404(self.get_queryset())

    def get_serializer_context(self):
        '''Inject the request user to the serializer context, used at model create stage'''
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context

    def create(self, request):
        '''Check if user has a passport photo first before attempting a create'''

        passport_photo = self.get_queryset().first()

        if passport_photo:
            data = {
                'message': 'A passport photo already exists. Use the PUT endpoint to replace it.',
                'passport_photo': self.serializer_class(passport_photo).data
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)
