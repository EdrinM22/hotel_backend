from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from users.serializers.cleaner_serializer import CleanerListSerializer, CleanerCreateSerializer
from users.permissions.guest_permissions import GuestPermission
from users.permissions.admin_permisions import AdminPermission
from users.permissions.hotel_manager_permissions import HotelManagerPermissions

from users.models import Cleaner, Admin, HotelManager


class CleanerCreateListAPIView(ListCreateAPIView):
    queryset = Cleaner.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CleanerCreateSerializer
        else:
            return CleanerListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Cleaner Created'}, status=status.HTTP_201_CREATED)

class CleanerRetrieveAPIView(RetrieveAPIView):
    queryset = Cleaner.objects.all()
    serializer_class = CleanerListSerializer
    permission_classes = [IsAuthenticated, GuestPermission, HotelManagerPermissions, AdminPermission]

    def get_object(self):
        if Admin.objects.filter(user=self.request.user).exists() or HotelManager.objects.filter(user=self.request.user).exists():
            return Cleaner.objects.get(id=self.request.query_params.get('cleaner_id')) if Cleaner.objects.filter(id=self.request.query_params.get('cleaner_id')).exists() else None
        elif Cleaner.objects.filter(user=self.request.user).exists():
            return Cleaner.objects.get(user=self.request.user)
        