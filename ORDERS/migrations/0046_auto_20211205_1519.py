# Generated by Django 3.1.3 on 2021-12-05 15:19

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0045_auto_20211205_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='nrsde',
            name='w_cash',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Wartość końcowa koszty gotówkowe'),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='w_cash_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='w_direct',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Wartość końcowa koszty bezpośrednie'),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='w_direct_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
    ]