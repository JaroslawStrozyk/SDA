# Generated by Django 5.0 on 2024-04-21 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HIP', '0038_auto_20240101_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='serwis',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sprzet',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='system',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
