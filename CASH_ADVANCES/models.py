from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ORDERS.models import NrSDE, NrMPK
from .functions import CheckCurrency
from TaskAPI.models import FlagaZmiany


class Rozliczenie(models.Model):
    rok = models.IntegerField(default=0, verbose_name="Rok", blank=True)
    data_zal = models.DateField(default=timezone.now, verbose_name="Data zaliczki", blank=True)
    data_roz = models.DateField(verbose_name="Data rozliczenia", null=True, blank=True)
    kw = models.CharField(max_length=300, verbose_name="Nr KW", blank=True)
    nazwisko = models.CharField(max_length=250, blank=True, verbose_name="Nazwisko i Imię")
    zal_kwota = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota zaliczki", blank=True)
    zal_suma = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma wydatków", blank=True)
    saldo = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Saldo", blank=True)
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")
    roz = models.BooleanField(default=False, verbose_name="Rozliczono")
    przek = models.BooleanField(default=False, verbose_name="Przekazano do rozliczenia")
    kontrola = models.IntegerField(default=0, verbose_name="Kontrola", blank=True)
    inicjaly = models.CharField(max_length=10, verbose_name="Inicjały", blank=True)
    flaga_zmian = models.BooleanField(default=False, verbose_name="Zmiany w pozycjach dla tej zaliczki")

    def __str__(self):
        return '{}__[{}]__{}'.format(self.data_zal.strftime('%Y-%m-%d'), self.inicjaly, self.nazwisko)

    class Meta:
        verbose_name = "Rozliczenie"
        verbose_name_plural = "Rozliczenia"


class Pozycja(models.Model):
    rok = models.IntegerField(default=0, verbose_name="Rok")
    nr_roz = models.ForeignKey('Rozliczenie', verbose_name="Zaliczka", max_length=100, on_delete=models.CASCADE)
    kontrahent = models.CharField(max_length=300, verbose_name="Kontrahent", blank=True)
    nr_fv = models.CharField(max_length=100, verbose_name="Nr faktury", blank=True)
    kwota_netto = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota netto")
    kwota_brutto = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota brutto")
    data_zam = models.DateField(verbose_name="Data zamówienia", null=True, blank=True)
    data_zak = models.DateField(verbose_name="Data zakupu/Data FV", null=True, blank=True)
    opis = models.CharField(max_length=300, verbose_name="Opis zamówienia", blank=True)
    nr_sde = models.ForeignKey(NrSDE, verbose_name="Nr SDE", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    nr_mpk = models.ForeignKey(NrMPK, verbose_name="Nr MPK", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    kontrola = models.IntegerField(default=0, verbose_name="Kontrola", blank=True)
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")
    inicjaly = models.CharField(max_length=10, verbose_name="Inicjały", blank=True)
    kwota_netto_pl = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota [NETTO PLN]")
    kurs_walut = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs walut")

    def save(self, *args, **kwargs):
        super(Pozycja, self).save(*args, **kwargs)

    def __str__(self):
        return self.opis

    class Meta:
        verbose_name = "Pozycja"
        verbose_name_plural = "Pozycje"


@receiver(post_save, sender=Pozycja)
def pozycja_po_zapisaniu(sender, instance, **kwargs):
    aktualizacja_rozliczen(instance)
    aktualizacja_danych_p()


@receiver(post_delete, sender=Pozycja)
def pozycja_po_skasowaniu(sender, instance, **kwargs):
    aktualizacja_rozliczen(instance)
    aktualizacja_danych_p()


def aktualizacja_rozliczen(instance):
    pk = instance.nr_roz.id
    zal_kwota = instance.nr_roz.zal_kwota
    zal_suma = CheckCurrency(zal_kwota)
    poz = Pozycja.objects.filter(nr_roz=pk, data_zak__isnull=False)
    for pz in poz:
        zal_suma = zal_suma + pz.kwota_brutto
    saldo = zal_kwota - zal_suma

    r = Rozliczenie.objects.get(id=pk)
    r.zal_suma = zal_suma
    r.saldo = saldo
    r.save()


# przekazanie do sda-calc informacji o potrzebie przeliczenia danych
def aktualizacja_danych_p():
    x = FlagaZmiany.objects.all().first()
    x.pozycja = 1
    x.save()
