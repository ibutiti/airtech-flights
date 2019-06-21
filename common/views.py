from rest_framework.viewsets import (
    GenericViewSet,
    mixins
)


class CreateRetrieveUpdateDestroyViewset(mixins.CreateModelMixin,
                                         mixins.RetrieveModelMixin,
                                         mixins.UpdateModelMixin,
                                         mixins.DestroyModelMixin,
                                         GenericViewSet):
    '''Custom viewset without the list method implemented'''



class CreateRetrieveDestroyViewset(mixins.CreateModelMixin,
                                   mixins.RetrieveModelMixin,
                                   mixins.ListModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericViewSet):
    '''Custom viewset without the update methods implemented'''
