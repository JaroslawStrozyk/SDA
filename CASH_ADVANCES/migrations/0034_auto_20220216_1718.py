# Generated by Django 3.1.3 on 2022-02-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CASH_ADVANCES', '0033_auto_20211204_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozycja',
            name='data_zam',
            field=models.DateField(blank=True, null=True, verbose_name='Data zamówienia'),
        ),
    ]
