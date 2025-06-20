# Generated by Django 3.1.3 on 2022-12-15 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INVOICES', '0018_auto_20221116_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faktura',
            name='naz_imie',
            field=models.CharField(choices=[('', ''), ('Agnieszka Skóra', 'Agnieszka Skóra'), ('Julia Królak', 'Julia Królak'), ('Piotr Junik', 'Piotr Junik'), ('Agnieszka Kaźmierska', 'Agnieszka Kaźmierska'), ('Patryk Chodecki', 'Patryk Chodecki'), ('Dariusz Kaczmarek', 'Dariusz Kaczmarek'), ('Łukasz Jerzmanowski', 'Łukasz Jerzmanowski'), ('Michał Ogrzewalski', 'Michał Ogrzewalski'), ('Marzena Michalska', 'Marzena Michalska'), ('Łukasz Zaremba', 'Łukasz Zaremba'), ('Joanna Dittmar', 'Joanna Dittmar'), ('Bartosz Ługowski', 'Bartosz Ługowski'), ('Adam Beim', 'Adam Beim'), ('Eryk Przybyłowicz', 'Eryk Przybyłowicz'), ('Małgorzata Świadek', 'Małgorzata Świadek'), ('Monika Stefańska', 'Monika Stefańska'), ('Katarzyna Rybak', 'Katarzyna Rybak'), ('Dariusz Grabowski', 'Dariusz Grabowski'), ('Jarosław Stróżyk', 'Jarosław Stróżyk')], default='', max_length=300, verbose_name='Imię i Nazwisko'),
        ),
    ]
