from django.db import models
from django.utils import timezone


class Ubezpieczenie(models.Model):
    nazwa    = models.CharField(max_length=200, verbose_name="Nazwa/Nr Polisy")
    dotyczy  = models.CharField(max_length=200, verbose_name="Czego/kogo dotyczy")
    opiekun  = models.CharField(max_length=100, verbose_name="Opiekun (Imię i Nazwisko)")
    skn1     = models.FileField(upload_to='insurance', verbose_name="Skan1", blank=True)
    skn2     = models.FileField(upload_to='insurance', verbose_name="Skan2", blank=True)
    daod     = models.DateField(default=timezone.now, verbose_name="Data od")
    dado     = models.DateField(default=timezone.now, verbose_name="Data do")
    uwagi    = models.TextField(blank=True, verbose_name="Uwagi")

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Ubezpieczenie"
        verbose_name_plural = "Ubezpieczenia"
