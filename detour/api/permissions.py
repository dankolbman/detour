from rest_framework import permissions
from .models import Trip


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Anyone can read
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow if admin
        if request.user.is_superuser:
            return True

        parsed = request.parser_context['kwargs']
        if 'trip_id' in parsed:
            return Trip.objects.get(id=parsed['trip_id']).owner == request.user
        if 'pk' in parsed:
            return Trip.objects.get(id=parsed['pk']).owner == request.user
        return False

    def has_object_permission(self, request, view, obj):
        # Anyone can read
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow if admin
        if request.user.is_superuser:
            return True

        # Trip must belong to user
        if hasattr(obj, 'trip'):
            return obj.trip.owner == request.user
        if hasattr(obj, 'owner'):
            return obj.owner == request.user

        return False
