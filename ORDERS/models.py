from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from SDA.settings import ORD_PM
from TaskAPI.models import FlagaZmiany
import datetime


class NrSDE(models.Model):
    CHOISES_PM = ORD_PM

    CHOISES_MC = (
        ('styczeń', 'styczeń'),
        ('luty', 'luty'),
        ('marzec', 'marzec'),
        ('kwiecień', 'kwiecień'),
        ('maj', 'maj'),
        ('czerwiec', 'czerwiec'),
        ('lipiec', 'lipiec'),
        ('sierpień', 'sierpień'),
        ('wrzesień', 'wrzesień'),
        ('październik', 'październik'),
        ('listopad', 'listopad'),
        ('grudzień', 'grudzień'),
    )
    rok  = models.IntegerField(default=datetime.datetime.now().year, verbose_name="Rok Nr SDE")
    rokk = models.IntegerField(default=datetime.datetime.now().year, verbose_name="Rok kal Nr SDE")
    d_miesiac = models.CharField(max_length=500, blank=True, verbose_name="Bezp. Miesiac")
    c_miesiac = models.CharField(max_length=500, blank=True, verbose_name="Got. Miesiac")
    nazwa    = models.CharField(max_length=250, blank=True, verbose_name="Nazwa")
    nazwa_id = models.CharField(max_length=250, blank=True, verbose_name="ID Nazwa", default="")
    klient = models.CharField(max_length=500, blank=True, verbose_name="Klient")
    targi  = models.CharField(max_length=500, blank=True, verbose_name="Targi")
    stoisko = models.CharField(max_length=500, blank=True, verbose_name="Stoisko")
    opis  = models.CharField(max_length=500, blank=True, verbose_name="Opis")
    fv    = models.CharField(max_length=500, blank=True, verbose_name="Faktura")
    rks   = models.CharField(max_length=50, blank=True, verbose_name="Rok sprzedaży (z FV)")
    mcs   = models.CharField(max_length=50, blank=True, verbose_name="Miesiąc sprzedaży (z FV)", choices=CHOISES_MC, default='')
    pm    = models.CharField(max_length=500, blank=True, verbose_name="Project Manager", choices=CHOISES_PM, default='')
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")
    sum_direct = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma koszty bezpośrednie")
    sum_cash   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma koszty gotówkowe")
    sum_premie = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma Premie")
    sum_deleg  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma Delegacje")
    sum_pre_del = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Premie i delegacje")
    pow_stoisko = models.IntegerField(default=0, verbose_name="Powierzchnia stoiska")
    pow_pietra  = models.IntegerField(default=0, verbose_name="Powierzchnia piętra")
    deleg_sum   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma delegacji")
    magazyn_dre = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Magazyny drewna")
    magazyn_wewn = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11,verbose_name="Magazyn wewnętrzny")
    mpk_402111 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11,verbose_name="402-11-1")
    mpk_402112 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="402-11-2")
    mpk_403161 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="403-16-1")
    mpk_403162 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="403-16-2")
    mpk_403163 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="403-16-3")
    mpk_403164 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="403-16-4")
    mpk_403165 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="403-16-5")
    mpk_403166 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="403-16-6")
    mpk_403167 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="403-16-7")
    del_roznica = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Delegacja różnica")
    del_wyjazd = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Delegacja wyjazd")

    def __str__(self):
        if self.stoisko != '':
            tekst = self.nazwa + "......" + self.targi + ' - ' + self.klient +' /' + self.stoisko + '/'
        else:
            tekst = self.nazwa + "......" + self.opis
        return tekst

    class Meta:
        ordering = ["nazwa"]
        verbose_name = "Numer SDE"
        verbose_name_plural = "Numery SDE"


class NrMPK(models.Model):
    rok      = models.IntegerField(default=datetime.datetime.now().year, verbose_name="Rok Nr MPK")
    nazwa    = models.CharField(max_length=50, blank=True, verbose_name="Nazwa")
    sum_zam  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma zamówień")
    sum_zal  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma zaliczek")
    opis     = models.CharField(max_length=500, blank=True, verbose_name="Opis")
    uwagi    = models.TextField(blank=True, verbose_name="Uwagi")
    st = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Styczeń")
    lu = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Luty")
    ma = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Marzec")
    kw = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwiecień")
    mj = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Maj")
    cz = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Czerwiec")
    lp = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Lipiec")
    si = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Sierpień")
    wr = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wrzesień")
    pa = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Październik")
    li = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Listopad")
    gr = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Grudzień")
    b_d = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Bez daty")
    suma = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma")
    lsde = models.BooleanField(default=False, verbose_name="Lista dla SDE")

    def __str__(self):
        return self.nazwa + "......" + self.opis

    class Meta:
        ordering = ["nazwa"]
        verbose_name = "Numer MPK"
        verbose_name_plural = "Numery MPK"


class FlagaSzukania(models.Model):
    nazwa = models.CharField(default='', max_length=100, verbose_name="Nazwa")
    uwagi = models.CharField(default='', max_length=200, verbose_name="Uwagi")

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Flaga szukania"
        verbose_name_plural = "Flagi szukania"


class Nip(models.Model):
    nip = models.CharField(max_length=100, verbose_name="NIP")
    kontrahent = models.CharField(max_length=300, verbose_name="Kontrahent", blank=True)

    def __str__(self):
        return self.nip + '..... [' + self.kontrahent + ']'
    class Meta:
        verbose_name = "NIP"
        verbose_name_plural = "NIP-y"


class Zamowienie(models.Model):
    CHOISES_SPOSOB = (
        ('Przelew', 'Przelew'),
        ('Karta', 'Karta'),
        ('Gotówka', 'Gotówka'),
    )

    CHOISES_RODZAJ = (
        ('Faktura', 'Faktura'),
        ('Proforma', 'Proforma'),
        ('Zamowienie', 'Zamówienie'),
        ('Zaliczka', 'Zaliczka'),
        ('Korekta','Korekta'),
        ('Nota','Nota'),
        ('Polisa', 'Polisa'),
        ('Duplikat', 'Duplikat'),
        ('Inny', 'Inny'),
    )

    rok          = models.IntegerField(default=0, verbose_name="Rok wg SDE")
    rokk         = models.IntegerField(default=0, verbose_name="Rok kalendarzowy")
    nip_ind      = models.ForeignKey('Nip', verbose_name="NIP", max_length=100,  on_delete=models.SET_NULL, null=True, blank=True)
    nip          = models.CharField(default='', max_length=100, verbose_name="NIP1", blank=True)
    opis         = models.CharField(max_length=300, verbose_name="Opis zamówienia")
    kontrahent   = models.CharField(max_length=300, verbose_name="Kontrahent")
    flaga_sz     = models.ForeignKey('FlagaSzukania', verbose_name="Flaga wyszukiwania", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    wartosc_zam  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wartość zamówienia")
    nr_zam       = models.CharField(max_length=300, verbose_name="Nr zamówienia", blank=True)
    sposob_plat  = models.CharField(max_length=100, verbose_name="Sposób płatności", choices=CHOISES_SPOSOB, default='', blank=True)
    rodzaj_plat  = models.CharField(max_length=100, verbose_name="Rodzaj dokumentu", choices=CHOISES_RODZAJ, default='', blank=True)
    nr_sde       = models.ForeignKey('NrSDE', verbose_name="Nr SDE", max_length=100,  on_delete=models.SET_NULL, null=True, blank=True)
    nr_mpk       = models.ForeignKey('NrMPK', verbose_name="Nr MPK", max_length=100,  on_delete=models.SET_NULL, null=True, blank=True)
    nr_dok1      = models.CharField(max_length=100, verbose_name="Nr proformy", blank=True)
    zal1         = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Proforma")
    zal1_bi      = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Brutto Inne")
    nr_dok2      = models.CharField(max_length=100, verbose_name="Nr zaliczki", blank=True)
    zal2         = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Zaliczka")
    zal2_bi      = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Brutto Inne")
    nr_dok3      = models.CharField(max_length=100, verbose_name="Nr FV rozliczającej", blank=True)
    zal3         = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="FV rozliczająca")
    zal3_bi      = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Brutto Inne")
    kwota_netto  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota [NETTO]")
    kwota_brutto = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota [BRUTTO]")
    kwota_netto_pl = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11,  verbose_name="Kwota [NETTO PLN]")
    kurs_walut   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11,  verbose_name="Kurs walut")
    data_zam     = models.DateField(verbose_name="Data zamówienia", null=True,  blank=True)
    data_dost    = models.DateField(verbose_name="Data dostawy", null=True,  blank=True)
    data_fv      = models.DateField(verbose_name="Data faktury", null=True,  blank=True)
    nr_fv        = models.CharField(max_length=100, verbose_name="Nr faktury", blank=True)
    roz          = models.BooleanField(default=False, verbose_name="Akceptacja")
    kontrola     = models.IntegerField(default=0, verbose_name="Kontrola")
    uwagi        = models.TextField(blank=True, verbose_name="Uwagi")
    inicjaly     = models.CharField(max_length=10, verbose_name="Inicjały", blank=True)


    def save(self, *args, **kwargs):
        super(Zamowienie, self).save(*args, **kwargs)

    def __str__(self):
        return self.opis

    class Meta:
        verbose_name = "Zamowienie"
        verbose_name_plural = "Zamowienia"


@receiver(pre_save, sender=Zamowienie)
def pozycja_przed_zapisem(sender, instance, **kwargs):
    pass



@receiver(post_save, sender=Zamowienie)
def pozycja_po_zapisaniu(sender, instance, **kwargs):
    aktualizacja_danych()


@receiver(post_delete, sender=Zamowienie)
def pozycja_po_skasowaniu(sender, instance, **kwargs):
    aktualizacja_danych()

# przekazanie do sda-calc informacji o potrzebie przeliczenia danych
def aktualizacja_danych():
    x = FlagaZmiany.objects.all().first()
    x.zamowienie = 1
    x.save()


