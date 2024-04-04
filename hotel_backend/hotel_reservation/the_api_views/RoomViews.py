from rest_framework.generics import ListAPIView
from hotel_reservation.models import Reservation, RoomReservation, Room
from hotel_reservation.serializers.RoomSerializer import RoomListSerializer

from datetime import datetime, timedelta


START_DATE_ROOM_KEY: str = 'room_reservations__reservation__start_date__range'
END_DATE_ROOM_KEY: str = 'room_reservations__reservation__end_date__range'
class RoomListAPIView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer

    def get_queryset(self):
        if self.request.query_params.get('start_date') and self.request.query_params.get('end_date'):
            start_date = datetime.strptime(self.request.get('start_date'), '%d/%m/%Y').date()
            end_date = (datetime.strptime(self.request.get('end_date'), '%d/%m/%Y') - timedelta(days=1)).date()
        else:
            start_date = None
            end_date = None
        filter_dictionary: dict = {
            # 'exclude': {
            #     START_DATE_ROOM_KEY: [start_date, end_date],
            #     END_DATE_ROOM_KEY: [start_date, end_date],
            # },
            'filter': {
                'room_type': self.request.query_params.get('room_type'),
                'size': self.request.query_params.get('size'),
            },
        }
        # filter_dictionary = {{value[k]: v for k, v in value.items() if v is not None} for key, value in filter_dictionary.items()}
        for key, value in filter_dictionary.items():
            for k, v in value.items():
                if v is not None:
                    value[k] = v
        r1 = Room.objects.all()
        return r1




