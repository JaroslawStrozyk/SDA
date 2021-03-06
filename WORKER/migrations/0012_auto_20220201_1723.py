# Generated by Django 3.1.3 on 2022-02-01 17:23

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0011_auto_20220130_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='pensja',
            name='brutto_brutto',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Brutto brutto'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='brutto_brutto_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pensja',
            name='del_ilosc_100',
            field=models.IntegerField(default=0, verbose_name='Delega. ilość 100%'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='del_ilosc_50',
            field=models.IntegerField(default=0, verbose_name='Delega. ilość 50%'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='del_ilosc_razem',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Delegacja razem'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='del_ilosc_razem_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pensja',
            name='dodatek_opis',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Opis extra dodatek'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='km_ilosc',
            field=models.IntegerField(default=0, verbose_name='Kilome. ilość dni'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='km_wartosc',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Kilome. wartość'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='km_wartosc_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pensja',
            name='komornik',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Komornik'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='komornik_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pensja',
            name='l4',
            field=models.BooleanField(default=False, verbose_name='L4'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='nadgodz_opis',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Opis nadgodziny'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='obciazenie_opis',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Opis extra obciążenie'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='premia',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Premia'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='premia_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pensja',
            name='razem',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Razem'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='razem_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pensja',
            name='rozliczono',
            field=models.BooleanField(default=False, verbose_name='Rozliczono'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='sum_kosztow',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Suma kosztów'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='sum_kosztow_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pensja',
            name='uwagi',
            field=models.TextField(blank=True, verbose_name='Uwagi'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='wyplata',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Wypłata'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='wyplata_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pensja',
            name='zaliczka',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Zaliczka'),
        ),
        migrations.AddField(
            model_name='pensja',
            name='zaliczka_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pracownik',
            name='dystans',
            field=models.IntegerField(default=0, verbose_name='Kilometry dynstans'),
        ),
        migrations.AlterField(
            model_name='pensja',
            name='dodatek',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Extra dodatek'),
        ),
        migrations.AlterField(
            model_name='pensja',
            name='miesiac',
            field=models.IntegerField(default=2, verbose_name='Miesiąc'),
        ),
        migrations.AlterField(
            model_name='pensja',
            name='obciazenie',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Extra obciążenie'),
        ),
    ]
