from django.urls import path
from . import views


urlpatterns = [
    path('', views.RemindingMessagesListCreateAPIView.as_view(), name='reminder'),
]