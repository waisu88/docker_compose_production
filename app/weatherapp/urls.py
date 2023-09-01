from django.urls import path
from . import views


urlpatterns = [
    path('', views.api_overview, name='api_overview'),
    path('data-list/', views.synoptic_data_list, name='synoptic_data_list'),
    path('single-station/', views.get_single_station_weather, name='single-station'),
    path('by-given-hour/', views.get_all_station_weather_by_given_hour, name='all-station-given-hour'),
]