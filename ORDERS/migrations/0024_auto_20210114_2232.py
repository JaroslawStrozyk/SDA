# Generated by Django 3.1.5 on 2021-01-14 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0023_auto_20210102_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zamowienie',
            name='rodzaj_plat',
            field=models.CharField(blank=True, choices=[('Zaliczka', 'Zaliczka'), ('Proforma', 'Proforma'), ('Zamowienie', 'Zamówienie'), ('Faktura', 'Faktura'), ('Korekta', 'Korekta'), ('Nota', 'Nota')], default='-', max_length=100, verbose_name='Rodzaj dokumentu'),
        ),
    ]