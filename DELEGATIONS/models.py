from djmoney.models.fields import MoneyField

from django.db import models
from django.utils import timezone



class Delegacja(models.Model):
    imie       = models.CharField(max_length=100, verbose_name="Imię")
    nazwisko   = models.CharField(max_length=100, verbose_name="Nazwisko")
    targi      = models.CharField(max_length=200, verbose_name="Nazwa Targów")
    data_od    = models.DateField(default=timezone.now, verbose_name="Data od")
    data_do    = models.DateField(default=timezone.now, verbose_name="Data do")
    kasa_pln   = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ PLN ]")
    kasa_euro  = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ € ]")
    kasa_funt  = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ £ ] ")
    kasa_inna  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Gotówka [ Inna ]")
    kasa_karta = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Karta [ Kwota ]")
    zrobione = models.BooleanField(default=False, verbose_name="Wystawione")

    def save(self, *args, **kwargs):
        # print("#############################################################")
        # print("#  Dodano pozycję do delegacji: "+self.nazwisko+"           #")
        # print("#############################################################")
        super(Delegacja, self).save(*args, **kwargs)

    def __str__(self):
        return self.nazwisko

    class Meta:
        verbose_name = "Delegacja"
        verbose_name_plural = "Delegacje"