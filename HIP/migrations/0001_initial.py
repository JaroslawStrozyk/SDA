# Generated by Django 2.2.3 on 2019-07-06 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(blank=True, max_length=250, verbose_name='Nazwa')),
                ('uwagi', models.TextField(blank=True, verbose_name='Uwagi')),
            ],
            options={
                'verbose_name': 'Dział',
                'verbose_name_plural': 'Działy',
            },
        ),
        migrations.CreateModel(
            name='Sprzet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa_siec', models.CharField(max_length=50, verbose_name='Nazwa sieciowa')),
                ('kik', models.CharField(blank=True, max_length=50, verbose_name='Oznaczenie')),
                ('usr', models.CharField(blank=True, max_length=100, verbose_name='Użytkownik')),
                ('host', models.CharField(choices=[('Komputer', 'Komputer'), ('Drukarka', 'Drukarka'), ('Serwer', 'Serwer'), ('Access Point', 'Access Point'), ('Router', 'Router'), ('Switch', 'Switch'), ('Domena', 'Domena'), ('Tablet', 'Tablet'), ('Inne', 'Inne')], default='Komputer', max_length=100, verbose_name='Host')),
                ('typ', models.CharField(blank=True, max_length=100, verbose_name='Typ')),
                ('adres_ip', models.CharField(blank=True, max_length=200, verbose_name='Adres IP')),
                ('domena', models.CharField(blank=True, max_length=50, verbose_name='Domena')),
                ('sw_gn', models.CharField(blank=True, max_length=50, verbose_name='SW gniazdo')),
                ('typm', models.CharField(blank=True, max_length=200, verbose_name='Typ monitora')),
                ('snk', models.CharField(blank=True, max_length=200, verbose_name='Nr seryjny Komputera')),
                ('snm', models.CharField(blank=True, max_length=200, verbose_name='Nr seryjny Monitora')),
                ('uwagi', models.TextField(blank=True, verbose_name='Uwagi')),
                ('zdj', models.FileField(blank=True, upload_to='images', verbose_name='Zdjęcie')),
                ('system', models.ForeignKey(max_length=400, on_delete=django.db.models.deletion.CASCADE, to='HIP.System', verbose_name='System')),
            ],
            options={
                'verbose_name': 'Komputer',
                'verbose_name_plural': 'Komputery',
            },
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rodzaj_konta', models.CharField(max_length=200, verbose_name='Rodzaj/program')),
                ('kod', models.CharField(blank=True, max_length=200, verbose_name='Kod')),
                ('konto', models.CharField(max_length=100, verbose_name='Nazwa konta')),
                ('haslo', models.CharField(blank=True, max_length=100, verbose_name='Hasło konta')),
                ('adres', models.CharField(blank=True, max_length=100, verbose_name='Adres IP')),
                ('uwagi', models.TextField(blank=True, verbose_name='Uwagi')),
                ('sprzet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIP.Sprzet', verbose_name='Sprzęt')),
            ],
            options={
                'verbose_name': 'Profil',
                'verbose_name_plural': 'Profile',
            },
        ),
    ]