from django.db import models

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=250)
    abbrev = models.CharField(max_length=10)


class Word(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.word


class WordsPair(models.Model):
    base_word = models.ForeignKey(Word, related_name='base_word', on_delete=models.CASCADE)
    translated_word = models.ForeignKey(Word, related_name='translated_word', on_delete=models.CASCADE)

    

