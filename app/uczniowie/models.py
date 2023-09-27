from django.db import models
from itertools import combinations
from django.db.models import Min
# Create your models here.
import random
from django.db.models import Q


class Klasa(models.Model):
    numer_klasy = models.CharField(max_length=10, unique=True)
    rok = models.PositiveIntegerField()


    def __str__(self):
        return self.numer_klasy


class Uczen(models.Model):
    imie = models.CharField(max_length=20, unique=True)
    klasa = models.ForeignKey(Klasa, on_delete=models.CASCADE)


    def __str__(self):
        return self.imie


class ParaUczniow(models.Model):
    uczen_1 = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='uczen_1')
    uczen_2 = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='uczen_2')
    ile_razy_byla_utworzona = models.PositiveIntegerField(default=0, blank=True, null=True)
    para_w_tym_tygodniu = models.BooleanField(default=False)

    def __str__(self):
        return self.uczen_1.imie + " + " + self.uczen_2.imie

    def tworz_pary(self):
        uczniowie = Uczen.objects.all()
        lista_uczniow = [uczen.imie for uczen in uczniowie]
        sortowane_pary = [sorted(pair) for pair in combinations(lista_uczniow, 2)]
        for para in sortowane_pary:
            ParaUczniow.objects.create(uczen_1=Uczen.objects.get(imie=para[0]), uczen_2=Uczen.objects.get(imie=para[1]))    


class KombinacjaPar(models.Model):
    kombinacja = models.CharField(max_length=300)

    
    def komb_par(self):
        ParaUczniow.objects.all().update(para_w_tym_tygodniu=False)
        ile_par = int(Uczen.objects.all().count()/2)
        
        kompilacja_par = []
        pary_uczniow = ParaUczniow.objects.filter(Q(uczen_1__imie="Pusty") | Q(uczen_2__imie="Pusty"))
        licznik = pary_uczniow.aggregate(Min('ile_razy_byla_utworzona'))
        pary_uczniow = pary_uczniow.filter(ile_razy_byla_utworzona__lte=licznik['ile_razy_byla_utworzona__min'])
        para = random.choice(pary_uczniow)
        kompilacja_par.append(para)
        wybrani = [para.uczen_1, para.uczen_2]
        pary_uczniow = ParaUczniow.objects.exclude(Q(uczen_1__in=wybrani) | Q(uczen_2__in=wybrani))

        for _ in range(ile_par - 1):
            nowa_para = random.choice(pary_uczniow)
            kompilacja_par.append(nowa_para)
            wybrani.extend([nowa_para.uczen_1, nowa_para.uczen_2])
            pary_uczniow = pary_uczniow.exclude(Q(uczen_1__in=wybrani) | Q(uczen_2__in=wybrani))
        for para_wybrana in kompilacja_par:
            para_wybrana.para_w_tym_tygodniu = True
            para_wybrana.save()
        para.ile_razy_byla_utworzona += 1
        para.save()
        print(kompilacja_par)

        wybrani = ParaUczniow.objects.filter(para_w_tym_tygodniu=True)
        print(wybrani)


