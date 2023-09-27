from django.urls import path
from . import views


urlpatterns = [
    path('', views.uczniowie_api_overview, name='uczniowie_api_overview'),
    path('uczen/', views.UczenListCreateAPIView.as_view(), name='lista-uczniow'),
    path('uczen/<int:pk>', views.UczenDetailAPIView.as_view(), name='uczen'),
    path('uczen/<int:pk>/update', views.UczenUpdateAPIView.as_view(), name='uczen-uaktualnij'),
    path('uczen/<int:pk>/delete', views.UczenDestroyAPIView.as_view(), name='uczen-usun'),
    path('klasa/', views.KlasaListCreateAPIView.as_view(), name='klasa'),
    path('pary/', views.ParyView.as_view(), name='plan-pary'),  
]