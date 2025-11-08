# rides/permissions.py
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Allow only admin users."""
    message = "Access denied — Admins only."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')


class IsDriver(BasePermission):
    """Allow only drivers."""
    message = "Only drivers can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'driver')


class IsRider(BasePermission):
    """Allow only riders."""
    message = "Only riders can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'rider')


class IsDriverOrAdmin(BasePermission):
    """Allow drivers or admins."""
    message = "Only drivers or admins can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['driver', 'admin'])


class IsRiderOrAdmin(BasePermission):
    """Allow riders or admins."""
    message = "Only riders or admins can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['rider', 'admin'])
