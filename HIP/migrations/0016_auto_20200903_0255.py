# Generated by Django 2.2.3 on 2020-09-03 02:55

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('HIP', '0015_auto_20200830_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprzet',
            name='stan',
            field=models.DecimalField(choices=[(-1, '-----'), (0, 'DO KASACJI LUB USZKODZONY.'), (1, 'DOSTATECZNY.'), (2, 'DOBRY.'), (3, 'BARDZO DOBRY.'), (4, 'BARDZO DOBRY Z GWARANCJĄ.')], decimal_places=0, default=-1, max_digits=4, verbose_name='Stan sprzętu'),
        ),
        migrations.AlterField(
            model_name='sprzet',
            name='wartosc',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Wartość sprzętu'),
        ),
    ]
