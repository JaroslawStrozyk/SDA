# Generated by Django 2.2.3 on 2020-08-30 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HIP', '0013_auto_20200830_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprzet',
            name='host',
            field=models.CharField(choices=[('Komputer', 'Komputer'), ('Monitor', 'Monitor'), ('Drukarka', 'Drukarka'), ('Serwer', 'Serwer'), ('Access Point', 'Access Point'), ('Router', 'Router'), ('Switch', 'Switch'), ('Domena', 'Domena'), ('Tablet', 'Tablet'), ('Inne', 'Inne')], default='Komputer', max_length=100, verbose_name='Host'),
        ),
    ]
