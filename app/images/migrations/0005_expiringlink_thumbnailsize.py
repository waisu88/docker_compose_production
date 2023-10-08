# Generated by Django 4.2.5 on 2023-10-04 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_alter_grantedtier_account_tier_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiringLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ThumbnailSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_name', models.CharField(max_length=50, unique=True)),
                ('size', models.PositiveIntegerField(unique=True)),
            ],
        ),
    ]
