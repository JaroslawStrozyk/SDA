# Generated by Django 3.1.3 on 2022-02-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0016_auto_20220204_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pensja',
            name='km_ilosc',
            field=models.IntegerField(default=0, verbose_name='Kilometrówka ilość dni'),
        ),
        migrations.AlterField(
            model_name='pracownik',
            name='dystans',
            field=models.IntegerField(default=0, verbose_name='Dystans [km]'),
        ),
    ]