from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users.views import CleanerCreateView

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('cleaner/create/', CleanerCreateView.as_view(), name='cleaner_create')
]