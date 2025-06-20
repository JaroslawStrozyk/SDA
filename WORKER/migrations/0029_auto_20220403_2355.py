# Generated by Django 3.1.3 on 2022-04-03 23:55

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0028_auto_20220329_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='premia',
            name='ind_pr_nazwa',
        ),
        migrations.AddField(
            model_name='premia',
            name='pr_wartosc',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Premia za stoisko'),
        ),
        migrations.AddField(
            model_name='premia',
            name='pr_wartosc_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='pensja',
            name='miesiac',
            field=models.IntegerField(default=4, verbose_name='Miesiąc'),
        ),
        migrations.AlterField(
            model_name='podsumowanie',
            name='miesiac',
            field=models.IntegerField(default=4, verbose_name='Miesiąc'),
        ),
        migrations.AlterField(
            model_name='premia',
            name='ind_pr_kwota',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Indywid. premia za projekt'),
        ),
        migrations.AlterField(
            model_name='premia',
            name='miesiac',
            field=models.IntegerField(default=4, verbose_name='Miesiąc'),
        ),
    ]
