# Generated by Django 2.2.3 on 2020-06-28 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HIP', '0008_sprzet_mag'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprzet',
            name='historia',
            field=models.CharField(blank=True, max_length=200, verbose_name='Historia'),
        ),
        migrations.AddField(
            model_name='sprzet',
            name='opis',
            field=models.CharField(blank=True, max_length=200, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='sprzet',
            name='stan',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=3, verbose_name='Stan sprzętu'),
        ),
    ]
