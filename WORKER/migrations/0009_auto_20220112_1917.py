# Generated by Django 3.1.3 on 2022-01-12 19:17

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0008_auto_20220112_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pracownik',
            name='pensja',
        ),
        migrations.RemoveField(
            model_name='pracownik',
            name='pensja_currency',
        ),
        migrations.AddField(
            model_name='pensja',
            name='pracownik',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.SET_NULL, to='WORKER.pracownik', verbose_name='Pracownik'),
        ),
        migrations.AddField(
            model_name='pracownik',
            name='pensja_ust',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Ustalona pensja'),
        ),
        migrations.AddField(
            model_name='pracownik',
            name='pensja_ust_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
    ]
