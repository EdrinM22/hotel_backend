from django.db import transaction
from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers.cleaner_serializer import CleanerCreateSerializer
from .models import Cleaner


# Create your the_API_views here.

class CleanerCreateView(CreateAPIView):
    queryset = Cleaner.objects.all()
    serializer_class = CleanerCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Createde!'}, status=status.HTTP_201_CREATED)


def get_user_type_from_retrieve(serializer_class, type, obj):
    if not obj:
        return Response({'message': 'Error, Please write the user you want to get'},status=status.HTTP_400_BAD_REQUEST)
    serializer = serializer_class(obj)
    data = serializer.data
    data['type'] = type
    return Response(data, status=status.HTTP_200_OK)
