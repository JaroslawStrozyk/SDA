# Generated by Django 3.1.3 on 2021-08-08 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0040_auto_20210710_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zamowienie',
            name='data_zam',
            field=models.DateField(blank=True, null=True, verbose_name='Data zamówienia'),
        ),
        migrations.AlterField(
            model_name='zamowienie',
            name='roz',
            field=models.BooleanField(default=False, verbose_name='Akceptacja'),
        ),
    ]