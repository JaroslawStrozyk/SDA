from django.db import models

class Lan(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True, verbose_name="Adres IP")
    nazwa = models.CharField(max_length=250, blank=True, verbose_name="Nazwa")
    typ = models.CharField(max_length=250, blank=True, verbose_name="Typ")
    opis = models.CharField(max_length=250, blank=True, verbose_name="Opis")
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "LAN"
        verbose_name_plural = "LAN-y"
