# Generated by Django 3.1.3 on 2023-04-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TIMBER_WH', '0025_auto_20230402_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plyta',
            name='magazyn',
            field=models.CharField(choices=[('MAGAZYN1', 'MAGAZYN Szparagowa'), ('MAGAZYN2', 'MAGAZYN Podolany'), ('MAGAZYN3', 'MAGAZYN Chemii')], default='MAGAZYN1', max_length=50, verbose_name='Magazyn'),
        ),
    ]
