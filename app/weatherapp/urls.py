from django.urls import path
from . import views


urlpatterns = [
    path('', views.weather_api_overview, name='api_overview'),
    path('data-list/', views.synoptic_data_list, name='synoptic_data_list'),
    path('single-station/', views.by_given_station, name='single-station'),
    path('by-given-hour/', views.by_given_hour, name='all-station-given-hour'),
]