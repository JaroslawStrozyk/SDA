# Generated by Django 3.1.3 on 2022-08-04 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DELEGATIONS', '0036_auto_20220804_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delegacja',
            name='koszt_paliwo_kr',
        ),
        migrations.RemoveField(
            model_name='delegacja',
            name='koszt_paliwo_za',
        ),
    ]
