# Generated by Django 5.0 on 2023-12-16 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INSURANCE', '0012_alter_ubezpieczenie_skladka_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termin',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ubezpieczenie',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
