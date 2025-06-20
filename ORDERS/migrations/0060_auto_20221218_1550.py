# Generated by Django 3.1.3 on 2022-12-18 15:50

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0059_auto_20221116_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='nrsde',
            name='magazyn_dre',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Magazyny drewna'),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='magazyn_dre_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='magazyn_wewn',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Magazyn wewnętrzny'),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='magazyn_wewn_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='nrsde',
            name='pm',
            field=models.CharField(blank=True, choices=[('Agnieszka Skóra', 'Agnieszka Skóra'), ('Julia Królak', 'Julia Królak'), ('Agnieszka Kaźmierska', 'Agnieszka Kaźmierska'), ('Patryk Chodecki', 'Patryk Chodecki'), ('Dariusz Kaczmarek', 'Dariusz Kaczmarek'), ('Łukasz Jerzmanowski', 'Łukasz Jerzmanowski'), ('Michał Ogrzewalski', 'Michał Ogrzewalski'), ('Marzena Michalska', 'Marzena Michalska'), ('Łukasz Zaremba', 'Łukasz Zaremba'), ('Joanna Dittmar', 'Joanna Dittmar'), ('Adam Beim', 'Adam Beim'), ('Eryk Przybyłowicz', 'Eryk Przybyłowicz'), ('Małgosia Świadek', 'Małgorzata Świadek')], default='', max_length=500, verbose_name='Project Manager'),
        ),
    ]
