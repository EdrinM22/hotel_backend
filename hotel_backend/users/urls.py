from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users.views import CleanerCreateView

from users.the_API_views.ReceptionistViews import ReceptionistListCreateAPIView
from users.the_API_views.HotelAdminViews import HotelAdminListCreateAPIView
from users.the_API_views.HotelManager import HotelManagerListCreateAPIView

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('cleaner/create/', CleanerCreateView.as_view(), name='cleaner_create'),
    path('receptionist/create/list/', ReceptionistListCreateAPIView.as_view(), name='receptionist_create'),
    path('manager/create/list/', HotelManagerListCreateAPIView.as_view(), name='admin_create'),
    path('admin/create/list/', HotelAdminListCreateAPIView.as_view(), name='manager_create'),

]