# Generated by Django 3.1.3 on 2022-02-03 11:48

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0012_auto_20220201_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pensja',
            name='wyplata',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Wypłata'),
        ),
    ]
