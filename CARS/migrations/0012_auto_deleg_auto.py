# Generated by Django 3.1.3 on 2022-08-07 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CARS', '0011_auto_20220104_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='deleg_auto',
            field=models.BooleanField(default=False, verbose_name='Widok auta w delegacji'),
        ),
    ]
