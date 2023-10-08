from django.urls import path
from .views import LoginAPIView, LogoutAPIView, AuthAPIOverview


urlpatterns = [
    path('', AuthAPIOverview.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]