from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from hotel_reservation.models import Reservation
from hotel_reservation.serializers.ReservationSerializers import ReservationCreateViaGuestUser, \
    ReservationCreateViaGuestInfo

from users.models import Guest, Receptionist

from hotel_reservation.views import calculate_the_total_cost_of_reservation, create_name_for_reservation


class ReservationCreateAPIView(CreateAPIView):
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_authenticated and Guest.objects.filter(user=self.request.user).exists():
            return ReservationCreateViaGuestUser
        if not self.request.user.is_authenticated or Receptionist.objects.filter(user=self.request.user):
            return ReservationCreateViaGuestInfo

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not self.request.data.get('success') or not self.request.data.get('payment_intent_id'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        total_cost_of_reservation = calculate_the_total_cost_of_reservation(request.data, request)
        name_of_reservation = create_name_for_reservation(request.data) if Guest.objects.filter(user=self.request.user).exists() else create_name_for_reservation(self.request.data, guest_account=False)
        request.data['total_cost'] = total_cost_of_reservation
        request.data['name'] = name_of_reservation
        serializer_obj = self.get_serializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        return Response(serializer_obj.validated_data, status=status.HTTP_201_CREATED)
