# Generated by Django 3.1.3 on 2022-01-12 19:12

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0007_auto_20220112_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pensja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wynagrodzenie_currency', djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3)),
                ('wynagrodzenie', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Wynagrodzenie')),
                ('ppk_currency', djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3)),
                ('ppk', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='PPK')),
                ('przelew_currency', djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3)),
                ('przelew', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Przelew')),
                ('gotowka_currency', djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3)),
                ('gotowka', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Gotówka')),
                ('dodatek_currency', djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3)),
                ('dodatek', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Niestandardowy dodatek')),
                ('obciazenie_currency', djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3)),
                ('obciazenie', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Niestandardowe obciążenie')),
                ('nadgodz_ilosc', models.DecimalField(decimal_places=2, default=0.0, max_digits=11, verbose_name='Ilość nadgodzin')),
                ('nadgodz_currency', djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3)),
                ('nadgodz', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Nadgodziny')),
            ],
            options={
                'verbose_name': 'Pensja',
                'verbose_name_plural': 'Pensje',
            },
        ),
        migrations.AddField(
            model_name='pracownik',
            name='stawka_nadgodz',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Nadgodziny stawka'),
        ),
        migrations.AddField(
            model_name='pracownik',
            name='stawka_nadgodz_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='pracownik',
            name='stawka_wyj',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Wyjazd stawka'),
        ),
        migrations.AddField(
            model_name='pracownik',
            name='stawka_wyj_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
    ]