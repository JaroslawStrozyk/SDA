# Generated by Django 3.1.3 on 2024-01-01 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PHONES', '0011_alter_telefon_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telefon',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
