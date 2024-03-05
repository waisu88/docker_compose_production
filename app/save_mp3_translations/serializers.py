from rest_framework import serializers
from .models import WordsPair

class WordsPairSerializer(serializers.ModelSerializer):
    base_word = serializers.StringRelatedField()
    translated_word = serializers.StringRelatedField()

    class Meta:
        model = WordsPair   
        fields = [
            'base_word',
            'translated_word'
        ]