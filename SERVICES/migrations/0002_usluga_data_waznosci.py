# Generated by Django 3.1.3 on 2021-12-29 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SERVICES', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usluga',
            name='data_waznosci',
            field=models.DateField(blank=True, null=True, verbose_name='Data ważności'),
        ),
    ]
