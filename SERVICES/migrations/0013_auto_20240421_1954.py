# Generated by Django 3.1.3 on 2024-04-21 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SERVICES', '0012_alter_profil_id_alter_usluga_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usluga',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
