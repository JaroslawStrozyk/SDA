# Generated by Django 3.1.5 on 2021-01-15 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0028_auto_20210115_2331'),
        ('CASH_ADVANCES', '0019_auto_20210102_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozycja',
            name='nr_mpk',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ORDERS.nrmpk', verbose_name='Nr MPK'),
        ),
        migrations.AlterField(
            model_name='pozycja',
            name='nr_sde',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ORDERS.nrsde', verbose_name='Nr SDE'),
        ),
        migrations.DeleteModel(
            name='NrMPK',
        ),
        migrations.DeleteModel(
            name='NrSDE',
        ),
    ]
