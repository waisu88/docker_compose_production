# Generated by Django 4.2.11 on 2024-03-19 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('save_mp3_translations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordspair',
            name='base_word_sentence',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='wordspair',
            name='translated_word_sentence',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]