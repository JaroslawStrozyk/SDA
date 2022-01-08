from djmoney.models.fields import MoneyField

from django.db import models
from django.utils import timezone



class Delegacja(models.Model):
    CHOISES_PM = (
        ('', ''),
        ('Agnieszka Skóra', 'Agnieszka Skóra'),
        ('Julia Królak', 'Julia Królak'),
        ('Piotr Junik', 'Piotr Junik'),
        ('Laura Bartkowiak', 'Laura Bartkowiak'),
        ('Dariusz Kaczmarek', 'Dariusz Kaczmarek'),
        ('Łukasz Jerzmanowski', 'Łukasz Jerzmanowski'),
        ('Michał Ogrzewalski', 'Michał Ogrzewalski'),
        ('Marzena Michalska', 'Marzena Michalska'),
        ('Łukasz Zaremba', 'Łukasz Zaremba'),
        ('Joanna Dittmar', 'Joanna Dittmar'),
        ('Bartosz Ługowski', 'Bartosz Ługowski'),
        ('Adam Beim', 'Adam Beim'),
        ('Eryk Przybyłowicz', 'Eryk Przybyłowicz'),
        ('Małgosia Świadek', 'Małgosia Świadek'),
        ('Olga Siukova', 'Olga Siukova'),
        ('Jarosław Stróżyk', 'Jarosław Stróżyk')
    )
    CHOISES_CON = (
        ('SKYPE', 'SKYPE'),
        ('E-MAIL', 'E-MAIL'),
        ('BEZ POTWIERDZENIA', 'BEZ POTWIERDZENIA')
    )

    imie       = models.CharField(max_length=100, verbose_name="Imię", blank=True, default='')
    nazwisko   = models.CharField(max_length=100, verbose_name="Nazwisko", blank=True, default='')
    naz_imie = models.CharField(max_length=300, verbose_name="Imię i Nazwisko", choices=CHOISES_PM, default='')
    targi      = models.CharField(max_length=200, verbose_name="Nazwa Targów")
    data_od    = models.DateField(default=timezone.now, verbose_name="Data od")
    data_do    = models.DateField(default=timezone.now, verbose_name="Data do")
    kasa_pln   = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ PLN ]")
    kasa_euro  = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ € ]")
    kasa_funt  = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ £ ] ")
    kasa_inna  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Gotówka [ Inna ]")
    kasa_karta = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Karta [ Kwota ]")
    zrobione = models.BooleanField(default=False, verbose_name="Wystawione")
    confirm = models.CharField(max_length=50, verbose_name="Potwierdzenie", choices=CHOISES_CON, default='SKYPE')

    def save(self, *args, **kwargs):
        super(Delegacja, self).save(*args, **kwargs)

    def __str__(self):
        return self.nazwisko

    class Meta:
        verbose_name = "Delegacja"
        verbose_name_plural = "Delegacje"