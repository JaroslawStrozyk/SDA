# Generated by Django 3.1.3 on 2025-04-01 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('COMP_REPO_NEW', '0013_elementkatalogowy_wysokosc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historiapalety',
            name='sklad',
        ),
        migrations.RemoveField(
            model_name='okresprzechowywania',
            name='firma',
        ),
        migrations.RemoveField(
            model_name='sklad',
            name='element_katalogowy',
        ),
        migrations.RemoveField(
            model_name='sklad',
            name='firma',
        ),
        migrations.RemoveField(
            model_name='sklad',
            name='nr_sde',
        ),
        migrations.RemoveField(
            model_name='sklad',
            name='okres',
        ),
        migrations.DeleteModel(
            name='ElementKatalogowy',
        ),
        migrations.DeleteModel(
            name='Firma',
        ),
        migrations.DeleteModel(
            name='HistoriaPalety',
        ),
        migrations.DeleteModel(
            name='OkresPrzechowywania',
        ),
        migrations.DeleteModel(
            name='Sklad',
        ),
    ]
