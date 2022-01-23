from django.db import models
from djmoney.models.fields import MoneyField
import datetime


class Pracownik(models.Model):
    CHOISES_GROUP = (
        ('BIURO', 'BIURO'),
        ('PRODUKCJA', 'PRODUKCJA')
    )
    CHOISES_SEC = (
        ('PROJEKTANT', 'PROJEKTANT'),
        ('MARKETING', 'MARKETING'),
        ('TM', 'TM'),
        ('STOLARZ', 'STOLARZ'),
        ('MONTAZYSTA', 'MONTAZYSTA'),
        ('MAGAZYN', 'MAGAZYN'),
        ('ZAOPATRZENIE', 'ZAOPATRZENIE'),
        ('ADMINISTRACJA', 'ADMINISTRACJA'),
        ('ZARZĄD', 'ZARZĄD')
    )
    CHOISES_EMPLOY = (
        ('UMOWA', 'UMOWA'),
        ('DZIAŁALNOŚĆ', 'DZIAŁALNOŚĆ')
    )
    imie           = models.CharField(max_length=100, verbose_name="Imię", blank=True, default='')
    nazwisko       = models.CharField(max_length=100, verbose_name="Nazwisko", blank=True, default='')
    grupa          = models.CharField(max_length=300, blank=True, verbose_name="Grupa", choices=CHOISES_GROUP, default='')
    dzial          = models.CharField(max_length=300, blank=True, verbose_name="Dział", choices=CHOISES_SEC, default='')
    zatrudnienie   = models.CharField(max_length=300, blank=True, verbose_name="Zatrudnienie", choices=CHOISES_EMPLOY, default='UMOWA')
    wymiar         = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Wymiar zatrudnienia")
    data_zat       = models.DateField(null=True, blank=True, verbose_name="Data zatrudnienia")
    staz           = models.IntegerField(default=0, verbose_name="Staż pracy")
    pensja_ust     = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Ustalona pensja")
    stawka_nadgodz = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nadgodziny stawka")
    stawka_wyj     = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wyjazd stawka")
    uwagi          = models.TextField(blank=True, verbose_name="Uwagi")

    def __str__(self):
        return self.imie+" "+self.nazwisko

    class Meta:
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"


class Pensja(models.Model):
    rok = models.IntegerField(default=datetime.datetime.now().year, verbose_name="Rok")
    miesiac = models.IntegerField(default=datetime.datetime.now().month, verbose_name="Miesiąc")
    pracownik = models.ForeignKey('Pracownik', verbose_name="Pracownik", max_length=100,  on_delete=models.SET_NULL, null=True, blank=True)
    wynagrodzenie = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wynagrodzenie")
    ppk = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="PPK")
    przelew = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Przelew")
    gotowka = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Gotówka")
    dodatek = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Niestandardowy dodatek")
    obciazenie = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Niestandardowe obciążenie")
    nadgodz_ilosc = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Ilość nadgodzin")
    nadgodz =  MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nadgodziny")

    def __str__(self):
        return self.wynagrodzenie

    class Meta:
        verbose_name = "Pensja"
        verbose_name_plural = "Pensje"