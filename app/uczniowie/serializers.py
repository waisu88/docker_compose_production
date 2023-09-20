from rest_framework import serializers
from .models import Uczen

class UczenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uczen
        fields = "__all__"