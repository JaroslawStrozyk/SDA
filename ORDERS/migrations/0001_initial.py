# Generated by Django 3.1.3 on 2020-11-18 16:18

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NrMPK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(blank=True, max_length=250, verbose_name='Nazwa')),
                ('uwagi', models.TextField(blank=True, verbose_name='Uwagi')),
            ],
            options={
                'verbose_name': 'Numer MPK',
                'verbose_name_plural': 'Numery MPK',
            },
        ),
        migrations.CreateModel(
            name='NrSDE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(blank=True, max_length=250, verbose_name='Nazwa')),
                ('uwagi', models.TextField(blank=True, verbose_name='Uwagi')),
            ],
            options={
                'verbose_name': 'Numer SDE',
                'verbose_name_plural': 'Numery SDE',
            },
        ),
        migrations.CreateModel(
            name='Zamowienie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opis', models.CharField(max_length=300, verbose_name='Opis zamówienia')),
                ('kontrahent', models.CharField(max_length=300, verbose_name='Kontrahent')),
                ('wartosc_zam_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'Dolar\xa0Amerykański'), ('EUR', 'Euro'), ('CHF', 'Frank Szwajcarski'), ('GBP', 'Funt Brytyjski'), ('PLN', 'Złoty Polski Nowy')], default='PLN', editable=False, max_length=3)),
                ('wartosc_zam', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Wartość zamówienia')),
                ('nr_zam', models.CharField(max_length=300, verbose_name='Nr zamówienia')),
                ('sposob_plat', models.CharField(choices=[('-', '-'), ('Przelew', 'Przelew'), ('Karta', 'Karta'), ('Gotówka', 'Gotówka')], default='-', max_length=100, verbose_name='Sposób płatności')),
                ('rodzaj_plat', models.CharField(choices=[('-', '-'), ('Zaliczka', 'Zaliczka'), ('Proforma', 'Proforma')], default='-', max_length=100, verbose_name='Rodzaj platności')),
                ('nr_dok1', models.CharField(max_length=100, verbose_name='Nr dokumentu 1')),
                ('zal1_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'Dolar\xa0Amerykański'), ('EUR', 'Euro'), ('CHF', 'Frank Szwajcarski'), ('GBP', 'Funt Brytyjski'), ('PLN', 'Złoty Polski Nowy')], default='PLN', editable=False, max_length=3)),
                ('zal1', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Zal 1/proforma')),
                ('nr_dok2', models.CharField(max_length=100, verbose_name='Nr dokumentu 2')),
                ('zal2_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'Dolar\xa0Amerykański'), ('EUR', 'Euro'), ('CHF', 'Frank Szwajcarski'), ('GBP', 'Funt Brytyjski'), ('PLN', 'Złoty Polski Nowy')], default='PLN', editable=False, max_length=3)),
                ('zal2', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Zaliczka 2')),
                ('nr_dok3', models.CharField(max_length=100, verbose_name='Nr FV rozlicz.')),
                ('zal3_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'Dolar\xa0Amerykański'), ('EUR', 'Euro'), ('CHF', 'Frank Szwajcarski'), ('GBP', 'Funt Brytyjski'), ('PLN', 'Złoty Polski Nowy')], default='PLN', editable=False, max_length=3)),
                ('zal3', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='FV rozliczająca')),
                ('kwota_netto_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'Dolar\xa0Amerykański'), ('EUR', 'Euro'), ('CHF', 'Frank Szwajcarski'), ('GBP', 'Funt Brytyjski'), ('PLN', 'Złoty Polski Nowy')], default='PLN', editable=False, max_length=3)),
                ('kwota_netto', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Kwota netto')),
                ('kwota_brutto_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'Dolar\xa0Amerykański'), ('EUR', 'Euro'), ('CHF', 'Frank Szwajcarski'), ('GBP', 'Funt Brytyjski'), ('PLN', 'Złoty Polski Nowy')], default='PLN', editable=False, max_length=3)),
                ('kwota_brutto', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Kwota brutto')),
                ('data_zam', models.DateField(default=django.utils.timezone.now, verbose_name='Data zamówienia')),
                ('data_dost', models.DateField(default=django.utils.timezone.now, verbose_name='Data dostawy')),
                ('nr_fv', models.CharField(max_length=100, verbose_name='Nr faktury')),
                ('data_przeka', models.DateField(default=django.utils.timezone.now, verbose_name='Data przekazania księgowej')),
                ('kontrola_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'Dolar\xa0Amerykański'), ('EUR', 'Euro'), ('CHF', 'Frank Szwajcarski'), ('GBP', 'Funt Brytyjski'), ('PLN', 'Złoty Polski Nowy')], default='PLN', editable=False, max_length=3)),
                ('kontrola', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=11, verbose_name='Kontrola')),
                ('nr_mpk', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to='ORDERS.nrmpk', verbose_name='Nr MPK')),
                ('nr_sde', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to='ORDERS.nrsde', verbose_name='Nr SDE')),
            ],
            options={
                'verbose_name': 'Zamowienie',
                'verbose_name_plural': 'Zamowienia',
            },
        ),
    ]