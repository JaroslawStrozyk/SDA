from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField


class System(models.Model):
    nazwa = models.CharField(max_length=250, blank=True, verbose_name="Nazwa")
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Dział"
        verbose_name_plural = "Działy"



class Sprzet(models.Model):
    CHOISES_HOST = (
        ('Komputer', 'Komputer'),
        ('Monitor', 'Monitor'),
        ('Drukarka','Drukarka'),
        ('Serwer','Serwer'),
        ('Access Point', 'Access Point'),
        ('Router', 'Router'),
		('Switch', 'Switch'),
		('Domena', 'Domena'),
		('Tablet', 'Tablet'),
        ('Czytnik', 'Czytnik'),
        ('VOIP', 'VOIP'),
        ('RCP', 'RCP'),
        ('Inne','Inne'),
    )

    CHOISES_STAN = (
        (-1, '-----'),
        (0,  'DO KASACJI LUB USZKODZONY.'),
        (1,  'DOSTATECZNY.'),
        (2,  'DOBRY.'),
        (3,  'BARDZO DOBRY.'),
        (4,  'BARDZO DOBRY Z GWARANCJĄ.'),
    )

    system = models.ForeignKey('System', verbose_name="Dział", max_length=400,  on_delete=models.CASCADE)
    nazwa_siec = models.CharField(max_length=50, verbose_name="Nazwa sieciowa")
    kik = models.CharField(blank=True, max_length=50, verbose_name="Oznaczenie")
    usr =  models.CharField(blank=True, max_length=100, verbose_name="Użytkownik")
    host = models.CharField(max_length=100, verbose_name="Host", choices=CHOISES_HOST, default='Komputer')
    typ = models.CharField(blank=True, max_length=100, verbose_name="Typ")
    adres_ip = models.CharField(blank=True, max_length=200, verbose_name="Adres IP")
    domena = models.CharField(blank=True, max_length=50, verbose_name="Domena")
    sw_gn = models.CharField(blank=True, max_length=50, verbose_name="SW gniazdo")
    snk = models.CharField(blank=True, max_length=200, verbose_name="Nr seryjny Komputera")
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")
    zdj = models.FileField(upload_to='images', verbose_name="Zdjęcie", blank=True)
    arch = models.BooleanField(default=False,  verbose_name="Konfiguracja Archiwalna")
    mag = models.BooleanField(default=False, verbose_name="Magazyn")
    pr = models.DateField(default=timezone.now, verbose_name="Data przyjęcia")
    pz = models.DateField(default=timezone.now, verbose_name="Data zdania")
    gw   = models.DateField(default=timezone.now, verbose_name="Termin Gwarancji")
    doc = models.FileField(upload_to='protokoly', verbose_name="Dokument przyjęcia", blank=True)
    docz = models.FileField(upload_to='protokoly', verbose_name="Dokument zdania", blank=True)
    zam  = models.CharField(blank=True, max_length=300, verbose_name="Zamieszkały")
    pesel = models.CharField(blank=True, max_length=100, verbose_name="PESEL")
    stan = models.DecimalField(max_digits=4, decimal_places=0, default=-1, verbose_name="Stan sprzętu", choices=CHOISES_STAN, )
    opis = models.TextField(blank=True, verbose_name="Opis")
    historia = models.CharField(blank=True, max_length=200, verbose_name="Historia")
    wartosc = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wartość sprzętu")
    sprzedany = models.BooleanField(default=False, verbose_name="Sprzedany")

    def save(self, *args, **kwargs):
        super(Sprzet, self).save(*args, **kwargs)

    def __str__(self):
        return self.nazwa_siec + " [" + self.host + " / " + self.typ + "] " + self.usr

    class Meta:
        verbose_name = "Komputer"
        verbose_name_plural = "Komputery"



class Profil(models.Model):
    CHOISES_PAY = (
        ('NIE', 'NIE'),
        ('TAK', 'TAK'),
    )
    sprzet = models.ForeignKey(Sprzet, on_delete=models.CASCADE, verbose_name="Sprzęt")
    rodzaj_konta = models.CharField(max_length=200, verbose_name="Rodzaj/program")
    kod = models.CharField(max_length=200, verbose_name="Kod", blank=True)
    konto = models.CharField(max_length=100, verbose_name="Nazwa konta")
    haslo = models.CharField(max_length=100, verbose_name="Hasło konta", blank=True)
    adres = models.CharField(max_length=100, verbose_name="Adres IP", blank=True)
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")
    fv = models.FileField(upload_to='faktury', verbose_name="Faktura", blank=True)
    data_waznosci = models.DateField(verbose_name="Data ważności (Puste - jeśli licencja stała)", null=True, blank=True)
    termin = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Termin")
    auto_platnosc = models.CharField(max_length=10, verbose_name="Auto płatność", choices=CHOISES_PAY, default='NIE')
    karta = models.CharField(max_length=150, verbose_name="Karta płatnicza", blank=True)


    def __str__(self):
        return self.konto

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profile"


class Serwis(models.Model):
    sprzet = models.ForeignKey(Sprzet, on_delete=models.CASCADE, verbose_name="Sprzęt")
    data = models.DateField(default=timezone.now, verbose_name="Data")
    problem = models.TextField(blank=True, verbose_name="Problem")
    opis = models.TextField(blank=True, verbose_name="Opis")
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")

    def __str__(self):
        return str(self.data)

    class Meta:
        verbose_name = "Serwis"
        verbose_name_plural = "Serwisy"





