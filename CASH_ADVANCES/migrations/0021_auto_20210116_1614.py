# Generated by Django 3.1.5 on 2021-01-16 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CASH_ADVANCES', '0020_auto_20210115_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozycja',
            name='nr_roz',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CASH_ADVANCES.rozliczenie', verbose_name='Zaliczka'),
        ),
    ]