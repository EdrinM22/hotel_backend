from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hotel_reservation.models import Reservation, RoomReservation, Room, RoomType
from hotel_reservation.serializers.RoomSerializer import RoomListSerializer, RoomTypeCustomSerializer, \
    RoomCreateSerializer, RoomtypeListForScrollSerializer
from users.permissions.hotel_manager_permissions import HotelManagerPermissions

from .shared import get_the_room_for_diferent_days, parse_to_date_time_dd_mm_yy_version

from datetime import datetime, timedelta

START_DATE_ROOM_KEY: str = 'room_reservations__reservation__start_date'
END_DATE_ROOM_KEY: str = 'room_reservations__reservation__end_date'


class RoomListAPIView(ListAPIView):
    '''
    For the guests and all. They can check the type of rooms that are free in the dyas wanted
    '''
    queryset = Room.objects.all()
    serializer_class = RoomTypeCustomSerializer

    def get(self, request, *args, **kwargs):
        if self.request.query_params.get('start_date') and self.request.query_params.get('end_date'):
            start_date = datetime.strptime(self.request.query_params.get('start_date'), '%d/%m/%Y').date()
            end_date = (datetime.strptime(self.request.query_params.get('end_date'), '%d/%m/%Y')).date()
            room_query_set = Room.objects.exclude(pk__in=get_the_room_for_diferent_days(start_date, end_date,
                                                                                        self.request.query_params.get(
                                                                                            "room_type")).values_list(
                'id', flat=True))
            room_query_set.order_by('room_type')
        else:
            room_query_set = Room.objects.all().order_by('room_type')
        data_1 = []
        r1 = list(room_query_set)
        count = 0
        for i, elemenet in enumerate(room_query_set):
            if len(list(filter(lambda x: x.get('room_type') == elemenet.room_type, data_1))) == 0:
                data_1.append({
                    'room_type': elemenet.room_type,
                    'room_count': 0,
                })
            data_1[-1]['room_count'] += 1
        serializer_obj: RoomTypeCustomSerializer = self.get_serializer(data_1, many=True) if len(
            data_1) else self.get_serializer(data_1)
        return Response(serializer_obj.data, status=status.HTTP_200_OK)
        #
        # for key, value in filter_dictionary.items():
        #     for k, v in value.items():
        #         if v is not None:
        #             value[k] = v
        # r1 = Room.objects.all()
        # return r1


class RoomAdminListAPIView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer
    '''
    Rooms for the admins or managers
    '''

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        in_these_dates_include = self.request.query_params.get('include')

        if start_date and end_date:
            start_date = parse_to_date_time_dd_mm_yy_version(start_date)
            end_date = parse_to_date_time_dd_mm_yy_version(end_date)
            if in_these_dates_include == True:
                the_wanted_queryset = self.get_queryset_for_given_reservation_dates(start_date, end_date)
                self.filter_the_queryset(the_wanted_queryset)
                return the_wanted_queryset
            elif in_these_dates_include == False:
                the_wanted_queryset = self.get_queryset_for_given_reservation_dates(start_date, end_date)
                self.filter_the_queryset(the_wanted_queryset)
                return the_wanted_queryset
        return self.filter_the_queryset(Room.objects.all())

    def get_queryset_for_given_reservation_dates(self, start_date, end_date):
        return get_the_room_for_diferent_days(start_date, end_date, self.request.query_params.get('room_type'))


    def get_queryset_except_given_reservation_dates(self, start_date, end_date):
        return Room.objects.exclude(pk__in=get_the_room_for_diferent_days(start_date, end_date, self.request.query_params.get('room_type')).values_list('id', flat=True))

    def filter_the_queryset(self, the_query_set):
        filter_dict = {
            'room_type__id': self.request.query_params.get('room_type'),
            'room_type__size': self.request.query_params.get('size'),
            'room_type__price': self.request.query_params.get('price'),
            'clean': self.request.query_params.get('clean')
        }
        return the_query_set.filter(**filter_dict)

class FinanceProfitsListAPIView(ListAPIView):
    pass

class RoomCreateAPIView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer
    permission_classes = [IsAuthenticated, HotelManagerPermissions]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        room_type_id = self.request.data.get('room_type')
        if not RoomType.objects.filter(pk=room_type_id).exists():
            return Response({'message': 'Room Failed'}, status=status.HTTP_400_BAD_REQUEST)
        if Room.objects.filter(room_unique_number=self.request.data.get('room_unique_number')).exists():
            return Response({'message': 'Rooom Already Exists'}, status=status.HTTP_400_BAD_REQUEST)
        room_type = RoomType.objects.get(id=room_type_id)
        data = {
            'online_price': room_type.online_price,
            'real_price': room_type.real_price,
            'size': room_type.size,
            **request.data
        }
        serializer: RoomCreateSerializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomTypeListForScrollerAPIView(ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomtypeListForScrollSerializer
    permission_classes = [IsAuthenticated]

