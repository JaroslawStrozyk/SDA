# Generated by Django 2.2.3 on 2019-07-06 17:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rodzaj', models.CharField(choices=[('AUTO', 'Auto'), ('WUWI', 'Wózek widłowy')], default='AUTO', max_length=100, verbose_name='Rodzaj pojazdu')),
                ('typ', models.CharField(max_length=100, verbose_name='Typ')),
                ('rej', models.CharField(max_length=100, verbose_name='Nr rejestracyjny')),
                ('imie', models.CharField(max_length=100, verbose_name='Imię')),
                ('nazwisko', models.CharField(max_length=100, verbose_name='Nazwisko')),
                ('img1', models.FileField(blank=True, upload_to='dokuments', verbose_name='Zdjęcie')),
                ('img2', models.FileField(blank=True, upload_to='dokuments', verbose_name='Zdjęcie')),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data wprowadzenia')),
                ('us', models.DateField(default=django.utils.timezone.now, verbose_name='Data ubezpieczenia')),
                ('ps', models.DateField(default=django.utils.timezone.now, verbose_name='Data przeglądu')),
                ('uwagi', models.TextField(blank=True, verbose_name='Uwagi')),
            ],
            options={
                'verbose_name': 'Auto',
                'verbose_name_plural': 'Auta',
            },
        ),
    ]
