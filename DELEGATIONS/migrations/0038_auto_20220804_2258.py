# Generated by Django 3.1.3 on 2022-08-04 22:58

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('DELEGATIONS', '0037_auto_20220804_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='delegacja',
            name='koszt_paliwo_kr',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Koszt paliwa kraj'),
        ),
        migrations.AddField(
            model_name='delegacja',
            name='koszt_paliwo_kr_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='delegacja',
            name='koszt_paliwo_za',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Koszt paliwa świat'),
        ),
        migrations.AddField(
            model_name='delegacja',
            name='koszt_paliwo_za_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
    ]
