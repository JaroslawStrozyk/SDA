# Generated by Django 3.1.3 on 2025-04-17 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COMP_REPO_NEW', '0020_auto_20250417_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementkatalogowy',
            name='zwolnione',
            field=models.BooleanField(default=False, verbose_name='Nie licz'),
        ),
    ]
