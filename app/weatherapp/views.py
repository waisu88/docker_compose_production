from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .models import SynopticData
from .serializers import SynopticDataSerializer
from rest_framework.reverse import reverse
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend




@api_view(['GET'])
def api_overview(request):
    routes = {
            'List': request.build_absolute_uri(reverse(('synoptic_data_list'))),
            'Single station': request.build_absolute_uri(reverse(('single-station'))),
            'By-hour': request.build_absolute_uri(reverse(('all-station-given-hour'))),
    }
    return Response(routes)


class SynopticDataList(generics.ListAPIView):
    queryset = SynopticData.objects.all()
    serializer_class = SynopticDataSerializer
    
synoptic_data_list = SynopticDataList.as_view()


class StationSynopticDataList(generics.ListAPIView):
    queryset = SynopticData.objects.all()
    serializer_class = SynopticDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['stacja']

by_given_station = StationSynopticDataList.as_view()


class HourSynopticDataList(generics.ListAPIView):
    queryset = SynopticData.objects.all()
    serializer_class = SynopticDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['godzina_pomiaru']

by_given_hour = HourSynopticDataList.as_view()




# @api_view(['GET'])
# def synoptic_data_list(request):
#     synoptic_data = SynopticData.objects.all()
#     serializer = SynopticDataSerializer(synoptic_data, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
def get_single_station_weather(request):
    stacja = request.data["stacja"]
    data_pomiaru = request.data["data_pomiaru"]
    synoptic_data = SynopticData.objects.filter(stacja=stacja, data_pomiaru=data_pomiaru)
    serializer = SynopticDataSerializer(synoptic_data, many=True)
    return Response(serializer.data)

    
@api_view(['GET'])
def get_all_station_weather_by_given_hour(request):
    data_pomiaru = request.data["data_pomiaru"]
    godzina_pomiaru = request.data["godzina_pomiaru"]
    synoptic_data = SynopticData.objects.filter(data_pomiaru=data_pomiaru, godzina_pomiaru=godzina_pomiaru)
    serializer = SynopticDataSerializer(synoptic_data, many=True)
    return Response(serializer.data)