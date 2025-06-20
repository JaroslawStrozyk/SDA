# Generated by Django 3.1.3 on 2023-04-02 20:18

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAPI', '0021_flagazmiany_loop_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waluta',
            name='kurs_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CHF', 'CHF'), ('DKK', 'DKK'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('PLN', 'PLN'), ('USD', 'USD')], default='PLN', editable=False, max_length=3),
        ),
    ]
