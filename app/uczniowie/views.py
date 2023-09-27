from typing import Any
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Uczen, Klasa
from .serializers import UczenSerializer, KlasaSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.views.generic import TemplateView
# Create your views here.

from .models import ParaUczniow

@api_view(['GET'])
def uczniowie_api_overview(request):
    routes = {
            'Lista Uczniów': request.build_absolute_uri(reverse(('lista-uczniow'))),
            # 'Uczeń': request.build_absolute_uri(reverse(('uczen'))),
            # 'Uaktualnij dane ucznia': request.build_absolute_uri(reverse(('uczen-uaktualnij'))),
            # 'Usuń ucznia': request.build_absolute_uri(reverse(('uczen-usun'))),
            'Klasa': request.build_absolute_uri(reverse(('klasa'))),
            'Pary': request.build_absolute_uri(reverse(('plan-pary'))),
    }
    return Response(routes)


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


class KlasaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Klasa.objects.all()
    serializer_class = KlasaSerializer


class ParyView(TemplateView):
    template_name = 'uczniowie/pary_uczniow.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(ParyView, self).get_context_data(**kwargs)
        context['pary'] = ParaUczniow.objects.filter(para_w_tym_tygodniu=True)
        return context 
          
 