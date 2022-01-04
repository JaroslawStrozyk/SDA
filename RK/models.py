from django.db import models
from djmoney.models.fields import MoneyField
from django.utils import timezone

class Waluta(models.Model):
    tab     = models.CharField(max_length=2, verbose_name="Typ tablicy", blank=True)
    kod     = models.CharField(max_length=5, verbose_name="Kod waluty", blank=True)
    poz     = models.CharField(max_length=50, verbose_name="Identyfikator tablicy", blank=True)
    data    = models.CharField(max_length=50, verbose_name="Data", blank=True)
    kurs    = models.FloatField(verbose_name="Kurs", blank=True)
    opis    = models.CharField(max_length=50, verbose_name="Opis", blank=True)

    def __str__(self):
        return self.kod+', '+self.poz

    class Meta:
        verbose_name = "Waluta"
        verbose_name_plural = "Waluty"



class FirmaKasa(models.Model):
    CHOISES_WHAT = (
        ('KO', 'Kasa ogólna'),
        ('KZ', 'Kasa zastrzeżona'),
    )
    rodzaj  = models.CharField(max_length=100, verbose_name="Rodzaj kasy", choices=CHOISES_WHAT, default='KO')
    nazwa   = models.CharField(max_length=200, verbose_name="Nazwa firmy", blank=True)
    adres   = models.CharField(max_length=200, verbose_name="Ulica, numer", blank=True)
    miasto  = models.CharField(max_length=200, verbose_name="Kod pocztowy, Miasto", blank=True)
    nip     = models.CharField(max_length=200, verbose_name="NIP", blank=True)
    kasa    = models.CharField(max_length=200, verbose_name="Nazwa kasy", blank=True)
    konto   = models.CharField(max_length=200, verbose_name="Nr konta kasy", blank=True)
    bo      = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Bilans otwarcia")
    stan    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Stan")
    data_bo = models.DateField(default=timezone.now, verbose_name="Data bilansu")
    uwagi   = models.TextField(blank=True, verbose_name="Uwagi")

    def __str__(self):
        return self.nazwa+', '+self.kasa

    class Meta:
        verbose_name = "FirmaKasa"
        verbose_name_plural = "FirmyKasy"


class RaportKasowy(models.Model):
    kasa           = models.ForeignKey('FirmaKasa', verbose_name="Firma&Kasa", max_length=400, on_delete=models.CASCADE, default=1)
    data           = models.DateField(default=timezone.now, verbose_name="Data")
    sum_przychod   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Sum przychód") #models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    sum_rozchod    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Sum rozchód")
    stan_poprzedni = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Sum poprzedni")
    stan_obecny    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Sum obecny")
    kw             = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name="KW")
    kp             = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name="KP")
    mkw            = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name="KW w m-c")
    mkp            = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name="KP w m-c")


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "RaportKasowy"
        verbose_name_plural = "RaportyKasowe"


class KwKp(models.Model):
    CHOISES_WHO = (
        ('KW', 'KW'),
        ('KP', 'KP'),
    )

    kasa      = models.ForeignKey('FirmaKasa', verbose_name="Kasa", max_length=400, on_delete=models.CASCADE)
    rodzaj    = models.CharField(max_length=100, verbose_name="Rodzaj", choices=CHOISES_WHO, default='KW')
    numer     = models.DecimalField(max_digits=11, decimal_places=0, default=0,  verbose_name="Numer dokumentu")
    nazwa     = models.CharField(max_length=200, verbose_name="Nazwa/Nazwisko i Imię", blank=True)
    adres     = models.CharField(max_length=200, verbose_name="Adres", blank=True)
    miasto    = models.CharField(max_length=200, verbose_name="Miasto i kod", blank=True)
    przychod  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Przychód")
    rozchod   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Rozchód")
    data      = models.DateField(default=timezone.now, verbose_name="Data")
    opis      = models.CharField(max_length=200, verbose_name="Opis", blank=True)
    uwagi     = models.TextField(blank=True, verbose_name="Uwagi")
    switch    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wartość")

    def __str__(self):
        return self.rodzaj+' '+self.opis

    class Meta:
        verbose_name = "KwKp"
        verbose_name_plural = "KwKpy"