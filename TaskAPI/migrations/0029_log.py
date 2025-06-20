# Generated by Django 5.0 on 2023-12-16 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAPI', '0028_delete_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=200, verbose_name='Data i Czas')),
                ('modul', models.CharField(max_length=200, verbose_name='Moduł')),
                ('uwagi', models.CharField(max_length=200, verbose_name='Uwagi')),
            ],
            options={
                'verbose_name': 'System - Log',
                'verbose_name_plural': 'System - Logi',
            },
        ),
    ]
