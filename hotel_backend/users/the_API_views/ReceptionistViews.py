from django.db import transaction

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from users.models import Receptionist

from users.serializers.receptionist_serializer import ReceptionistListSerializer, ReceptionistCreateSerializer

class ReceptionistListCreateAPIView(ListCreateAPIView):

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
