from django.urls import path
from .views import RemindingMessagesListCreateAPIView, RemindingMessageDetailAPIView


urlpatterns = [
    path('', RemindingMessagesListCreateAPIView.as_view(), name='reminding-messages-list'),
    path('<int:pk>/', RemindingMessageDetailAPIView.as_view(), name='message-details'),
]