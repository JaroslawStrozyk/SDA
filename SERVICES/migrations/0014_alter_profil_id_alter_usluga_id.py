# Generated by Django 5.0 on 2025-01-03 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SERVICES', '0013_auto_20240421_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usluga',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
