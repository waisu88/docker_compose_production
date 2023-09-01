from rest_framework import serializers
from .models import SynopticData

class SynopticDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynopticData
        fields = "__all__"