# Generated by Django 2.2.3 on 2020-02-03 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HIP', '0004_auto_20200202_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprzet',
            name='pesel',
            field=models.CharField(blank=True, max_length=100, verbose_name='PESEL'),
        ),
        migrations.AddField(
            model_name='sprzet',
            name='zam',
            field=models.CharField(blank=True, max_length=300, verbose_name='Zamieszkały'),
        ),
    ]