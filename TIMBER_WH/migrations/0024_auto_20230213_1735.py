# Generated by Django 3.1.3 on 2023-02-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TIMBER_WH', '0023_plyta_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plyta',
            name='limit',
            field=models.DecimalField(decimal_places=1, default=10.0, max_digits=11, verbose_name='Poziom limitu towaru'),
        ),
    ]
