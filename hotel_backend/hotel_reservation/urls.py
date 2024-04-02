from django.urls import path, include
from hotel_reservation.the_api_views.ReservationViews import ReservationCreateAPIView
urlpatterns = [
    path('reservation/create/', ReservationCreateAPIView.as_view(), name='Reservation_Create')
]