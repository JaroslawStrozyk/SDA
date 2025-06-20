# Generated by Django 3.1.3 on 2023-05-04 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TIMBER_WH', '0031_auto_20230504_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='przychod',
            name='inwentura',
            field=models.BooleanField(default=False, verbose_name='Inwentura'),
        ),
        migrations.AddField(
            model_name='rozchod',
            name='inwentura',
            field=models.BooleanField(default=False, verbose_name='Inwentura'),
        ),
        migrations.CreateModel(
            name='StanObecny',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plyta', models.ForeignKey(max_length=400, on_delete=django.db.models.deletion.CASCADE, to='TIMBER_WH.plyta', verbose_name='Płyta')),
                ('przychod', models.ForeignKey(max_length=400, on_delete=django.db.models.deletion.CASCADE, to='TIMBER_WH.przychod', verbose_name='Przychód')),
                ('rozchod', models.ForeignKey(max_length=400, on_delete=django.db.models.deletion.CASCADE, to='TIMBER_WH.rozchod', verbose_name='Rozchód')),
            ],
            options={
                'verbose_name': 'Statystyka',
                'verbose_name_plural': 'Statystyki',
            },
        ),
    ]
