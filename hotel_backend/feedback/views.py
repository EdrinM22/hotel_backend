from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from .models import Feedback
from .serializers import FeedBackCreateSerializer, FeedBackListSerializer

from users.permissions.guest_permissions import GuestOnlyPermission, GuestPermission

from users.models import Guest


# Create your views here.


class FeedbackCreateAPIView(CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedBackCreateSerializer
    permission_classes = [IsAuthenticated, GuestOnlyPermission]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        guest_id = Guest.objects.get(user=request.user).pk
        data_obj = {
            'guest': guest_id,
            **request.data
        }
        serializer_obj: FeedBackCreateSerializer = self.get_serializer(data=data_obj)
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        return Response(serializer_obj.validated_data, status=status.HTTP_201_CREATED)


class FeedbackListAPIView(ListAPIView):
    serializer_class = FeedBackListSerializer
    permission_classes = [IsAuthenticated, GuestPermission]

    def get_queryset(self):
        guest = Guest.objects.get(user=self.request.user) if Guest.objects.filter(user=self.request.user).exists() else self.request.query_params.get('guest')
        s1 = list(filter(lambda x: 'date_time_created' in x, self.request.query_params.keys()))
        data = {}
        for k in s1:
            data[k] = datetime.strptime(self.request.query_params.get(k), '%d/%m/%Y') if self.request.query_params.get(k) else None

        filtered_data = {
            'guest': guest,
            'stars': self.request.query_params.get('stars'),
            'stars__lte': self.request.query_params.get('stars__lte'),
            'stars__gte': self.request.query_params.get('stars__gte'),
            'stars__lt': self.request.query_params.get('stars__lt'),
            'stars__gt': self.request.query_params.get('stars__gt'),
            **data
        }
        final_filter_data = dict({v for k, v in filtered_data.items() if v is not None})
        return Feedback.objects.filter(**final_filter_data)
