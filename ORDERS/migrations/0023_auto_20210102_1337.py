# Generated by Django 3.1.4 on 2021-01-02 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0022_zamowienie_inicjaly'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zamowienie',
            name='rok',
            field=models.IntegerField(default=0, verbose_name='Rok zamówienia'),
        ),
    ]
