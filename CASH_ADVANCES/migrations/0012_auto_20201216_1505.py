# Generated by Django 3.1.4 on 2020-12-16 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CASH_ADVANCES', '0011_auto_20201203_2037'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nrmpk',
            options={'ordering': ['nazwa'], 'verbose_name': 'Numer MPK', 'verbose_name_plural': 'Numery MPK'},
        ),
        migrations.AlterModelOptions(
            name='nrsde',
            options={'ordering': ['nazwa'], 'verbose_name': 'Numer SDE', 'verbose_name_plural': 'Numery SDE'},
        ),
    ]
