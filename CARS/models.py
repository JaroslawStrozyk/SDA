from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField
from django.db.models.signals import pre_save
from django.conf import settings
from TaskAPI.functions import TestData, TestDataT
from django.dispatch import receiver

class Auto(models.Model):
    CHOISES_WHAT = (
        ('AUTO', 'Auto'),
        ('WUWI', 'Wózek widłowy'),
        ('INNY', 'Inny sprzęt'),
    )
    rodzaj   = models.CharField(max_length=100, verbose_name="Rodzaj pojazdu", choices=CHOISES_WHAT, default='AUTO')
    typ      = models.CharField(max_length=100, verbose_name="Typ")
    rej      = models.CharField(max_length=100, verbose_name="Nr rejestracyjny/ser.")
    imie_n   = models.CharField(max_length=100, verbose_name="Imię i Nazwisko", blank=True)
    opis     = models.CharField(max_length=200, verbose_name="Opis/Lokalizacja", blank=True)
    img1     = models.FileField(upload_to='cars', verbose_name="Skan", blank=True)
    img2     = models.FileField(upload_to='cars', verbose_name="Skan", blank=True)
    data     = models.DateTimeField(default=timezone.now, verbose_name="Data wprowadzenia")
    us       = models.DateField(default=timezone.now, verbose_name="Data ubezpieczenia")
    ps       = models.DateField(default=timezone.now, verbose_name="Data przeglądu")
    pt       = models.DateField(verbose_name="Data przeglądu tachometru", null=True, blank=True)
    stu      = models.IntegerField(default=0, verbose_name="Status ubezpieczenia ")
    stp      = models.IntegerField(default=0, verbose_name="Status przeglądu")
    spt      = models.IntegerField(default=0, verbose_name="Status przeglądu tachometru")
    nul      = models.CharField(max_length=100, verbose_name="Nr umowy leasingu", blank=True)
    drl      = models.DateField(default=timezone.now, verbose_name="Data rozp. leasingu")
    dzl      = models.DateField(default=timezone.now, verbose_name="Data zakon. leasingu")
    rul      = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Rata leasingu")
    arch     = models.BooleanField(default=False, verbose_name="Sprzet Archiwalny")
    stdrl    = models.IntegerField(default=0, verbose_name="Status data leasing start ")
    stdzl    = models.IntegerField(default=0, verbose_name="Status data leasing koniec")
    koniecl  = models.BooleanField(default=False, verbose_name="Koniec Leasingu")
    sprzedany = models.BooleanField(default=False, verbose_name="Sprzedany")
    uwagi    = models.TextField(blank=True, verbose_name="Uwagi")
    deleg_auto = models.BooleanField(default=False, verbose_name="Widok auta w delegacji")

    def __str__(self):
        return str(self.rej) + " [" + str(self.typ) + "]"

    class Meta:
        verbose_name = "Auto"
        verbose_name_plural = "Auta"

@ receiver(pre_save, sender=Auto)
def auto_zapis(sender, instance, **kwargs):
    shift = settings.CARS_DATE_SHIFT
    lshift = settings.CARS_LEASING_SHIFT
    if instance.arch == False:
        instance.stu = TestData(str(instance.us), shift, instance.koniecl, instance.sprzedany, instance.arch, False)
        instance.stp = TestData(str(instance.ps), shift, instance.koniecl, instance.sprzedany, instance.arch, False)
        instance.spt = TestDataT(str(instance.pt), shift, instance.koniecl, instance.sprzedany, instance.arch, False)
        instance.stdrl = 0
        instance.stdzl = TestData(str(instance.dzl), lshift, instance.koniecl, instance.sprzedany, instance.arch, True)
    else:
        instance.stu = 0
        instance.stp = 0
        instance.stdrl = 0
        instance.stdzl = 0


