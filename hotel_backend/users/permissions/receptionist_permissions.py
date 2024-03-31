from rest_framework.permissions import BasePermission

from users.models import Receptionist, Admin, HotelManager


class ReceptionistPermission(BasePermission):
    def has_permission(self, request, view):
        return Receptionist.objects.filter(user=request.user).exists() or Admin.objects.filter(
            user=request.user).exists() or HotelManager.objects.filter(user=request.user).exists()
