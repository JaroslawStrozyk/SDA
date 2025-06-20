# Generated by Django 3.1.3 on 2023-01-14 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COMP_REPO', '0011_auto_20230114_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sklad',
            name='czas_do',
            field=models.DateField(blank=True, null=True, verbose_name='Do daty'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='czas_od',
            field=models.DateField(blank=True, null=True, verbose_name='Od daty'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='przech_gl',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=11, verbose_name='Głebokość [m]'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='przech_pow',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=11, verbose_name='Powierzchnia przechowywania [m²]'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='przech_sze',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=11, verbose_name='Szerokość [m]'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='przech_wys',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=11, verbose_name='Wysokość [m]'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='wydano_ilosc',
            field=models.IntegerField(default=0, verbose_name='Ile wydano'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='zwroco_ilosc',
            field=models.IntegerField(default=0, verbose_name='Ile zwrócono'),
        ),
    ]
