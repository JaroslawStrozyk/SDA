# Generated by Django 3.1.3 on 2022-01-07 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORDERS', '0049_auto_20220102_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nrsde',
            name='pm',
            field=models.CharField(blank=True, choices=[('Agnieszka Skóra', 'Agnieszka Skóra'), ('Julia Królak', 'Julia Królak'), ('Piotr Junik', 'Piotr Junik'), ('Laura Bartkowiak', 'Laura Bartkowiak'), ('Dariusz Kaczmarek', 'Dariusz Kaczmarek'), ('Łukasz Jerzmanowski', 'Łukasz Jerzmanowski'), ('Michał Ogrzewalski', 'Michał Ogrzewalski'), ('Marzena Michalska', 'Marzena Michalska'), ('Łukasz Zaremba', 'Łukasz Zaremba'), ('Joanna Dittmar', 'Joanna Dittmar'), ('Adam Beim', 'Adam Beim'), ('Eryk Przybyłowicz', 'Eryk Przybyłowicz'), ('Małgosia Świadek', 'Małgosia Świadek')], default='', max_length=500, verbose_name='Project Manager'),
        ),
    ]
