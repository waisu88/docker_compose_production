from django.urls import path
from . import views


urlpatterns = [
    path('', views.RemindingMessagesListCreateAPIView.as_view(), name='reminding-messages-list'),
    path('<int:pk>/', views.RemindingMessageDetailAPIView.as_view(), name='message-details'),
]