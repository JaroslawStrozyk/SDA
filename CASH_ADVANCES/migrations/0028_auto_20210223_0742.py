# Generated by Django 3.1.3 on 2021-02-23 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CASH_ADVANCES', '0027_auto_20210223_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozycja',
            name='data_zam',
            field=models.DateField(blank=True, null=True, verbose_name='Data zamówienia'),
        ),
    ]
