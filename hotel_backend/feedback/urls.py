from django.urls import path, include
from .views import FeedbackCreateAPIView, FeedbackListAPIView

urlpatterns = [
    path('create/', FeedbackCreateAPIView.as_view(),),
    path('list/', FeedbackListAPIView.as_view()),
]