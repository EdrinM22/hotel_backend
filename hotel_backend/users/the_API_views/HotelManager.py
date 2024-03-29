from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from users.models import HotelManager, Admin

from users.serializers.hotel_manager_serializer import HotelManagerListSerializer, HotelManagerCreateSerializer


class HotelManagerListCreateAPIView(ListCreateAPIView):
    queryset = HotelManager.objects.all()
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

class HotelManagerRetrieveAPIView(RetrieveAPIView):
    queryset = HotelManager.objects.all()
    serializer_class = HotelManagerListSerializer

    def get_object(self):
        if HotelManager.objects.filter(user=self.request.user).exists():
            return HotelManager.objects.get(user=self.request.user)
        elif Admin.objects.filter(user=self.request.user).exists():
            return HotelManager.objects.get(id=self.request.query_params.get('hotel_manager_id')) \
                if HotelManager.objects.filter(id=self.request.query_params.get('hotel_manager_id')).exists() else None
