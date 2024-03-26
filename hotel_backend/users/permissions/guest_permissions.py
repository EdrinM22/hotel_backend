from rest_framework.permissions import BasePermission

from users.models import Guest


class GuestPermission(BasePermission):

    def has_permission(self, request, view):
        return Guest.objects.filter(user=request.user).exists()