from django.db import models
from djmoney.models.fields import MoneyField
from django.utils import timezone


class Faktura(models.Model):
    CHOISES_WHAT = (
        ('PROFORMA', 'PROFORMA'),
        ('ZALICZKOWA', 'ZALICZKOWA'),
        ('ROZLICZAJACA', 'ROZLICZAJĄCA'),
        ('KOREKTA', 'KOREKTA'),
        ('INNE', 'INNE'),
    )
    CHOISES_FORWHAT = (
        ('STOISKO', 'STOISKO'),
        ('PROJEKT', 'PROJEKT STOISKA'),
        ('MAGAZYNOWANIE', 'MAGAZYNOWANIE'),
        ('TRANSPORT','TRANSPORT'),
    )
    CHOISES_SPEC = (
        ('NIE', 'NIE MA'),
        ('TAK', 'JEST'),
    )
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

    data       = models.DateTimeField(default=timezone.now, verbose_name="Data zgłoszenia")
    imie       = models.CharField(max_length=100, verbose_name="Imię", blank=True, default='')
    nazwisko   = models.CharField(max_length=100, verbose_name="Nazwisko", blank=True, default='')
    naz_imie   = models.CharField(max_length=300, verbose_name="Imię i Nazwisko", choices=CHOISES_PM, default='')
    rfaktura   = models.CharField(max_length=100, verbose_name="Rodzaj faktury", choices=CHOISES_WHAT, default='PROFORMA')
    termin     = models.DateField(default=timezone.now, verbose_name="Termin płatności")
    targi      = models.CharField(max_length=200, verbose_name="Nazwa Targów")
    stoisko    = models.CharField(max_length=200, verbose_name="Nazwa Stoiska")
    kwota      = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota [ netto ]")
    zaco       = models.CharField(max_length=100, verbose_name="Za co", choices=CHOISES_FORWHAT, default='STOISKO')
    spec       = models.CharField(max_length=20,  verbose_name="Specyfikacja", choices=CHOISES_SPEC, default='NIE')
    uwagi      = models.TextField(blank=True, verbose_name="Uwagi")
    zrobione   = models.BooleanField(default=False,  verbose_name="Wystawione")
    sig_source = models.BooleanField(default=False)
    confirm    = models.CharField(max_length=50,  verbose_name="Potwierdzenie (smartinfo@smartdesign-expo.com)", choices=CHOISES_CON, default='SKYPE')

    def __str__(self):
        return self.nazwisko

    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "Faktury"


class Osoba(models.Model):
    naz_imie = models.CharField(max_length=300, verbose_name="Imię i Nazwisko")
    skype    = models.CharField(max_length=200, verbose_name="Adres Skype",blank=True)
    email    = models.CharField(max_length=200, verbose_name="Adres e-mail",blank=True)

    def __str__(self):
        return self.naz_imie

    class Meta:
        verbose_name = "Osoba"
        verbose_name_plural = "Osoby"