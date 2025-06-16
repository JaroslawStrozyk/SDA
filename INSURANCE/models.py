from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField


class Ubezpieczenie(models.Model):
    CHOISES_WHAT = (
        ('Ubezpieczenie', 'Ubezpieczenie'),
        ('Inne', 'Inne'),
    )
    rodzaj   = models.CharField(max_length=100, verbose_name="Rodzaj dokumentu", choices=CHOISES_WHAT, default='Ubezpieczenie')
    firma    = models.CharField(max_length=200, verbose_name="Firma", default='')
    nazwa    = models.CharField(max_length=200, verbose_name="Nr Polisy", default='')
    dotyczy  = models.CharField(max_length=200, verbose_name="Przedmiot ubezpieczenia", default='')
    suma     = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma ubezpieczenia")
    skladka  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Skladka")
    doc1     = models.FileField(upload_to='insurance', verbose_name="Dokument 1", blank=True)
    doc2     = models.FileField(upload_to='insurance', verbose_name="Dokument 2", blank=True)
    data_od  = models.DateField(default=timezone.now, verbose_name="Data od")
    data_do  = models.DateField(default=timezone.now, verbose_name="Data do")
    raty     = models.BooleanField(default=False, verbose_name="Raty")
    data_raty = models.DateField( verbose_name="Data raty", null=True, blank=True )
    uwagi    = models.TextField(blank=True, verbose_name="Uwagi")
    stu      = models.IntegerField(default=0, verbose_name="Status ubezpieczenia ")

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Ubezpieczenie"
        verbose_name_plural = "Ubezpieczenia"


class Termin(models.Model):

    firma    = models.CharField(max_length=200, verbose_name="Firma", default='')
    dotyczy  = models.CharField(max_length=200, verbose_name="Opis", default='')
    suma     = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma ubezpieczenia")
    skladka  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Skladka")
    doc1     = models.FileField(upload_to='insurance', verbose_name="Dokument 1", blank=True)
    doc2     = models.FileField(upload_to='insurance', verbose_name="Dokument 2", blank=True)
    data_od  = models.DateField(default=timezone.now, verbose_name="Data od")
    data_do  = models.DateField(default=timezone.now, verbose_name="Data do")
    uwagi    = models.TextField(blank=True, verbose_name="Uwagi")
    stt      = models.IntegerField(default=0, verbose_name="Status terminu ")

    def __str__(self):
        return self.firma

    class Meta:
        verbose_name = "Termin"
        verbose_name_plural = "Terminy"