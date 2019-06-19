from rest_framework import permissions


class FlightPermissions(permissions.IsAdminUser):
    '''
    Custom permission class to allow unauthenticated users
    access safe HTTP methods HEAD, OPTIONS, GET
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)
