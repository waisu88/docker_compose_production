from celery import shared_task
from .serializers import SynopticDataSerializer
from .models import SynopticData
from urllib.request import urlopen
import json

            


@shared_task(bind=True)
def get_api_data(request):
    url = "https://danepubliczne.imgw.pl/api/data/synop"
    response = urlopen(url)  
    data_json = json.load(response)
    total_response = []
    for station_record in data_json:
        serializer = SynopticDataSerializer(data=station_record)
        if serializer.is_valid():
            try:
                existing_data = SynopticData.objects.all().filter(
                    stacja=serializer.validated_data['stacja'], 
                    data_pomiaru=serializer.validated_data['data_pomiaru'], 
                    godzina_pomiaru=serializer.validated_data['godzina_pomiaru'])                  
            except SynopticData.DoesNotExist:
                print("jeszcze nie ma takiego rekordu")
            finally:
                if existing_data:
                    single_response = ({"messsage": f"Jest już zapisany rekord dla stacji {serializer.validated_data['stacja']} \
                                z dnia {serializer.validated_data['data_pomiaru']} \
                                z godziny {serializer.validated_data['godzina_pomiaru']}"})

                    total_response.append(single_response)
                else:
                    serializer.save()
                    total_response.append(serializer.data)