# Generated by Django 5.0 on 2024-12-28 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COMP_REPO', '0054_sklad_liczyc'),
    ]

    operations = [
        migrations.AddField(
            model_name='sklad',
            name='ilosc_dni',
            field=models.IntegerField(default=0, verbose_name='Liczba dni'),
        ),
    ]
