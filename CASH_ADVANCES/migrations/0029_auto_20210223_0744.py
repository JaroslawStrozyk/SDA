# Generated by Django 3.1.3 on 2021-02-23 07:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('CASH_ADVANCES', '0028_auto_20210223_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozycja',
            name='data_zam',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Data zamówienia'),
        ),
    ]
