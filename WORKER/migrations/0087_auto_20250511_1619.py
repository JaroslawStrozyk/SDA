# Generated by Django 3.1.3 on 2025-05-11 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0086_auto_20250401_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pensja',
            name='miesiac',
            field=models.IntegerField(default=5, verbose_name='Miesiąc'),
        ),
        migrations.AlterField(
            model_name='podsumowanie',
            name='miesiac',
            field=models.IntegerField(default=5, verbose_name='Miesiąc'),
        ),
    ]
