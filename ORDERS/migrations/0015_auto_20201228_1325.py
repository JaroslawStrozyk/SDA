# Generated by Django 3.1.4 on 2020-12-28 13:25

from django.db import migrations, models
import django.utils.timezone
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0014_nrsde_targi'),
    ]

    operations = [
        migrations.AddField(
            model_name='nrmpk',
            name='rok',
            field=models.IntegerField(default=2020, verbose_name='Rok Nr MPK'),
        ),
        migrations.AddField(
            model_name='nrsde',
            name='rok',
            field=models.IntegerField(default=2020, verbose_name='Rok Nr SDE'),
        ),
        migrations.AddField(
            model_name='zamowienie',
            name='data_fv',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Data faktury'),
        ),
        migrations.AddField(
            model_name='zamowienie',
            name='rok',
            field=models.IntegerField(default=2020, verbose_name='Rok zamówienia'),
        ),
        migrations.AlterField(
            model_name='zamowienie',
            name='kwota_brutto_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='zamowienie',
            name='kwota_netto_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='zamowienie',
            name='wartosc_zam_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='zamowienie',
            name='zal1_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='zamowienie',
            name='zal2_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='zamowienie',
            name='zal3_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
    ]