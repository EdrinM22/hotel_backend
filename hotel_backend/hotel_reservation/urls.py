from django.urls import path, include
from hotel_reservation.the_api_views.ReservationViews import ReservationCreateAPIView, ReservationListAPIVIew
from hotel_reservation.the_api_views.RoomViews import RoomListAPIView

urlpatterns = [
    path('reservation/create/', ReservationCreateAPIView.as_view(), name='Reservation_Create'),
    path('reservation/list/', ReservationListAPIVIew.as_view(), name='Reservation_List'),
    path('rooms/list/', RoomListAPIView.as_view(), name='room_list'),
]