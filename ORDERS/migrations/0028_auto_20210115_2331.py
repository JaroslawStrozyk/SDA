# Generated by Django 3.1.5 on 2021-01-15 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0027_auto_20210115_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='nrsde',
            name='fv',
            field=models.CharField(blank=True, max_length=500, verbose_name='Faktura'),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='klient',
            field=models.CharField(blank=True, max_length=500, verbose_name='Klient'),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='pm',
            field=models.CharField(blank=True, max_length=500, verbose_name='Project Manager'),
        ),
    ]