# Generated by Django 3.1.3 on 2022-01-12 18:16

from decimal import Decimal
from django.db import migrations, models
import django.utils.timezone
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pracownik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(blank=True, default='', max_length=100, verbose_name='Imię')),
                ('nazwisko', models.CharField(blank=True, default='', max_length=100, verbose_name='Nazwisko')),
                ('grupa', models.CharField(choices=[('BIURO', 'BIURO'), ('PRODUKCJA', 'PRODUKCJA')], default='BIURO', max_length=300, verbose_name='Grupa')),
                ('zatrudnienie', models.CharField(blank=True, choices=[('UMOWA', 'UMOWA'), ('DZIAŁALNOŚĆ', 'DZIAŁALNOŚĆ')], default='', max_length=300, verbose_name='Zatrudnienie')),
                ('wymiar', models.DecimalField(decimal_places=2, default=0.0, max_digits=11, verbose_name='Wymiar zatrudnienia')),
                ('data_zat', models.DateField(default=django.utils.timezone.now, verbose_name='Data zatrudnienia')),
                ('staz', models.IntegerField(default=0, verbose_name='Staż pracy')),
                ('pensja_currency', djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3)),
                ('pensja', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Ustalona pensja')),
                ('uwagi', models.TextField(blank=True, verbose_name='Uwagi')),
            ],
            options={
                'verbose_name': 'Pracownik',
                'verbose_name_plural': 'Pracownicy',
            },
        ),
    ]
