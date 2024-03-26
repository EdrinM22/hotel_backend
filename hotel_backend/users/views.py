from django.db import transaction
from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers.cleaner_serializer import CleanerCreateSerializer
from .models import Cleaner
# Create your views here.

class CleanerCreateView(CreateAPIView):
    queryset = Cleaner.objects.all()
    serializer_class = CleanerCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Createde!'}, status=status.HTTP_201_CREATED)




