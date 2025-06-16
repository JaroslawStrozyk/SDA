from django.db import models
from djmoney.models.fields import MoneyField
from ORDERS.models import NrSDE


class Firma(models.Model):
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa firmy", blank=True, default='')

    def __str__(self):
        return self.nazwa
    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmy"

def get_default_firma():
    return Firma.objects.first().id


class Sklad(models.Model):
    CHOISES_PLACE = (
        ('Wysogotowo', 'Wysogotowo'),
        ('Podolany', 'Podolany'),
        ('Jarocin', 'Jarocin')
    )
    magazyn        = models.CharField(max_length=50, verbose_name="Miejsce składowania", choices=CHOISES_PLACE, default='Podolany')
    magazyn_opis   = models.CharField(max_length=100, verbose_name="Miejsce składowania", default='')
    nr_sde         = models.ForeignKey(NrSDE, verbose_name="Stoisko", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    przech_nazwa   = models.CharField(max_length=100, verbose_name="Nazwa towaru", blank=True, default='')
    przech_zdjecie = models.FileField(upload_to='magazyn', verbose_name="Zdjęcie 1", blank=True)
    przech_zdjecie2 = models.FileField(upload_to='magazyn', verbose_name="Zdjęcie 2", blank=True)
    przech_zdjecie3 = models.FileField(upload_to='magazyn', verbose_name="Zdjęcie 3", blank=True)
    przech_zdjecie4 = models.FileField(upload_to='magazyn', verbose_name="Zdjęcie 4", blank=True)
    uszkodz_zdjecie1 = models.FileField(upload_to='magazyn', verbose_name="Uszkodzenie 1", blank=True)
    uszkodz_zdjecie2 = models.FileField(upload_to='magazyn', verbose_name="Uszkodzenie 2", blank=True)
    uszkodz_zdjecie3 = models.FileField(upload_to='magazyn', verbose_name="Uszkodzenie 3", blank=True)
    uszkodz_zdjecie4 = models.FileField(upload_to='magazyn', verbose_name="Uszkodzenie 4", blank=True)
    przech_nrpalet = models.CharField(max_length=100, verbose_name="Numer palety", blank=True, default='')
    przech_sze     = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Szerokość [m]")
    przech_gl      = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Głebokość [m]")
    przech_wys     = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Wysokość [m]")
    przech_pow     = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Powierzchnia przechowywania [m²]")
    wydano_ilosc   = models.IntegerField(default=0, verbose_name="Ile wydano")
    wydano_data    = models.DateField(verbose_name="Data wydania", null=True,  blank=True)
    zwroco_ilosc   = models.IntegerField(default=0, verbose_name="Ile zwrócono")
    zwroco_data    = models.DateField(verbose_name="Data powrotu", null=True,  blank=True)
    zwroco_uwagi   = models.TextField(blank=True, verbose_name="Zwroty - Uwagi")
    czas_od        = models.DateField(verbose_name="Od daty", null=True,  blank=True)
    czas_do        = models.DateField(verbose_name="Do daty", null=True,  blank=True)
    stawka         = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Stawka")
    koszt_przech   = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Koszty przechowywania")
    suma           = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Suma Kosztów")
    suma_pow       = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Całkowita powierzchnia [m²]")
    suma_zw        = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Suma Zwolnień")
    suma_np        = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Suma nie przypisanych")
    faktura        = models.CharField(max_length=100, verbose_name="Numer faktury", blank=True, default='')
    zwolnione      = models.BooleanField(default=False, verbose_name="Zwolnione")
    flaga_op       = models.IntegerField(default=0, verbose_name="Flaga operacji")
    status         = models.IntegerField(default=0, verbose_name="Status")
    status_pracy   = models.BooleanField(default=False, verbose_name="Status pracy")
    blokada        = models.BooleanField(default=False, verbose_name="Blokada daty")
    blokada_zapisu = models.BooleanField(default=False, verbose_name="Blokada zapisu")
    multi_uzycie   = models.BooleanField(default=False, verbose_name="Element Wielokrotnego Użytku")    # Wielokrotne użycie
    multi_uzycie_id = models.BigIntegerField(default=0, verbose_name="MU ID")
    multi_uzycie_st = models.IntegerField(default=0, verbose_name="Ilość użycia")
    firma           = models.ForeignKey('Firma', verbose_name="Firma", max_length=100, on_delete=models.SET_NULL, null=True, blank=True, default=get_default_firma)
    dok_pdf1 = models.FileField(upload_to='magazyn', verbose_name="Lista do przechowywania1", blank=True)
    dok_pdf2 = models.FileField(upload_to='magazyn', verbose_name="Lista do przechowywania2", blank=True)
    dok_pdf3 = models.FileField(upload_to='magazyn', verbose_name="Lista do przechowywania3", blank=True)
    dok_pdf4 = models.FileField(upload_to='magazyn', verbose_name="Lista do przechowywania4", blank=True)
    fv_pdf1 = models.FileField(upload_to='magazyn', verbose_name="Faktura", blank=True)
    uwagi = models.TextField(blank=True, verbose_name="Adnotacje")
    do_skasowania = models.BooleanField(default=False, verbose_name="Skasować?")
    liczyc = models.BooleanField(default=False, verbose_name="Pierwszy wpis do obliczeń")
    ilosc_dni = models.IntegerField(default=0, verbose_name="Liczba dni")

    def __str__(self):
        return self.przech_nazwa
    class Meta:
        verbose_name = "Sklad"
        verbose_name_plural = "Sklady"
