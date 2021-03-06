# Generated by Django 3.1.5 on 2021-01-17 05:23

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0029_auto_20210116_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='nrsde',
            name='c_lp',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Got. Lipiec'),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='c_lp_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='d_lp',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Bezp. Lipiec'),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='d_lp_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
    ]
