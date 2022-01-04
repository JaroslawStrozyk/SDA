from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver




class ModulName(models.Model):
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa",blank=True)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Moduł Źródłowy"
        verbose_name_plural = "Moduły Źródłowe"


class ErrorList(models.Model):
    nazwa = models.CharField(max_length=150, verbose_name="Nazwa",blank=True)
    status_id = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Status id")
    status = models.CharField(max_length=10, verbose_name="Status", null=True, blank=True)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "ErrorList"
        verbose_name_plural = "ErrorListy"


class Log(models.Model):
    status_id = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Status id")
    status = models.CharField(max_length=10, verbose_name="Status", null=True, blank=True)
    data = models.DateField(verbose_name="Data", null=True,  blank=True)
    godz = models.TimeField(verbose_name="Godz", null=True,  blank=True)
    modul = models.ForeignKey('ModulName', verbose_name="ID Modułu", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    komunikat = models.ForeignKey('ErrorList', verbose_name="ID Komunikatu", max_length=150, on_delete=models.SET_NULL, null=True, blank=True)
    opis = models.CharField(max_length=400, verbose_name="Opis", null=True, blank=True)
    kto = models.CharField(max_length=10, verbose_name="Kto", null=True, blank=True)
    nowy = models.BooleanField(default=False, verbose_name="Nowy wpis")

    def save(self, *args, **kwargs):
        super(Log, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)
        #return str(self.data) + " " + str(self.godz)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

