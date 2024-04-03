from rest_framework.generics import ListAPIView
from hotel_reservation.models import Reservation, RoomReservation, Room
from hotel_reservation.serializers.RoomSerializer import RoomListSerializer


class RoomListAPIView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer
