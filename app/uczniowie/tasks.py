from celery import shared_task
from .models import ParaUczniow, Uczen
import random
from django.db.models import Min, Q

@shared_task(bind=True)
def kombinacja_par(request):
    ParaUczniow.objects.all().update(para_w_tym_tygodniu=False)
    liczba_uczniow = Uczen.objects.all().count()
    liczba_par = int(liczba_uczniow/2)
    kombinacja_par = []
    pary_uczniow = ParaUczniow.objects.filter(Q(uczen_1__imie="Pusty") | Q(uczen_2__imie="Pusty"))
    if len(pary_uczniow) == 0:
        pary_uczniow = ParaUczniow.objects.all()
    najmniejsza_liczba_par = pary_uczniow.aggregate(Min('ile_razy_byla_utworzona'))
    pary_uczniow = pary_uczniow.filter(ile_razy_byla_utworzona__lte=najmniejsza_liczba_par['ile_razy_byla_utworzona__min'])
    pierwsza_para = random.choice(pary_uczniow)
    kombinacja_par.append(pierwsza_para)
    wybrani = [pierwsza_para.uczen_1, pierwsza_para.uczen_2]
    
    for _ in range(liczba_par - 1):
        pary_uczniow = pary_uczniow.exclude(Q(uczen_1__in=wybrani) | Q(uczen_2__in=wybrani))
        nowa_para = random.choice(pary_uczniow)
        wybrani.extend([nowa_para.uczen_1, nowa_para.uczen_2])
        kombinacja_par.append(nowa_para)
        
    for para_wybrana in kombinacja_par:
        para_wybrana.para_w_tym_tygodniu = True
        para_wybrana.save()
    pierwsza_para.ile_razy_byla_utworzona += 1
    pierwsza_para.save()
