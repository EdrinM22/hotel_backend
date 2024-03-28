from django.db import transaction
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework.response import Response

from users.serializers.cleaner_serializer import CleanerListSerializer, CleanerCreateSerializer

from users.models import Cleaner


class CleanerCreateListAPIView(ListCreateAPIView):

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
