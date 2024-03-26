from django.db import transaction

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Admin

from users.serializers.hotel_admin_serializer import AdminCreateSerializer, AdminListSerializer

class HotelAdminListCreateAPIView(ListCreateAPIView):

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
