from django.urls import path
from django.views.generic import TemplateView
from .views import IndexTemplateView

urlpatterns = [
    path('', IndexTemplateView.as_view(), name="index"),
]