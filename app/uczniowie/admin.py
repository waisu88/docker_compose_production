from django.contrib import admin
from .models import Uczen, ParaUczniow, KombinacjaPar
# Register your models here.

admin.site.register((Uczen, ParaUczniow, KombinacjaPar, ))