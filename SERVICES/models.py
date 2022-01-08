from django.db import models


class Usluga(models.Model):
    CHOISES_PAY = (
        ('ROCZNY', 'ROCZNY.'),
        ('MIESIĘCZNY', 'MIESIECZNY.'),
        ('BEZPŁATNY', 'BEZPŁATNY.'),
        ('NIE DOTYCZY', 'NIE DOTYCZY.')
    )
    nazwa_siec = models.CharField(max_length=150, verbose_name="Nazwa sieciowa")
    usr        = models.CharField(blank=True, max_length=100, verbose_name="Użytkownik")
    dostawca   = models.CharField(blank=True, max_length=150, verbose_name="Dostawca")
    hosting    = models.CharField(blank=True, max_length=100, verbose_name="Hosting")
    uwagi      = models.TextField(blank=True, verbose_name="Uwagi")
    zdj        = models.FileField(upload_to='images', verbose_name="Zdjęcie", blank=True)
    okres      = models.CharField(max_length=20, verbose_name="Okres rozliczeniowy", choices=CHOISES_PAY, default='ROCZNY')
    data_waznosci = models.DateField(verbose_name="Data ważności", null=True, blank=True)
    termin = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Termin")

    def save(self, *args, **kwargs):
        super(Usluga, self).save(*args, **kwargs)

    def __str__(self):
        return self.nazwa_siec

    class Meta:
        verbose_name = "Usługa"
        verbose_name_plural = "Usługi"


class Profil(models.Model):
    usluga       = models.ForeignKey(Usluga, on_delete=models.CASCADE, verbose_name="Usługa")
    rodzaj_konta = models.CharField(max_length=200, verbose_name="Rodzaj/program")
    konto        = models.CharField(max_length=100, verbose_name="Nazwa konta")
    haslo        = models.CharField(max_length=100, verbose_name="Hasło konta", blank=True)
    adres        = models.CharField(max_length=100, verbose_name="Adres IP", blank=True)
    uwagi        = models.TextField(blank=True, verbose_name="Uwagi")


    def __str__(self):
        return self.konto

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profile"

