from django.db import models
from django.utils import timezone

class Dowod(models.Model):
    imie     = models.CharField(max_length=100, verbose_name="Imię")
    nazwisko = models.CharField(max_length=100, verbose_name="Nazwisko")
    img1     = models.FileField(upload_to='documents', verbose_name="Zdjęcie", blank=True)
    img2     = models.FileField(upload_to='documents', verbose_name="Zdjęcie", blank=True)
    data     = models.DateTimeField(default=timezone.now, verbose_name="Data wprowadzenia")
    uwagi    = models.TextField(blank=True, verbose_name="Uwagi")

    def __str__(self):
        return self.nazwisko

    class Meta:
        verbose_name = "Dowod"
        verbose_name_plural = "Dowody"
