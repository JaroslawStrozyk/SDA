# Generated by Django 3.1.3 on 2022-11-03 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DELEGATIONS', '0064_delegacja_targi2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delegacja',
            name='kod_sde_targi1',
        ),
        migrations.RemoveField(
            model_name='delegacja',
            name='kod_sde_targi2',
        ),
        migrations.RemoveField(
            model_name='delegacja',
            name='targi1',
        ),
        migrations.RemoveField(
            model_name='delegacja',
            name='targi2',
        ),
    ]
