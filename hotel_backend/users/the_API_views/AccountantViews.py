from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers.accountant_serializer import AccountantCreateSerializer, AccountantListSerializer
from users.models import Accountant, Admin, HotelManager


class AccountantListCreateAPIView(ListCreateAPIView):
    queryset = Accountant.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AccountantCreateSerializer
        else:
            return AccountantListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Accountant Created'}, status=status.HTTP_201_CREATED)


class AccountantRetreiveAPIView(RetrieveAPIView):
    queryset = Accountant.objects.all()
    serializer_class = AccountantListSerializer

    def get_object(self):
        if Admin.objects.filter(user=self.request.user).exists() or HotelManager.objects.filter(
                user=self.request.user).exists():
            return Accountant.objects.get(id=self.request.query_params.get('accountant_id')) if Admin.objects.filter(
                id=self.request.query_params.get('accountant_id')).exists() else None
