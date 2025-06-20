# Generated by Django 5.0 on 2024-09-30 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COMP_REPO', '0047_auto_20240929_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sklad',
            name='dok_pdf2',
        ),
        migrations.RemoveField(
            model_name='sklad',
            name='dok_pdf3',
        ),
        migrations.RemoveField(
            model_name='sklad',
            name='dok_pdf4',
        ),
        migrations.AlterField(
            model_name='firma',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='dok_pdf1',
            field=models.FileField(blank=True, upload_to='magazyn', verbose_name='Lista do przechowywania'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='uwagi',
            field=models.TextField(blank=True, verbose_name='Adnotacje'),
        ),
    ]
