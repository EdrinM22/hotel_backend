from rest_framework.permissions import BasePermission

from users.models import Guest, Admin, HotelManager


class GuestPermission(BasePermission):

    def has_permission(self, request, view):
        return Guest.objects.filter(user=request.user).exists() or Admin.objects.filter(
            user=request.user).exists() or HotelManager.objects.filter(user=request.user).exists()


class GuestOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return Guest.objects.filter(user=request.user).exists()