# Generated by Django 5.0 on 2024-01-01 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0071_pracownik_ppk_pracownik_ppk_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pensja',
            name='miesiac',
            field=models.IntegerField(default=1, verbose_name='Miesiąc'),
        ),
        migrations.AlterField(
            model_name='pensja',
            name='rok',
            field=models.IntegerField(default=2024, verbose_name='Rok'),
        ),
        migrations.AlterField(
            model_name='podsumowanie',
            name='miesiac',
            field=models.IntegerField(default=1, verbose_name='Miesiąc'),
        ),
        migrations.AlterField(
            model_name='podsumowanie',
            name='rok',
            field=models.IntegerField(default=2024, verbose_name='Rok'),
        ),
    ]
