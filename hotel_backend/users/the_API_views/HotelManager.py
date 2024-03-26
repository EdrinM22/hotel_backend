from django.db import transaction
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from users.models import HotelManager

from users.serializers.hotel_manager_serializer import HotelManagerListSerializer, HotelManagerCreateSerializer


class HotelManagerListCreateAPIView(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return HotelManagerCreateSerializer
        else:
            return HotelManagerListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Manager created!'}, status=status.HTTP_201_CREATED)
