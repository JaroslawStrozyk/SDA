# Generated by Django 3.1.3 on 2022-01-05 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SERVICES', '0003_usluga_termin'),
    ]

    operations = [
        migrations.AddField(
            model_name='usluga',
            name='okres',
            field=models.CharField(choices=[('ROCZNY', 'ROCZNY'), ('MIESIĘCZNY', 'MIESIECZNY'), ('BEZPŁATNY', 'BEZPŁATNY')], default='ROCZNY', max_length=10, verbose_name='Okres rozliczeniowy'),
        ),
    ]