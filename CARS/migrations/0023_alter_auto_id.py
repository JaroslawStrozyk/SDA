# Generated by Django 5.0 on 2025-01-03 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CARS', '0022_auto_20240421_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
