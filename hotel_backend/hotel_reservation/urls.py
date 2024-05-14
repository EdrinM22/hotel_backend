from django.urls import path, include
from hotel_reservation.the_api_views.ReservationViews import ReservationCreateAPIView, ReservationListAPIVIew
from hotel_reservation.the_api_views.RoomViews import RoomListAPIView, RoomCreateAPIView, \
    RoomTypeListForScrollerAPIView, RoomTypeCreateAPIView, RoomAdminListAPIView
from hotel_reservation.the_api_views.finance_views import RoomTypeFinanceListAPIView

urlpatterns = [
    path('reservation/create/', ReservationCreateAPIView.as_view(), name='Reservation_Create'),
    path('reservation/list/', ReservationListAPIVIew.as_view(), name='Reservation_List'),
    path('rooms/list/', RoomListAPIView.as_view(), name='room_list'),
    path('room/create/', RoomCreateAPIView.as_view(), name='room_create'),
    path('reservation/profit/', RoomTypeFinanceListAPIView.as_view()),
    path('room_type/scroll/list/', RoomTypeListForScrollerAPIView.as_view(), name='room_type_for_Scroll'),
    path('room_type/create/', RoomTypeCreateAPIView.as_view(), name='room_type_create'),
    path('rooms/admin/list/', RoomAdminListAPIView.as_view(), name="Room_Admin_List"),
]