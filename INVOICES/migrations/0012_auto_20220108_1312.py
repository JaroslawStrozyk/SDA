# Generated by Django 3.1.3 on 2022-01-08 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INVOICES', '0011_auto_20220107_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faktura',
            name='confirm',
            field=models.CharField(choices=[('SKYPE', 'SKYPE'), ('E-MAIL', 'E-MAIL'), ('BEZ POTWIERDZENIA', 'BEZ POTWIERDZENIA')], default='SKYPE', max_length=50, verbose_name='Potwierdzenie (smartinfo@smartdesign-expo.com)'),
        ),
    ]
