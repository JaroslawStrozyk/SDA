# Generated by Django 3.1.3 on 2022-08-07 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CARS', '0012_auto_deleg_auto'),
        ('DELEGATIONS', '0043_auto_20220805_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='delegacja',
            name='dane_auta',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CARS.auto', verbose_name='Dane auta'),
        ),
    ]
