# Generated by Django 3.1.3 on 2023-05-04 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TIMBER_WH', '0030_auto_20230503_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='przychod',
            name='inwentura',
        ),
        migrations.RemoveField(
            model_name='rozchod',
            name='inwentura',
        ),
    ]
