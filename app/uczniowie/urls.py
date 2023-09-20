from django.urls import path
from . import views


urlpatterns = [
    path('', views.UczenListCreateAPIView.as_view()),
    path('<int:pk>', views.UczenDetailAPIView.as_view()),
    path('<int:pk>/update', views.UczenUpdateAPIView.as_view()),
    path('<int:pk>/delete', views.UczenDestroyAPIView.as_view()),
]