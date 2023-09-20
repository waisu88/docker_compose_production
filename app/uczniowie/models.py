from django.db import models
from itertools import combinations
import random

# Create your models here.
class Uczen(models.Model):
    imie = models.CharField(max_length=20)


class KombinacjaParUczniow(models.Model):
    lista = models.CharField(max_length=420)

    def sk(self):
        lista_uczniow = [obj.imie for obj in Uczen.objects.all()]
        item = lista_uczniow.pop(random.randint(0, len(lista_uczniow))-1)
  
        print(item)

