# Generated by Django 3.1.3 on 2025-01-06 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ID_CARDS', '0011_alter_dowod_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dowod',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
