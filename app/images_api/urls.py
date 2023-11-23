from django.urls import path
from .views import ImageListCreateAPIView, ImageDetailDestroyAPIView, ExpiringLinkListCreateAPIView

urlpatterns = [
    path('', ImageListCreateAPIView.as_view(), name='images'),
    path('<slug:slug>/expiring/', ExpiringLinkListCreateAPIView.as_view(), name='expiring-list-create'),
    path('<slug:slug>/', ImageDetailDestroyAPIView.as_view(), name='image-detail-destroy'),
]
