from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField



class Katalog(models.Model):
    nazwa = models.CharField(max_length=200, verbose_name="Nazwa")
    opis  = models.CharField(max_length=200, verbose_name="Opis", blank=True)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Katalog"
        verbose_name_plural = "Katalogi"


class Plik(models.Model):
    nazwa = models.CharField(max_length=200, verbose_name="Nazwa")
    katalog = models.ForeignKey(Katalog, verbose_name="Katalog", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    dokument = models.FileField(upload_to='wdokumenty', verbose_name="Dokument", blank=True)
    form = models.BooleanField(default=False, verbose_name="Formularz")

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Plik"
        verbose_name_plural = "Pliki"



class Asp(models.Model):
    cel    = models.IntegerField(default=0, verbose_name="CEL")
    adres  = models.CharField(max_length=200, verbose_name="ADRES")
    tytul  = models.CharField(max_length=200, verbose_name="TYTUŁ", blank=True)
    info   = models.CharField(max_length=12000, verbose_name="INFO")
    data   = models.DateTimeField(default=timezone.now, verbose_name="DATA WPROWADZENIA")

    def __str__(self):
        return self.adres

    class Meta:
        verbose_name = "Asp"
        verbose_name_plural = "Asp"


class Waluta(models.Model):
    tab  = models.CharField(max_length=50, verbose_name="TABELA")
    kod  = models.CharField(max_length=10, verbose_name="KOD")
    poz  = models.CharField(max_length=10, verbose_name="POZYCJA", default="")
    data = models.CharField(max_length=50, verbose_name="DATA")
    opis = models.CharField(max_length=50, verbose_name="OPIS", default="")
    kurs = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="KURS")


    def __str__(self):
        return str(self.data)# +' '+str(self.kod)+' '+str(self.kurs)

    class Meta:
        verbose_name = "Waluta"
        verbose_name_plural = "Waluty"


class Log(models.Model):
    data = models.CharField(max_length=200, verbose_name="Data i Czas")
    modul = models.CharField(max_length=200, verbose_name="Moduł")
    uwagi = models.CharField(max_length=200, verbose_name="Uwagi")


    def __str__(self):
        return self.data

    class Meta:
        verbose_name = "System - Log"
        verbose_name_plural = "System - Logi"


class FlagaZmiany(models.Model):
    zamowienie  = models.IntegerField(default=0, verbose_name="Zmiana Zamówienie")
    pozycja     = models.IntegerField(default=0, verbose_name="Zmiana Pozycja")
    rozliczenie = models.IntegerField(default=0, verbose_name="Zmiana Rozliczenia")
    licznik     = models.IntegerField(default=0, verbose_name="Licznik")
    do_google   = models.IntegerField(default=0, verbose_name="Wyjście do Google")
    loop_count  = models.IntegerField(default=0, verbose_name="Licznik loop")


    def __str__(self):
        return self.adres

    class Meta:
        verbose_name = "Flaga"
        verbose_name_plural = "Flagi"



class Rok(models.Model):
    rok = models.IntegerField(default=0, verbose_name="Rok")
    flg = models.IntegerField(default=0, verbose_name="Flaga")

    def __str__(self):
        return str(self.rok)

    class Meta:
        verbose_name = "Rok"
        verbose_name_plural = "Lata"


class URok(models.Model):
    nazwa = models.CharField(max_length=200, verbose_name="Nazwa")
    rok   = models.IntegerField(default=0, verbose_name="Rok")

    def __str__(self):
        return self.nazwa + " " + str(self.rok)

    class Meta:
        verbose_name = "URok"
        verbose_name_plural = "ULata"

class Ustawienia(models.Model):
    CHOISES_WHAT = (
        ('Delegacja', 'Delegacja'),
        ('Faktury', 'Faktury'),
        ('Samochody', 'Samochody'),
        ('Ubezpieczenia', 'Ubezpieczenia'),
    )
    CHOISES_MED = (
        ('EMAIL', 'EMAIL'),
        ('SKYPE', 'SKYPE'),
    )
    co = models.CharField(max_length=100, verbose_name="Co", choices=CHOISES_WHAT, default='Delegacja')
    medium = models.CharField(max_length=100, verbose_name="Medium", choices=CHOISES_MED, default='EMAIL')
    email  = models.CharField(max_length=200, verbose_name="Email")
    skype  = models.CharField(max_length=200, verbose_name="Skype")
    dshift = models.IntegerField(default=0, verbose_name="Częstotliwość")
    tshift = models.IntegerField(default=0, verbose_name="Uprzedzenie")

    def __str__(self):
        return self.co + " " + self.medium

    class Meta:
        verbose_name = "Ustawienie"
        verbose_name_plural = "Ustawienia"