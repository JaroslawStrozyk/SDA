# Generated by Django 3.1.3 on 2020-11-30 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAPI', '0005_auto_20200825_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlagaZmiany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zamowienie', models.BooleanField(default=False, verbose_name='Zamówienie zmiana')),
            ],
            options={
                'verbose_name': 'flaga',
                'verbose_name_plural': 'Flagi',
            },
        ),
    ]