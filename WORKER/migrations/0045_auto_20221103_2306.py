# Generated by Django 3.1.3 on 2022-11-03 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0044_auto_20221008_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pensja',
            name='miesiac',
            field=models.IntegerField(default=11, verbose_name='Miesiąc'),
        ),
        migrations.AlterField(
            model_name='podsumowanie',
            name='miesiac',
            field=models.IntegerField(default=11, verbose_name='Miesiąc'),
        ),
    ]
