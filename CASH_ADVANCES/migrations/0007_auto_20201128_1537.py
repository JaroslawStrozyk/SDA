# Generated by Django 3.1.3 on 2020-11-28 15:37

from decimal import Decimal
from django.db import migrations, models
import django.utils.timezone
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('CASH_ADVANCES', '0006_auto_20201128_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rozliczenie',
            name='data_roz',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Data rozliczenia'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='kontrola',
            field=models.IntegerField(blank=True, default=0, verbose_name='Kontrola'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='kw',
            field=models.CharField(blank=True, max_length=300, verbose_name='Nr KW'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='rok',
            field=models.IntegerField(blank=True, default=0, verbose_name='Rok'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='saldo',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Saldo'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='zal1_data',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Data zaliczki 1'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='zal1_kwota',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Kwota zaliczki 1'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='zal2_data',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Data zaliczki 2'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='zal2_kwota',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Kwota zaliczki 2'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='zal3_data',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Data zaliczki 3'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='zal3_kwota',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Kwota zaliczki 3'),
        ),
        migrations.AlterField(
            model_name='rozliczenie',
            name='zal_suma',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Suma zaliczek'),
        ),
    ]
