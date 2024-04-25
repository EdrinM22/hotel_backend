from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from hotel_reservation.models import Reservation, RoomReservation, Room
from hotel_reservation.serializers.RoomSerializer import RoomListSerializer, RoomTypeCustomSerializer

from .shared import get_the_room_for_diferent_days, parse_to_date_time_dd_mm_yy_version

from datetime import datetime, timedelta

START_DATE_ROOM_KEY: str = 'room_reservations__reservation__start_date'
END_DATE_ROOM_KEY: str = 'room_reservations__reservation__end_date'


class RoomListAPIView(ListAPIView):
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

    def get_queryset_for_given_reservation_dates(self, start_date, end_date):
        return get_the_room_for_diferent_days(start_date, end_date, self.request.query_params.get('room_type'))


    def get_queryset_except_given_reservation_dates(self, start_date, end_date):
        return Room.objects.exclude(pk__in=get_the_room_for_diferent_days(start_date, end_date, self.request.query_params.get('room_type')).values_list('id', flat=True))

    def filter_the_queryset(self, query_set):
        filter_dict = {
            ''
        }