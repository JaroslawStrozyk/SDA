# Generated by Django 5.0 on 2023-12-16 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PHONES', '0007_alter_telefon_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telefon',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
