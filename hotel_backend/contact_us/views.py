from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ContactListSerializer, ContactCreateSerializer
from .models import Contact


# Create your views here.


class ContactCreateAPIView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactCreateSerializer

    def create(self, request, *args, **kwargs):
        response = super(ContactCreateAPIView, self).create(request, *args, **kwargs)
        if response.status in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            pass
            # do something...
        return response


class ContactListAPIView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactListSerializer
