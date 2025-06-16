from django.db import models
from djmoney.models.fields import MoneyField
from datetime import datetime, timedelta
from ORDERS.models import NrSDE
from django.conf import settings
from TaskAPI.models import Rok, URok
from moneyed import Money, PLN

class Pracownik(models.Model):
    CHOISES_GROUP = (
        ('BIURO', 'BIURO'),
        ('PRODUKCJA', 'PRODUKCJA')
    )
    CHOISES_SEC = (
        ('PROJEKTANT', 'PROJEKTANT'),
        ('GRAFIK', 'GRAFIK'),
        ('MARKETING', 'MARKETING'),
        ('TM', 'TM'),
        ('PM', 'PM'),
        ('LOGISTYKA', 'LOGISTYKA'),
        ('KIEROWCA', 'KIEROWCA'),
        ('CNC', 'CNC'),
        ('STOLARZ', 'STOLARZ'),
        ('MONTAZYSTA', 'MONTAZYSTA'),
        ('MAGAZYN', 'MAGAZYN'),
        ('ZAOPATRZENIE', 'ZAOPATRZENIE'),
        ('ADMINISTRACJA', 'ADMINISTRACJA'),
        ('ZARZĄD', 'ZARZĄD')
    )
    CHOISES_EMPLOY = (
        ('UMOWA', 'UMOWA'),
        ('DZIAŁALNOŚĆ', 'DZIAŁALNOŚĆ')
    )
    imie           = models.CharField(max_length=100, verbose_name="Imię", blank=True, default='')
    nazwisko       = models.CharField(max_length=100, verbose_name="Nazwisko", blank=True, default='')
    grupa          = models.CharField(max_length=300, blank=True, verbose_name="Grupa", choices=CHOISES_GROUP, default='')
    dzial          = models.CharField(max_length=300, blank=True, verbose_name="Dział", choices=CHOISES_SEC, default='')
    zatrudnienie   = models.CharField(max_length=300, blank=True, verbose_name="Zatrudnienie", choices=CHOISES_EMPLOY, default='UMOWA')
    wymiar         = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Wymiar zatrudnienia")
    data_zat       = models.DateField(null=True, blank=True, verbose_name="Data zatrudnienia")
    staz           = models.IntegerField(default=0, verbose_name="Staż pracy")
    pensja_ust     = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Ustalona pensja")
    pensja_brutto  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Pensja [brutto]")
    stawka_godz    = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Stawka godz.")
    #stawka_nadgodz = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nadgodziny stawka")
    stawka_wyj_rob = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11,verbose_name="Wyjazd stawka dni rob.")
    stawka_wyj     = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wyjazd stawka")
    ppk            = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="PPK")
    dystans        = models.IntegerField(default=0, verbose_name="Dystans [km]")
    uwagi          = models.TextField(blank=True, verbose_name="Uwagi")
    pracuje        = models.BooleanField(default=True, verbose_name="Pracuje")
    maska          = models.BooleanField(default=False, verbose_name="Maska - nie wyświetlać")
    lp_biuro       = models.BooleanField(default=True, verbose_name="Lista płac biura")

    @classmethod
    def ilosc_pracownikow(cls):
        return cls.objects.filter(pracuje=True).count()


    def __str__(self):
        return self.imie+" "+self.nazwisko

    class Meta:
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"


class Pensja(models.Model):
    rok = models.IntegerField(default=datetime.now().year, verbose_name="Rok") # <<== GEN MC
    miesiac = models.IntegerField(default=datetime.now().month, verbose_name="Miesiąc") # <<== GEN MC
    osoba = models.CharField(max_length=200, verbose_name="Imię i Nazwisko", blank=True, default='') # <<== GEN MC
    pracownik = models.ForeignKey('Pracownik', verbose_name="Pracownik", max_length=100,  on_delete=models.SET_NULL, null=True, blank=True) # <<== GEN MC
    wynagrodzenie = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wynagrodzenie") # <<== GEN MC
    ppk = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="PPK")
    przelew = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Przelew")
    gotowka = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Gotówka")
    dodatek = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Extra dodatek")
    dodatek_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Extra dodatek - opis")
    obciazenie = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Obciążenie")
    obciazenie_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Opis obciążenia")
    km_stawka  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kilome. stawka")
    km_dystans = models.IntegerField(default=0, verbose_name="Dystans [km]")
    km_ilosc = models.IntegerField(default=0, verbose_name="Kilometrówka ilość dni")
    km_wartosc = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kilome. wartość")
    stawka_nadgodz = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nadgodziny stawka")
    nadgodz_ilosc = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Ilość nadgodzin")
    nadgodz =  MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Nadgodziny")
    nadgodz_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Opis nadgodziny")
    stawka_wyj_rob = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wyjazd stawka dni rob.") # <<== GEN MC
    stawka_wyj = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wyjazd stawka") # <<== GEN MC
    del_rozli = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Różnica rozliczenie") # < == calc_Del_to_Pensja() # pensja.del_rozli = pensja.del_rozli + delegacja.roznica_diet_pl
    del_ilosc_st = models.IntegerField(default=0, verbose_name="Wyjazd standard")
    del_ilosc_so = models.IntegerField(default=0, verbose_name="Wyjazd weekend [SO]")
    del_ilosc_we = models.IntegerField(default=0, verbose_name="Wyjazd weekend [ND]")
    del_ilosc_razem = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Delegacja razem")
    del_ilosc_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Opis delegacji")
    premia = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Premia")
    premia_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Opis premii")
    razem  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Razem")
    zaliczka = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Zaliczka")
    komornik = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Komornik")
    brutto_brutto = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Brutto brutto")
    wyplata = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wypłata")
    sum_kosztow = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma kosztów")
    rozliczono = models.BooleanField(default=False, verbose_name="Rozliczono")
    l4 =  models.BooleanField(default=False, verbose_name="L4")
    uwagi = models.TextField(blank=True, verbose_name="Uwagi")
    suma_pd = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma premii i delegacji") # < == calc_Del_to_Pensja() # pensja.suma_pd = pensja.premia + pensja.del_ilosc_razem + pensja.del_rozli
    blokada = models.BooleanField(default=False, verbose_name="Blokada miesiąca")

    @classmethod
    def flaga_ilosc_pensja(cls, rok, bmc):
        pens_ilosc = cls.objects.filter(rok=rok, miesiac=bmc).count()
        if pens_ilosc > 0:
            mc_test = True
        else:
            mc_test = False
        return mc_test

    def __str__(self):
        return str(self.pk) # + " [" + str(self.rok) + "/" + str(self.miesiac) + "] (" + str(self.osoba) + "/" + str(self.pracownik.nazwisko) + " " + str(self.pracownik.imie) + ")"

    class Meta:
        verbose_name = "Pensja"
        verbose_name_plural = "Pensje"


class Podsumowanie(models.Model):
    rok = models.IntegerField(default=datetime.now().year, verbose_name="Rok")
    miesiac = models.IntegerField(default=datetime.now().month, verbose_name="Miesiąc")
    suma_biuro = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma biuro")
    def __str__(self):
        return str(self.suma_biuro)

    class Meta:
        verbose_name = "Podsumowanie"
        verbose_name_plural = "Podsumowania"

class Import(models.Model):
    up_load = models.FileField(upload_to='import', verbose_name="Pliki PDF", blank=True)

    def __str__(self):
        return str(self.up_load)

    class Meta:
        verbose_name = "Import"
        verbose_name_plural = "Importy"


class Stoisko(models.Model):
    wielkosc = models.CharField(max_length=200, blank=True, default='', verbose_name="Wielkość stoiska")
    w_premii  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Premia")

    def __str__(self):
        return str(self.wielkosc)

    class Meta:
        verbose_name = "Stoisko"
        verbose_name_plural = "Stoiska"


class Premia_det(models.Model):
    pensja    = models.ForeignKey('Pensja', verbose_name="Pensja", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    projekt   = models.ForeignKey(NrSDE, verbose_name="Projekt", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)  # null=True, blank=True
    pr_wielkosc = models.ForeignKey('Stoisko', verbose_name="Wielkość stoiska", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    pr_wartosc = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11,verbose_name="Premia za stoisko")
    del_ilosc_st = models.IntegerField(default=0, verbose_name="Ilośc dni roboczych")
    del_ilosc_so = models.IntegerField(default=0, verbose_name="Ilość dni weekendowych [SO]")
    del_ilosc_we = models.IntegerField(default=0, verbose_name="Ilość dni weekendowych [ND]")
    del_ilosc_razem = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wyjazd razem")
    kw_sprzedazy = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota sprzedaży")
    premia_proj = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Premia za projekt")
    ind_pr_kwota = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11,verbose_name="Indywidualna premia")
    ind_pr_opis = models.CharField(max_length=200, blank=True, default='', verbose_name="Opis premii")
    akc = models.BooleanField(default=False, verbose_name="Akceptacja")


    def __str__(self):
        return str(self.pensja)

    class Meta:
        verbose_name = "Premia"
        verbose_name_plural = "Premie"


# class UserTech:
#     def name_log(self, request):
#         name_log = request.user.first_name + " " + request.user.last_name
#         return name_log
#
#     def inicjaly(self, request):
#         name_log = request.user.first_name + " " + request.user.last_name
#         inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
#         return inicjaly
#
#     def about(self):
#         return settings.INFO_PROGRAM
#
#     def test_rok(self, request):
#         tst = Rok.objects.all().order_by('rok')
#         lata = []
#         for t in tst:
#             lata.append(t.rok)
#         name_log = request.user.first_name + " " + request.user.last_name
#         inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
#
#         brok = datetime.now().strftime("%Y")
#         bmc = datetime.now().strftime("%m")
#
#         try:
#             rok = URok.objects.get(nazwa=inicjaly).rok
#         except:
#             p = URok(nazwa=inicjaly, rok=int(brok))
#             p.save()
#             rok = int(brok)
#
#         return lata, rok, brok, bmc
#
#     def biezacy_miesiac(self):
#         return datetime.now().strftime("%m")


# class CalcPracownik:
#     def oblicz_staz_pracy(self ,staz_p, data_zatrudnienia):
#         roz = 0
#         staz = int(staz_p)
#         if staz == 0:
#             if data_zatrudnienia != "":
#                 d_zat = datetime.strptime(data_zatrudnienia, '%d.%m.%Y')
#                 t = datetime.today()
#                 if d_zat != None:
#                     roz = round((t - d_zat) / timedelta(days=365))
#         else:
#             roz = staz
#         return roz
#
#
#     def oblicz_wszystkim_staz_pracy(self):
#         t = datetime.today().date()
#         for prac in Pracownik.objects.all():
#             d_zat = prac.data_zat
#             if d_zat != None:
#                 roz = round((t - d_zat) / timedelta(days=365))
#             else:
#                 roz = 0
#             prac.staz = roz
#             prac.save()
#
#
#     def oblicz_stawke_wyj(self, pensja):
#         pens = Money(str(pensja), PLN)
#         pens = (pens / 168) * 8
#         return pens