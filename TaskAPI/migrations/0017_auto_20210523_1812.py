# Generated by Django 3.1.3 on 2021-05-23 18:12

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAPI', '0016_auto_20210523_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waluta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tab', models.CharField(max_length=50, verbose_name='TABELA')),
                ('kod', models.CharField(max_length=10, verbose_name='KOD')),
                ('poz', models.CharField(default='', max_length=10, verbose_name='POZYCJA')),
                ('data', models.CharField(max_length=50, verbose_name='DATA')),
                ('opis', models.CharField(default='', max_length=50, verbose_name='OPIS')),
                ('kurs_currency', djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3)),
                ('kurs', djmoney.models.fields.MoneyField(decimal_places=4, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='KURS')),
            ],
            options={
                'verbose_name': 'Waluta',
                'verbose_name_plural': 'Waluty',
            },
        ),
        migrations.DeleteModel(
            name='WalutaNBP',
        ),
    ]