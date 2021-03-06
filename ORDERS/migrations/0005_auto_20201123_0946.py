# Generated by Django 3.1.3 on 2020-11-23 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0004_auto_20201120_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zamowienie',
            name='nr_zam',
            field=models.CharField(blank=True, max_length=300, verbose_name='Nr zamówienia'),
        ),
        migrations.AlterField(
            model_name='zamowienie',
            name='rodzaj_plat',
            field=models.CharField(blank=True, choices=[('-', '-'), ('Zaliczka', 'Zaliczka'), ('Proforma', 'Proforma'), ('Zamowienie', 'Zamówienie'), ('Faktura', 'Faktura')], default='-', max_length=100, verbose_name='Rodzaj dokumentu'),
        ),
    ]
