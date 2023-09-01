from django.db import models

# Create your models here.
class SynopticData(models.Model):
    id_stacji = models.PositiveIntegerField()
    stacja = models.CharField(max_length=50)
    data_pomiaru = models.DateField(auto_now_add=False)
    godzina_pomiaru = models.PositiveIntegerField()
    temperatura = models.DecimalField(max_digits=3, decimal_places=1)
    predkosc_wiatru = models.PositiveIntegerField()
    kierunek_wiatru = models.PositiveIntegerField()
    wilgotnosc_wzgledna = models.DecimalField(max_digits=4, decimal_places=1)
    suma_opadu = models.DecimalField(max_digits=10, decimal_places=2)
    cisnienie = models.DecimalField(max_digits=5, decimal_places=1)
    utworzony = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stacja}, {self.data_pomiaru}, {self.godzina_pomiaru}"