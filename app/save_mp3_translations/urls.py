from django.urls import path
from .views import create_mp3_from_words

urlpatterns = [
    path('wczytaj/', wczytaj_dane, name="wczytaj_dane"),
    # path('wordspairlist/', WordPairsAPIView.as_view(), name='word-pair-list-api-view'),
    # path('randompairs/', RandomWordPairsAPIView.as_view(), name='random-pairs'),
    path('', create_mp3_from_words, name='create-mp3'),
]