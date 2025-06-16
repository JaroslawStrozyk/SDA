from djmoney.models.fields import MoneyField
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ORDERS.models import NrSDE
from SDA.settings import DEL_INV_OP
import datetime
from CARS.models import Auto
from INVOICES.models import Osoba


class Dieta(models.Model):
    panstwo = models.CharField(max_length=100, verbose_name="Państwo", blank=True, default='')
    dieta   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Dieta")
    nocleg  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nocleg")

    def __str__(self):
        return self.panstwo

    class Meta:
        verbose_name = "Dieta"
        verbose_name_plural = "Diety"


class Delegacja(models.Model):
    CHOISES_PM = DEL_INV_OP

    CHOISES_CON = (
        ('SKYPE', 'SKYPE'),
        ('E-MAIL', 'E-MAIL'),
        ('BEZ POTWIERDZENIA', 'BEZ POTWIERDZENIA')
    )

    CHOISES_COUNTRY = (
        ('Afganistan', 'Afganistan'),
        ('Albania', 'Albania'),
        ('Algieria', 'Algieria'),
        ('Andora', 'Andora'),
        ('Angola', 'Angola'),
        ('Arabia Saudyjska', 'Arabia Saudyjska'),
        ('Argentyna', 'Argentyna'),
        ('Armenia', 'Armenia'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbejdżan', 'Azerbejdżan'),
        ('Bangladesz', 'Bangladesz'),
        ('Belgia', 'Belgia'),
        ('Białoruś', 'Białoruś'),
        ('Bośnia i Hercegowina', 'Bośnia i Hercegowina'),
        ('Brazylia', 'Brazylia'),
        ('Bułgaria', 'Bułgaria'),
        ('Chile', 'Chile'),
        ('Chiny', 'Chiny'),
        ('Chorwacja', 'Chorwacja'),
        ('Cypr', 'Cypr'),
        ('Czechy', 'Czechy'),
        ('Dania', 'Dania'),
        ('Egipt', 'Egipt'),
        ('Ekwador', 'Ekwador'),
        ('Estonia', 'Estonia'),
        ('Etiopia', 'Etiopia'),
        ('Finlandia', 'Finlandia'),
        ('Francja', 'Francja'),
        ('Gibraltar', 'Gibraltar'),
        ('Grecja', 'Grecja'),
        ('Gruzja', 'Gruzja'),
        ('Hiszpania', 'Hiszpania'),
        ('Hongkong', 'Hongkong'),
        ('Indie', 'Indie'),
        ('Indonezja', 'Indonezja'),
        ('Irak', 'Irak'),
        ('Iran', 'Iran'),
        ('Irlandia', 'Irlandia'),
        ('Islandia', 'Islandia'),
        ('Izrael', 'Izrael'),
        ('Japonia', 'Japonia'),
        ('Jemen', 'Jemen'),
        ('Jordania', 'Jordania'),
        ('Kambodża', 'Kambodża'),
        ('Kanada', 'Kanada'),
        ('Katar', 'Katar'),
        ('Kazachstan', 'Kazachstan'),
        ('Kenia', 'Kenia'),
        ('Kirgistan', 'Kirgistan'),
        ('Kolumbia', 'Kolumbia'),
        ('Kongo, Demokratyczna Republika Konga', 'Kongo, Demokratyczna Republika Konga'),
        ('Korea Południowa', 'Korea Południowa'),
        ('Koreańska Republika Ludowo-Demokratyczna', 'Koreańska Republika Ludowo-Demokratyczna'),
        ('Kostaryka', 'Kostaryka'),
        ('Kuba', 'Kuba'),
        ('Kuwejt', 'Kuwejt'),
        ('Laos', 'Laos'),
        ('Liban', 'Liban'),
        ('Libia', 'Libia'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Litwa', 'Litwa'),
        ('Luksemburg', 'Luksemburg'),
        ('Łotwa', 'Łotwa'),
        ('Macedonia', 'Macedonia'),
        ('Malezja', 'Malezja'),
        ('Malta', 'Malta'),
        ('Maroko', 'Maroko'),
        ('Meksyk', 'Meksyk'),
        ('Mołdowa', 'Mołdowa'),
        ('Monako', 'Monako'),
        ('Mongolia', 'Mongolia'),
        ('Niderlandy', 'Niderlandy'),
        ('Niemcy', 'Niemcy'),
        ('Nigeria', 'Nigeria'),
        ('Norwegia', 'Norwegia'),
        ('Nowa Zelandia', 'Nowa Zelandia'),
        ('Oman', 'Oman'),
        ('Pakistan', 'Pakistan'),
        ('palestyńska Władza Narodowa', 'palestyńska Władza Narodowa'),
        ('Panama', 'Panama'),
        ('Peru', 'Peru'),
        ('Polska', 'Polska'),
        ('Portugalia', 'Portugalia'),
        ('Republika Południowej Afryki', 'Republika Południowej Afryki'),
        ('Rosja', 'Rosja'),
        ('Rumunia', 'Rumunia'),
        ('San Marino', 'San Marino'),
        ('Senegal', 'Senegal'),
        ('Serbia i Czarnogóra', 'Serbia i Czarnogóra'),
        ('Singapur', 'Singapur'),
        ('Słowacja', 'Słowacja'),
        ('Słowenia', 'Słowenia'),
        ('Syria', 'Syria'),
        ('Szwajcaria', 'Szwajcaria'),
        ('Szwecja', 'Szwecja'),
        ('Tadżykistan', 'Tadżykistan'),
        ('Tajlandia', 'Tajlandia'),
        ('Tajwan', 'Tajwan'),
        ('Tanzania', 'Tanzania'),
        ('Tunezja', 'Tunezja'),
        ('Turcja', 'Turcja'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Ukraina', 'Ukraina'),
        ('Urugwaj', 'Urugwaj'),
        ('USA - Nowy Jork', 'USA - Nowy Jork'),
        ('USA - poza Nowym Jorkiem i Waszyngtonem', 'USA - poza Nowym Jorkiem i Waszyngtonem'),
        ('USA - Waszyngton', 'USA - Waszyngton'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Wenezuela', 'Wenezuela'),
        ('Węgry', 'Węgry'),
        ('Wielka Brytania', 'Wielka Brytania'),
        ('Wietnam', 'Wietnam'),
        ('Włochy', 'Włochy'),
        ('Wybrzeże Kości Słoniowej', 'Wybrzeże Kości Słoniowej'),
        ('Zimbabwe', 'Zimbabwe'),
        ('Zjednoczone Emiraty Arabskie', 'Zjednoczone Emiraty Arabskie'),
        ('INNE', 'INNE')
    )

    CHOISES_DRV = (
        ('SAMOLOT', 'SAMOLOT'),
        ('SAMOCHÓD', 'SAMOCHÓD'),
        ('SAMOCHÓD FIRMOWY', 'SAMOCHÓD FIRMOWY'),
        ('POCIĄG', 'POCIĄG'),
        ('AUTOBUS', 'AUTOBUS')
    )

    dataz          = models.DateField(verbose_name="Data zgłoszenia", default=timezone.now)
    data_pobr_zal  = models.DateField(verbose_name="Data pobrania zaliczki", default=timezone.now)
    kursz          = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty zaliczki")
    kurs_dataz     = models.DateField(verbose_name="Data notowania zaliczki", null=True, blank=True)
    numer          = models.CharField(max_length=50, verbose_name="Numer dokumentu", default='')
    naz_imie       = models.CharField(max_length=300, verbose_name="Imię i Nazwisko", choices=CHOISES_PM, default='')
    osoba          = models.ForeignKey(Osoba, verbose_name="Imię i Nazwisko", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    targi          = models.CharField(max_length=200, verbose_name="Nazwa Targów", blank=True, default='')
    lok_targi      = models.CharField(max_length=200, verbose_name="Kraj docelowy", choices=CHOISES_COUNTRY, default='Polska')
    data_od        = models.DateField(default=timezone.now, verbose_name="Data od")
    data_do        = models.DateField(default=timezone.now, verbose_name="Data do")
    data_rozl      = models.DateField(default=timezone.now, verbose_name="Data rozliczenia")
    cel_wyj        = models.CharField(max_length=200, verbose_name="Cel wyjazdu", blank=True, default='')
    transport      = models.CharField(max_length=50, verbose_name="Środek lokomocji", choices=CHOISES_DRV, default='SAMOLOT')
    silnik_poj     = models.BooleanField(default=True, verbose_name="Pojemność silnika > 900cm³ ?")
    km_ilosc       = models.IntegerField(default=0, verbose_name="Ilość kilometrów")
    prv_paliwo_kr  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Prywatny paliwo kraj")
    koszt_paliwo_kr = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Koszt paliwa kraj")
    koszt_paliwo_za = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Koszt paliwa świat")
    koszt_paliwo_za_pl = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Koszt paliwa świat [PLN]")
    kasa_pln       = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ PLN ]")
    kasa_euro      = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ € ]")
    kasa_euro_pl   = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ € => PLN ]")
    kasa_euro_kurs1 = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="[ € ] Kurs 1")
    kasa_euro_kurs2 = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="[ € ] Kurs 2")
    kasa_funt      = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ £ ] ")
    kasa_funt_pl = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ £ => PLN ]")
    kasa_funt_kurs1 = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="[ £ ] Kurs 1")
    kasa_funt_kurs2 = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="[ £ ] Kurs 2")
    kasa_dolar     = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ $ ] ")
    kasa_dolar_pl = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ $ => PLN ]")
    kasa_dolar_kurs1 = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="[ $ ] Kurs 1")
    kasa_dolar_kurs2 = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="[ $ ] Kurs 2")
    kasa_inna      = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ ₣ ] ")
    kasa_inna_pl = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Gotówka [ ₣ => PLN ]")
    kasa_inna_kurs1 = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="[ ₣ ] Kurs 1")
    kasa_inna_kurs2 = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="[ ₣ ] Kurs 2")
    kasa_karta     = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Karta [ Kwota ]")
    zrobione       = models.BooleanField(default=False, verbose_name="Rozliczono")
    pobrane_pw     = models.BooleanField(default=False, verbose_name="Wystawiono PW")
    confirm        = models.CharField(max_length=50, verbose_name="Potwierdzenie", choices=CHOISES_CON, default='BEZ POTWIERDZENIA')
    dc_rozpo       = models.DateTimeField(default=datetime.datetime.today, verbose_name="Data/Czas rozpoczęcia")
    dc_zakon       = models.DateTimeField(default=datetime.datetime.today, verbose_name="Data/Czas zakończenia")
    przekr_gran    = models.DateTimeField(default=datetime.datetime.today, verbose_name="Przekr. granicy")
    powrot_kraj    = models.DateTimeField(default=datetime.datetime.today, verbose_name="Powrót do Kraju [przekr. granicy]")
    czas_opis      = models.CharField(max_length=200, verbose_name="Opis czas", blank=True, default='')
    sniadanie      = models.IntegerField(default=0, verbose_name="Ilość Śniadań")
    obiad          = models.IntegerField(default=0, verbose_name="Ilość Obiadów")
    kolacja        = models.IntegerField(default=0, verbose_name="Ilość Kolacji")
    nocleg_ilosc_kr = models.IntegerField(default=0, verbose_name="Ilość noclegów kraj")
    nocleg_ilosc_za = models.IntegerField(default=0, verbose_name="Ilość noclegów zagranicznych")
    nocleg_kr      = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nocleg krajowa")
    nocleg_za      = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nocleg zagraniczna")
    nocleg_za_zl   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nocleg zagraniczna [zł]")
    dieta_kr       = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Dieta krajowa")
    dieta_za       = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Dieta zagraniczna")
    dieta_za_zl    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Dieta zagraniczna [zł]")
    dieta_za_euro  = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Dieta zagraniczna [eur]")
    dieta_za_not   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Dieta zagr. notowanie")
    dieta_za_efd   = models.CharField(max_length=200, verbose_name="Dieta EFD", blank=True, default='')
    dieta_razem    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Dieta razem")
    dieta_za_2     = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Dieta zagraniczna 2")
    dieta_za_3     = MoneyField(decimal_places=2, default=0, default_currency='GBP', max_digits=11, verbose_name="Dieta zagraniczna 3")
    dieta_za_4     = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11, verbose_name="Dieta zagraniczna 4")
    dieta_za_5     = MoneyField(decimal_places=2, default=0, default_currency='CHF', max_digits=11, verbose_name="Dieta zagraniczna 5")
    wydatki_sum    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma wydatków [PLN]")
    wydatki_sum_wal = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11,verbose_name="Suma wydatków")
    sum_wydatki1   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma wydatków 1")
    sum_wydatki2   = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Suma wydatków 2")
    sum_wydatki3   = MoneyField(decimal_places=2, default=0, default_currency='GBP', max_digits=11, verbose_name="Suma wydatków 3")
    sum_wydatki4   = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11, verbose_name="Suma wydatków 4")
    sum_wydatki5   = MoneyField(decimal_places=2, default=0, default_currency='CHF', max_digits=11, verbose_name="Suma wydatków 5")
    lacznie_koszty_wal = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Łącznie koszty")
    lacznie_koszty_pln = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Łącznie koszty [PLN]")
    pobr_zal_wal    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Pobrane zaliczki")
    pobr_zal_pln    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Pobrane zaliczki [PLN]")
    suma_koniec     = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma Końcowa")
    suma_koniec_pl  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma końcowa [PLN]")
    kurs           = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty")
    kurs_data      = models.DateField(verbose_name="Data notowania", null=True,  blank=True)
    dane_auta      = models.ForeignKey(Auto, verbose_name="Dane auta", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    podsumowanie1 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Podsumowanie 1")
    podsumowanie2 = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Podsumowanie 2")
    podsumowanie3 = MoneyField(decimal_places=2, default=0, default_currency='GBP', max_digits=11, verbose_name="Podsumowanie 3")
    podsumowanie4 = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11, verbose_name="Podsumowanie 4")
    podsumowanie5 = MoneyField(decimal_places=2, default=0, default_currency='CHF', max_digits=11, verbose_name="Podsumowanie 5")
    podsumowanie_pl2 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Podsumowanie pl 2")
    podsumowanie_pl3 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Podsumowanie pl 3")
    podsumowanie_pl4 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Podsumowanie pl 4")
    podsumowanie_pl5 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Podsumowanie pl 5")
    kursz2 = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty - pobranie 2")
    kursz3 = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty - pobranie 3")
    kursz4 = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty - pobranie 4")
    kursz5 = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty - pobranie 5")
    kurs2 = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty - rozliczenie 2")
    kurs3 = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty - rozliczenie 3")
    kurs4 = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty - rozliczenie 4")
    kurs5 = MoneyField(decimal_places=4, default=0, default_currency='PLN', max_digits=11, verbose_name="Kurs waluty - rozliczenie 5")
    zaliczka1 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Zaliczka 1")
    zaliczka2 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Zaliczka 2")
    zaliczka3 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Zaliczka 3")
    zaliczka4 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Zaliczka 4")
    zaliczka5 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Zaliczka 5")
    wd1 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wydatki + Diety 1")
    wd2 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wydatki + Diety 2")
    wd3 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wydatki + Diety 3")
    wd4 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wydatki + Diety 4")
    wd5 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wydatki + Diety 5")
    suma0 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma 0")
    suma1 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma 1")
    suma2 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma 2")
    suma3 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma 3")
    suma4 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma 4")
    suma5 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma 5")
    czysta_dieta = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Czysta dieta")
    roznica_diet = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Różnica diet")
    roznica_diet_pl = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Różnica diet [PLN]")
    kod_sde_targi1 = models.ForeignKey(NrSDE, related_name='sample1', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Kod SDE Targi 1")
    kod_sde_targi2 = models.ForeignKey(NrSDE, related_name='sample2', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Kod SDE Targi 2")
    sde_targi1_pln = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="SDE Targi 1 PLN")
    sde_targi2_pln = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="SDE Targi 2 PLN")


    def save(self, *args, **kwargs):
        super(Delegacja, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.osoba)

    class Meta:
        verbose_name = "Delegacja"
        verbose_name_plural = "Delegacje"


class Pozycja(models.Model):

    delegacja    = models.ForeignKey('Delegacja', verbose_name="Delegacja", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    pozycja      = models.CharField(max_length=200, verbose_name="Pozycja", blank=True, default='')
    kwota_waluta = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota")
    kwota_pln    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota PLN")
    fwaluta      = models.BooleanField(default=True, verbose_name="Flaga waluty")
    waluta       = models.CharField(max_length=10, verbose_name="Waluta", blank=True, default='PLN')


    def __str__(self):
        return self.pozycja

    class Meta:
        verbose_name = "Pozycja"
        verbose_name_plural = "Pozycje"


@receiver(post_save, sender=Delegacja)
def pozycja_po_zapisaniu(sender, instance, **kwargs):
    pass


@receiver(post_delete, sender=Delegacja)
def pozycja_po_skasowaniu(sender, instance, **kwargs):
    pass


@receiver(post_save, sender=Pozycja)
def pozycja_po_zapisaniu(sender, instance, **kwargs):
    pass


@receiver(post_delete, sender=Pozycja)
def pozycja_po_skasowaniu(sender, instance, **kwargs):
    pass
