# Generated by Django 2.2.3 on 2020-08-16 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usluga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa_siec', models.CharField(max_length=150, verbose_name='Nazwa sieciowa')),
                ('usr', models.CharField(blank=True, max_length=100, verbose_name='Użytkownik')),
                ('dostawca', models.CharField(blank=True, max_length=150, verbose_name='Dostawca')),
                ('hosting', models.CharField(blank=True, max_length=100, verbose_name='Hosting')),
                ('uwagi', models.TextField(blank=True, verbose_name='Uwagi')),
                ('zdj', models.FileField(blank=True, upload_to='images', verbose_name='Zdjęcie')),
            ],
            options={
                'verbose_name': 'Usługa',
                'verbose_name_plural': 'Usługi',
            },
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rodzaj_konta', models.CharField(max_length=200, verbose_name='Rodzaj/program')),
                ('konto', models.CharField(max_length=100, verbose_name='Nazwa konta')),
                ('haslo', models.CharField(blank=True, max_length=100, verbose_name='Hasło konta')),
                ('adres', models.CharField(blank=True, max_length=100, verbose_name='Adres IP')),
                ('uwagi', models.TextField(blank=True, verbose_name='Uwagi')),
                ('usluga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SERVICES.Usluga', verbose_name='Usługa')),
            ],
            options={
                'verbose_name': 'Profil',
                'verbose_name_plural': 'Profile',
            },
        ),
    ]
