# Generated by Django 3.1.4 on 2020-12-28 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0015_auto_20201228_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zamowienie',
            name='data_dost',
            field=models.DateField(blank=True, default='', verbose_name='Data dostawy'),
        ),
        migrations.AlterField(
            model_name='zamowienie',
            name='data_fv',
            field=models.DateField(blank=True, default='', verbose_name='Data faktury'),
        ),
    ]
