# Generated by Django 4.2.4 on 2023-09-01 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SynopticData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_stacji', models.PositiveIntegerField()),
                ('stacja', models.CharField(max_length=50)),
                ('data_pomiaru', models.DateField()),
                ('godzina_pomiaru', models.PositiveIntegerField()),
                ('temperatura', models.DecimalField(decimal_places=1, max_digits=3)),
                ('predkosc_wiatru', models.PositiveIntegerField()),
                ('kierunek_wiatru', models.PositiveIntegerField()),
                ('wilgotnosc_wzgledna', models.DecimalField(decimal_places=1, max_digits=4)),
                ('suma_opadu', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cisnienie', models.DecimalField(decimal_places=1, max_digits=5)),
                ('utworzony', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]