from django.db import models
from django.utils import timezone

class Telefon(models.Model):
    usr = models.CharField(max_length=100, verbose_name="Użytkownik")
    model = models.CharField(max_length=200, verbose_name="Model telefonu")
    imei =  models.CharField(max_length=200, verbose_name="IMEI telefonu")
    sim = models.CharField(blank=True, max_length=200, verbose_name="Nr karty SIM")
    msisdn = models.CharField(blank=True, max_length=200, verbose_name="Nr MSISDN")
    kod = models.CharField(blank=True, max_length=200, verbose_name="Kod Blokady")
    bkod = models.BooleanField(default=False, verbose_name="Brak kodu blokady")
    konto = models.CharField(blank=True, max_length=200, verbose_name="Konto")
    haslo = models.CharField(blank=True, max_length=200, verbose_name="Hasło")
    data = models.DateField(default=timezone.now, verbose_name="Data przekazania")
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")
    arch = models.BooleanField(default=False,  verbose_name="Konfiguracja Archiwalna")
    mag = models.BooleanField(default=False, verbose_name="Magazyn")
    pz = models.DateField(default=timezone.now, verbose_name="Data zdania")
    doc = models.FileField(upload_to='protokoly', verbose_name="Dokument przyjęcia", blank=True)
    docz = models.FileField(upload_to='protokoly', verbose_name="Dokument zdania", blank=True)
    zam  = models.CharField(blank=True, max_length=300, verbose_name="Zamieszkały")
    pesel = models.CharField(blank=True, max_length=100, verbose_name="PESEL")


    def __str__(self):
        return self.usr

    class Meta:
        verbose_name = "Telefon"
        verbose_name_plural = "Telefony"
