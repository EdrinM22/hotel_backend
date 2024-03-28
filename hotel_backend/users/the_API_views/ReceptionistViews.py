from django.db import transaction

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from users.models import Receptionist, HotelManager, Admin

from users.serializers.receptionist_serializer import ReceptionistListSerializer, ReceptionistCreateSerializer


class ReceptionistListCreateAPIView(ListCreateAPIView):
    queryset = Receptionist.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReceptionistCreateSerializer
        else:
            return ReceptionistListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

class ReceptionistRetrieveAPIView(RetrieveAPIView):
    queryset = Receptionist.objects.all()
    serializer_class = ReceptionistListSerializer

    def get_object(self):
        if Receptionist.objects.filter(user=self.request.user).exists():
            return Receptionist.objects.get(user=self.request.user)
        elif HotelManager.objects.filter(user=self.request.user).exists() or Admin.objects.filter(user=self.request.user).exists():
            if Receptionist.objects.filter(id=self.request.query_params.get('receptionist_id')).exists():
                return Receptionist.objects.get(id=self.request.query_params.get('receptionist_id'))