import pandas as pd
from .models import Language, Word, WordsPair

def wczytaj_dane_z_excela(plik):
    df = pd.read_excel(plik, header=None)

    for index, row in df.iterrows():
        # Sprawdzenie czy wiersz zawiera co najmniej dwie komórki
        if len(row) >= 2:
            slowo_chorwackie = row[0]  # Pierwsza komórka to słowo chorwackie
            slowo_polskie = row[1]      # Druga komórka to słowo polskie

            # Sprawdzenie, czy słowa są niepuste
            if slowo_chorwackie and slowo_polskie:
                # Sprawdzenie czy język chorwacki istnieje w bazie danych
                language_chorwacki, created = Language.objects.get_or_create(name='Chorwacki', abbrev='hr')
                # Sprawdzenie czy język polski istnieje w bazie danych
                language_polski, created = Language.objects.get_or_create(name='Polski', abbrev='pl')

                # Tworzenie obiektu Word dla słowa chorwackiego
                word_chorwackie, created = Word.objects.get_or_create(language=language_chorwacki, word=slowo_chorwackie)
                # Tworzenie obiektu Word dla słowa polskiego
                word_polskie, created = Word.objects.get_or_create(language=language_polski, word=slowo_polskie)

                # Tworzenie obiektu WordsPair i zapisanie go do bazy danych
                words_pair = WordsPair(base_word=word_chorwackie, translated_word=word_polskie)
                words_pair.save()

# Wywołanie funkcji, podając ścieżkę do pliku Excel
wczytaj_dane_z_excela('sciezka/do/pliku.xlsx')