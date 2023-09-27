from rest_framework import serializers
from .models import Uczen, Klasa

class UczenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uczen
        fields = "__all__"


class KlasaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klasa
        fields = "__all__"