# Generated by Django 3.1.3 on 2023-09-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0070_flagaszukania_uwagi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nip', models.CharField(max_length=100, verbose_name='NIP')),
                ('kontrahent', models.CharField(blank=True, max_length=300, verbose_name='Kontrahent')),
            ],
        ),
    ]
