# Generated by Django 2.2.3 on 2020-08-25 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAPI', '0002_asp_waluta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asp',
            name='info',
            field=models.CharField(max_length=600, verbose_name='INFO'),
        ),
    ]