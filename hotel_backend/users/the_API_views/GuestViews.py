from django.db import transaction
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework.response import Response

from users.serializers.guest_serializer import GuestListSerializer, GuestCreateSerializer

from users.models import Guest


class GuestListCreateAPIView(ListCreateAPIView):
    queryset = Guest.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GuestCreateSerializer
        else:
            return GuestListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Guest Created'}, status=status.HTTP_201_CREATED)
