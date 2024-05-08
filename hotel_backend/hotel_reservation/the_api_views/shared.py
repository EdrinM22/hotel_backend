import datetime

from rest_framework.exceptions import ValidationError

from hotel_reservation.models import Room
from django.db.models import Q

from datetime import datetime

#Returns the rooms that are occupied for these dates
def get_the_room_for_diferent_days(start_date, end_date, key=None):
    return Room.objects.filter(
        Q(room_reservations__reservation__start_date__gte=start_date,
          room_reservations__reservation__start_date__lt=end_date) |
        Q(room_reservations__reservation__end_date__gt=start_date,
          room_reservations__reservation__end_date__lte=end_date) |
        Q(room_reservations__reservation__start_date__lte=start_date,
          room_reservations__reservation__end_date__gte=end_date),
        room_type__type_name=key
    ) if key else Room.objects.filter(
        Q(room_reservations__reservation__start_date__gte=start_date,
          room_reservations__reservation__start_date__lt=end_date) |
        Q(room_reservations__reservation__end_date__gt=start_date,
          room_reservations__reservation__end_date__lte=end_date) |
        Q(room_reservations__reservation__start_date__lte=start_date,
          room_reservations__reservation__end_date__gte=end_date))

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

def parse_to_date_time_dd_mm_yy_version(date_in_string: str):
    return datetime.strptime(date_in_string, "%d/%m/%Y").date()

