from rest_framework.permissions import BasePermission
from users.models import HotelManager, Admin


class HotelManagerPermissions(BasePermission):

    def has_permission(self, request, view):
        return HotelManager.objects.filter(user=request.user).exists() or Admin.objects.filter(user=request.user).exists()
