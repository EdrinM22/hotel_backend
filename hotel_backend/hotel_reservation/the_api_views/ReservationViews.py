from datetime import datetime

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import NotAcceptable, ValidationError

from .paginators import CustomPagination

from hotel_reservation.models import Reservation, Room
from hotel_reservation.serializers.ReservationSerializers import ReservationCreateViaGuestUser, \
    ReservationCreateViaGuestInfo, ReservationListSerializer

from users.models import Guest, Receptionist

from hotel_reservation.views import calculate_the_total_cost_of_reservation, create_name_for_reservation



def get_the_room_for_diferent_days(start_date, end_date, key):
     return Room.objects.filter(
        Q(room_reservations__reservation__start_date__gte=start_date,
          room_reservations__reservation__start_date__lt=end_date) |
        Q(room_reservations__reservation__end_date__gt=start_date,
          room_reservations__reservation__end_date__lte=end_date) |
        Q(room_reservations__reservation__start_date__lte=start_date,
          room_reservations__reservation__end_date__gte=end_date),
        room_type__type_name=key
    )

def check_if_room_is_free(room_types: [], start_date: str, end_date: str):
    for element in room_types:
        query_set_size = len(Room.objects.filter(room_type__type_name=element['name']))

        # reservation_query_set = Reservation.objects.filter(
        #     Q(start_date__gte=start_date, start_date__lt=end_date) |
        #     Q(end_date__gte=start_date,
        #       end_date__lt=end_date) |
        #     Q(start_date__lte=start_date, end_date__gt=end_date),
        #     room_reservations__room__room_type__type_name=key
        # ).values_list('room_reservations__room_id', flat=True)

        room_query_set = get_the_room_for_diferent_days(start_date, end_date, element.get('name'))

        if (len(room_query_set) + element.get('count')) > query_set_size:
            raise ValidationError("No Rooms in these days")



    # def get_id_of_rooms_that_are_free(room_types: ):


class ReservationCreateAPIView(CreateAPIView):
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_authenticated and Guest.objects.filter(user=self.request.user).exists():
            return ReservationCreateViaGuestUser
        if not self.request.user.is_authenticated or Receptionist.objects.filter(user=self.request.user).exists():
            return ReservationCreateViaGuestInfo


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not self.request.data.get('success') or not self.request.data.get('payment_intent_id'):
            return Response({'message': 'What'}, status=status.HTTP_400_BAD_REQUEST)
        total_cost_of_reservation, payment_type = calculate_the_total_cost_of_reservation(request.data, request)

        # name_of_reservation = create_name_for_reservation(request.data) if request.user.is_authenticated and Guest.objects.filter(user=self.request.user).exists() else create_name_for_reservation(self.request.data, guest_account=False)
        # request.data['total_cost'] = total_cost_of_reservation
        # request.data['name'] = name_of_reservation
        the_data = {}
        for k, value in request.data.items():
            if k in ['start_date', 'end_date']:
                the_data[k] = datetime.strptime(value, '%d/%m/%Y').date()
            elif value:
                the_data[k] = value
        check_if_room_is_free(the_data.get('room_types'), the_data.get('start_date'), the_data.get('end_date'))

        # the_data = map(lambda k, v: {k: v[0]}, the_data)
        the_data['total_payment'] = total_cost_of_reservation
        the_data['payment_type'] = payment_type
        serializer_obj = self.get_serializer(data=the_data)
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        return Response(serializer_obj.validated_data, status=status.HTTP_201_CREATED)


class ReservationListAPIVIew(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        query_params = self.request.query_params
        if not query_params.get('start_date') or not query_params.get('end_date'):
            start_date = None
            end_date = None
        else:
            start_date = datetime.strptime(query_params.get('start_date'), '%d/%m/%Y').date()
            end_date = datetime.strptime(query_params.get('end_date'), '%d/%m/%Y').date()
        filter_diction = {
            # 'name__icontains': query_params.get('name', ''),
            'start_date__gte': start_date,
            'start_date__lte': end_date,
            'end_date__gte': start_date,
            'end_date__lte': end_date,
            'paid': query_params.get('paid'),
            'cancelled': query_params.get('cancelled'),
            'payment_type': query_params.get('payment_type')
        }
        filter_diction = {k: v for k, v in filter_diction.items() if v is not None}
        return Reservation.objects.filter(**filter_diction)
