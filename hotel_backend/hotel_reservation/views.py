from django.shortcuts import render
import stripe
from datetime import datetime
from .models import Room

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

def calculate_the_total_cost_of_reservation(data):
    start_date = datetime.strptime(data.get('start_date'), '%d/%m/%Y')
    end_date = datetime.strptime(data.get('end_date'), '%d/%m/%Y')
    difference_days = end_date - start_date
    room_queryset = Room.objects.filter(pk__in=data.get('room_ids'))
    total_price = sum(room_queryset.values_list('price', flat=True) * difference_days)
    return total_price


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

