# Generated by Django 3.1.3 on 2022-01-12 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WORKER', '0003_auto_20220112_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pracownik',
            name='dzial',
            field=models.CharField(blank=True, choices=[('PROJEKTANT', 'PROJEKTANT'), ('MARKETING', 'MARKETING'), ('TM', 'TM'), ('STOLARZ', 'STOLARZ'), ('MONTAZYSTA', 'MONTAZYSTA'), ('MAGAZYN', 'MAGAZYN'), ('ZAOPATRZENIE', 'ZAOPATRZENIE'), ('ADMINISTRACJA', 'ADMINISTRACJA'), ('ZARZĄD', 'ZARZĄD')], default='', max_length=300, verbose_name='Dział'),
        ),
    ]