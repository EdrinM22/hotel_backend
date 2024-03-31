from django.shortcuts import render
import stripe
from datetime import datetime
from .models import Room

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from users.models import Guest, Receptionist

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your the_api_views here.

def calculate_the_total_cost_of_reservation(data, request: Request):
    start_date = datetime.strptime(data.get('start_date'), '%d/%m/%Y')
    end_date = datetime.strptime(data.get('end_date'), '%d/%m/%Y')
    difference_days = end_date - start_date
    room_queryset = Room.objects.filter(pk__in=data.get('room_ids', []))
    if not request.user.is_authenticated or Guest.objects.filter(user=request.user).exists():
        total_price = sum(room_queryset.values_list('online_price', flat=True) * difference_days)
    elif Receptionist.objects.filter(user=request.user).exists():
        total_price = sum(room_queryset.values('real_price', flat=True) * difference_days)
    else:
        raise ValueError('No total_price_found')
    return total_price


def create_name_for_reservation(data, guest_account=True):
    if guest_account:
        guest = Guest.objects.get(id=data.get('guest_id'))
        name_for_reservation = data.get('applying_date') + ' ' + guest.user.first_name + ' ' + guest.user.last_name
    else:
        guest_info = data.get('guest_information')
        name_for_reservation = data.get('applying_date') + ' ' + guest_info.get('first_name') + guest_info.get(
            'last_name')

    return name_for_reservation


class PaymentIntentAPIView(APIView):

    def post(self, request):
        try:
            total_amount = calculate_the_total_cost_of_reservation(self.request.data)
            payment_intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency='eur',
                payment_method_types=['card']
            )
            return Response({
                'id': payment_intent.id,
                'client_secret': payment_intent.client_secret
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
