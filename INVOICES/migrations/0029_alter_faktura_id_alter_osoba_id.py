# Generated by Django 5.0 on 2023-12-16 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INVOICES', '0028_auto_20231210_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faktura',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='osoba',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
