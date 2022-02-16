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
        ('GRAFIK', 'GRAFIK'),
        ('MARKETING', 'MARKETING'),
        ('TM', 'TM'),
        ('PM', 'PM'),
        ('LOGISTYKA', 'LOGISTYKA'),
        ('KIEROWCA', 'KIEROWCA'),
        ('CNC', 'CNC'),
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
    ppk            = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="PPK")
    dystans        = models.IntegerField(default=0, verbose_name="Dystans [km]")
    uwagi          = models.TextField(blank=True, verbose_name="Uwagi")
    pracuje        = models.BooleanField(default=True, verbose_name="Pracuje")

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
    dodatek = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Extra dodatek")
    dodatek_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Opis extra dodatek")
    obciazenie = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Extra obciążenie")
    obciazenie_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Opis extra obciążenie")
    km_stawka  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kilome. stawka")
    km_dystans = models.IntegerField(default=0, verbose_name="Dystans [km]")
    km_ilosc = models.IntegerField(default=0, verbose_name="Kilometrówka ilość dni")
    km_wartosc = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kilome. wartość")
    stawka_nadgodz = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nadgodziny stawka")
    nadgodz_ilosc = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Ilość nadgodzin")
    nadgodz =  MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nadgodziny")
    nadgodz_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Opis nadgodziny")
    stawka_wyj = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wyjazd stawka")
    del_ilosc_100 = models.IntegerField(default=0, verbose_name="Delega. ilość 100%")
    del_ilosc_50 = models.IntegerField(default=0, verbose_name="Delega. ilość 50%")
    del_ilosc_razem = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Delegacja razem")
    del_ilosc_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Opis delegacji")
    premia = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Premia")
    razem  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Razem")
    zaliczka = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Zaliczka")
    komornik = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Komornik")
    brutto_brutto = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Brutto brutto")
    wyplata = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wypłata")
    sum_kosztow = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma kosztów")
    rozliczono = models.BooleanField(default=False, verbose_name="Rozliczono")
    l4 =  models.BooleanField(default=False, verbose_name="L4")
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Pensja"
        verbose_name_plural = "Pensje"


class Import(models.Model):
    up_load = models.FileField(upload_to='import', verbose_name="Pliki PDF", blank=True)

    def __str__(self):
        return str(self.up_load)

    class Meta:
        verbose_name = "Import"
        verbose_name_plural = "Importy"

