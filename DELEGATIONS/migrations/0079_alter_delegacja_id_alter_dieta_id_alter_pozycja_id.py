# Generated by Django 5.0 on 2023-12-16 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DELEGATIONS', '0078_alter_delegacja_czysta_dieta_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delegacja',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='dieta',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pozycja',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
