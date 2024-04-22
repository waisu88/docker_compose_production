import os
import pandas as pd
from .models import Language, Word, WordsPair
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import WordsPairSerializer
from .forms import MP3Form
from googletrans import Translator
from io import BytesIO
import re

from gtts import gTTS
from pydub import AudioSegment
import csv


@api_view(['POST', 'GET'])
def create_mp3_from_words(request):
    if request.method == 'POST':
        print("WESzło do view")
        form = MP3Form(request.POST)
        if form.is_valid():
            text = form.cleaned_data['words']
            sentences = re.split(r'[.!?]', text)
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

            enter_language = form.cleaned_data['enter_language']
            destination_language = form.cleaned_data['destination_language']
       
            final_audio = None
            translator = Translator()

            for sentence in sentences:
                enter_audio_io = BytesIO()
                translated_audio_io = BytesIO()
                try:
                    translated_text = translator.translate(sentence, src=enter_language, dest=destination_language).text

                    tts_enter = gTTS(sentence, lang=enter_language)
                    tts_enter.write_to_fp(enter_audio_io)

                    tts_dest = gTTS(translated_text, lang=destination_language)
                    tts_dest.write_to_fp(translated_audio_io)

                except Exception as e:
                    # print the exception to command
                    print("An error occurred: %s", e)
                enter_audio_io.seek(0)
                translated_audio_io.seek(0)

                enter_audio = AudioSegment.from_file(enter_audio_io, format="mp3")
                translated_audio = AudioSegment.from_file(translated_audio_io, format="mp3")
                empty_segment_duration_multiplier = len(sentence) // 10
                duration = 1000 * empty_segment_duration_multiplier
                if duration < 2001:
                    duration = 2500
                if duration > 7000:
                    duration = 7000
                empty_segment = AudioSegment.silent(duration=duration)
                if final_audio:
                    final_audio += enter_audio + translated_audio + empty_segment
                else:
                    final_audio = enter_audio + translated_audio + empty_segment

            audio_io = BytesIO()
            final_audio.export(audio_io, format="mp3")
            audio_io.seek(0)

            response = HttpResponse(audio_io, content_type='audio/mp3')
            # final_audio.export(response, format="mp3")
            response['Content-Disposition'] = 'attachment; filename="generated.mp3"'
            return response
    else:
        form = MP3Form()
        max_length = form.fields['words'].max_length

    return render(request, 'mp3translations.html', {'form': form, 'max_length': max_length})


def wczytaj_dane(request):
    biezacy_katalog = os.path.dirname(os.path.abspath(__file__))
    # Utworzenie ścieżki do pliku Excel
    sciezka_do_pliku_excel = os.path.join(biezacy_katalog, 'to_load', 'Czasowniki.xlsx')
    df = pd.read_excel(sciezka_do_pliku_excel, header=None)
    print(df)

    for _, row in df.items():
        for index, (column_name, value) in enumerate(row.items()):
    # Check if the value and the next value (if exists) are not null
            if not pd.isnull(value) and (index + 1 < len(row)):  # Check if index+1 is within range
                _, next_value = list(row.items())[index + 1]  # Get the next value
                if not pd.isnull(next_value):
                    # print("Both current and next values are not null.")
                    print(value, "   ", next_value, type(value))
                    language_chorwacki, created = Language.objects.get_or_create(name='Chorwacki', abbrev='hr')
                # Sprawdzenie czy język polski istnieje w bazie danych
                    language_polski, created = Language.objects.get_or_create(name='Polski', abbrev='pl')
                    # Tworzenie obiektu Word dla słowa chorwackiego
                    word_chorwackie, created = Word.objects.get_or_create(language=language_chorwacki, word=value)
                    # Tworzenie obiektu Word dla słowa polskiego
                    word_polskie, created = Word.objects.get_or_create(language=language_polski, word=next_value)

                    # Tworzenie obiektu WordsPair i zapisanie go do bazy danych
                    words_pair = WordsPair(base_word=word_chorwackie, translated_word=word_polskie)
                    words_pair.save()
                else:
                    pass

    return HttpResponse("<h1>Page was found</h1>")


class WordPairsAPIView(generics.ListAPIView):
    queryset = WordsPair.objects.all()
    serializer_class = WordsPairSerializer



def export_wordpairs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="wordpairs.csv"'

    writer = csv.writer(response)
    writer.writerow(['base_word', 'translated_word', 'translated_word_sentence'])

    wordpairs = WordsPair.objects.all().values_list('base_word', 'translated_word', 'translated_word_sentence')
    for wordpair in wordpairs:
        writer.writerow(wordpair)

    return response



# class RandomWordPairsAPIView(generics.ListAPIView):
    # serializer_class = WordsPairSerializer

    # def get_queryset(self):
    #     queryset = WordsPair.objects.all()
    #     counter = WordsPair.objects.count()
    #     sublist_number = 20

    #     items_per_sublist = counter // sublist_number
    #     print(counter)
    #     print(items_per_sublist)

    #     iterator = 0
    #     przeskok = 25
    #     empty_segment = AudioSegment.silent(duration=2500)
    #     outerator = 0
    #     # for i in range(3):
    #     while outerator < counter:
    #         outerator = iterator + przeskok
    #         if outerator > counter:
    #             outerator = counter

    #         sublist_queryset = queryset[iterator:outerator]
    #         final_audio = None
            

    #         for wordspair in sublist_queryset:
    #             tts_pl = gTTS(wordspair.translated_word.word, lang='pl')
    #             tts_hr = gTTS(wordspair.base_word.word, lang='hr')
    #             # with open(f"{wordspair.translated_word.word}-{wordspair.base_word.word}.mp3", 'wb') as f:
    #             #     tts_pl.write_to_fp(f)
    #             #     tts_hr.write_to_fp(f)

    #             # Save translations to temporary files
    #             tts_pl.save("pl1.mp3")
    #             tts_hr.save("hr1.mp3")

    #             # Load translations as audio segments
    #             audio_pl = AudioSegment.from_mp3("pl1.mp3")
    #             audio_hr = AudioSegment.from_mp3("hr1.mp3")
    #             # Concatenate empty audio with translations
    #             if final_audio:
    #                 final_audio += audio_pl
    #                 final_audio += audio_hr
    #                 final_audio += empty_segment
    #             else:
    #                 final_audio = audio_pl + audio_hr + empty_segment
    #             # final_audio += audio_pl
    #             # final_audio += audio_hr
    #             # final_audio += empty_segment
    #             # Concatenate empty audio with translations
    #             #  Export concatenated audio to file
    #         final_audio.export(f"glosowka-{iterator}.mp3", format="mp3")
    #         iterator = outerator
    #     return queryset


