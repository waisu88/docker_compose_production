# Generated by Django 4.2.6 on 2023-10-06 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0015_expiringlink_created_at_expiringlink_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expiringlink',
            name='url',
        ),
    ]