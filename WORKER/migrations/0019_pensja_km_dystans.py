# Generated by Django 3.1.3 on 2022-02-06 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0018_auto_20220206_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='pensja',
            name='km_dystans',
            field=models.IntegerField(default=0, verbose_name='Dystans [km]'),
        ),
    ]