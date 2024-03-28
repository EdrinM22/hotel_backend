from django.db import transaction

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Admin

from users.serializers.hotel_admin_serializer import AdminCreateSerializer, AdminListSerializer


class HotelAdminListCreateAPIView(ListCreateAPIView):
    queryset = Admin.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminCreateSerializer
        else:
            return AdminListSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        return Admin.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Admin Created!'}, status=status.HTTP_201_CREATED)


class HotelAdminRetrieveAPIView(RetrieveAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminListSerializer

    def get_object(self):
        if Admin.objects.filter(user=self.request.user).exists():
            return Admin.objects.get(user=self.request.user)
