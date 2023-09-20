from django.shortcuts import render
from rest_framework import generics
from .models import Uczen
from .serializers import UczenSerializer
# Create your views here.


class UczenListCreateAPIView(generics.ListCreateAPIView):
    queryset = Uczen.objects.all()
    serializer_class = UczenSerializer


class UczenDetailAPIView(generics.RetrieveAPIView):
    queryset = Uczen.objects.all()
    serializer_class = UczenSerializer
    lookup_field = 'pk'


class UczenUpdateAPIView(generics.UpdateAPIView):
    queryset = Uczen.objects.all()
    serializer_class = UczenSerializer
    lookup_field = 'pk'


class UczenDestroyAPIView(generics.DestroyAPIView):
    queryset = Uczen.objects.all()
    serializer_class = UczenSerializer
    lookup_field = 'pk'

