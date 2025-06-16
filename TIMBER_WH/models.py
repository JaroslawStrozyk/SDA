from django.db import models
from djmoney.models.fields import MoneyField
from ORDERS.models import NrSDE
from django.utils import timezone
import datetime




class Plyta(models.Model):
    CHOISES_PLACE = (
        ('MAGAZYN1', 'MAGAZYN Szparagowa'),
        ('MAGAZYN2', 'MAGAZYN Podolany'),
        ('MAGAZYN3', 'MAGAZYN Chemii'),
        ('MAGAZYN4', 'MAGAZYN Szkła'),
        ('MAGAZYN5', 'MAGAZYN Stali')
    )
    CHOISES_TYPE = (
        ('dre', 'MAGAZYN drewna'),
        ('wew', 'MAGAZYN wewnętrzny')
    )
    prod_id = models.IntegerField(default=0, verbose_name="ID Prod.")
    magazyn = models.CharField(max_length=50, verbose_name="Magazyn", choices=CHOISES_PLACE,default='MAGAZYN1')
    rodzaj  = models.CharField(max_length=50, verbose_name="Rodzaj Magazynu", choices=CHOISES_TYPE,default='dre')
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa", blank=True, default='')
    stan  = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Stan")
    jm = models.CharField(max_length=50, verbose_name="Jednostka", default='szt.')
    opis  = models.TextField(blank=True, verbose_name="Opis")
    cena  = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Cena")
    limit = models.DecimalField(max_digits=11, decimal_places=1, default=10.0, verbose_name="Poziom limitu towaru")
    inw_stan = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Inwentura Stan")
    inw_data = models.DateField(verbose_name="Inwentura Data", blank=True, null=True)


    def __str__(self):
        return "["+ str(self.prod_id) + "] " + self.nazwa + " [" + self.opis + "]"

    class Meta:
        verbose_name = "Plyta"
        verbose_name_plural = "Plyty"



class Przychod(models.Model):
    CHOISES_TYPE = (
        ('m²', 'm²'),
        ('m³', 'm³'),
        ('mb', 'mb'),
        ('szt.', 'szt.'),
        ('kompl.', 'kompl.')
    )
    doc_id = models.CharField(max_length=20, verbose_name="ID dok.", blank=True, default='')
    plyta  = models.ForeignKey('Plyta', verbose_name="Płyta", max_length=400, on_delete=models.CASCADE)
    zrodlo = models.CharField(max_length=200, verbose_name="Źródło przychodu", blank=True, default='')
    data   = models.DateField(verbose_name="Data", default=timezone.now)
    ilosc  = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Ilość")
    jm     = models.CharField(max_length=50, verbose_name="Jednostka", choices=CHOISES_TYPE, default='szt.')
    cena   = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Cena")
    cena_j = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Cena jednostkowa")
    inwentura = models.BooleanField(default=False, verbose_name="Inwentura")
    bo = models.BooleanField(default=False, verbose_name="Stan początkowy")

    def __str__(self):
        return "["+self.doc_id+"] "+self.zrodlo
        #return str(self.data)

    class Meta:
        verbose_name = "Przychod"
        verbose_name_plural = "Przychody"


class Rozchod(models.Model):
    CHOISES_TYPE = (
        ('m²', 'm²'),
        ('m³', 'm³'),
        ('mb', 'mb'),
        ('szt.', 'szt.'),
        ('kompl.', 'kompl.')
    )
    doc_id = models.CharField(max_length=20, verbose_name="ID dok.", blank=True, default='')
    rokk  = models.IntegerField(default=datetime.datetime.now().year, verbose_name="Rok Nr SDE")
    plyta = models.ForeignKey('Plyta', verbose_name="Płyta", max_length=400, on_delete=models.CASCADE)
    cel   = models.CharField(max_length=200, verbose_name="Cel rozchodu", blank=True, default='')
    data  = models.DateField(verbose_name="Data", default=timezone.now)
    nr_sde = models.ForeignKey(NrSDE, verbose_name="Nr SDE", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    ilosc = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Ilość")
    jm = models.CharField(max_length=50, verbose_name="Jednostka", choices=CHOISES_TYPE, default='szt.')
    kwota = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota")
    inwentura = models.BooleanField(default=False, verbose_name="Inwentura")
    bo = models.BooleanField(default=False, verbose_name="Bilans otwarcia")

    def __str__(self):
        return "["+self.doc_id+"] "+self.cel
        #return str(self.data)

    class Meta:
        verbose_name = "Rozchod"
        verbose_name_plural = "Rozchod"


class Zwrot(models.Model):
    CHOISES_TYPE = (
        ('m²', 'm²'),
        ('m³', 'm³'),
        ('mb', 'mb'),
        ('szt.', 'szt.'),
        ('kompl.', 'kompl.')
    )
    doc_id = models.CharField(max_length=20, verbose_name="ID dok.", blank=True, default='')
    rokk  = models.IntegerField(default=datetime.datetime.now().year, verbose_name="Rok Nr SDE")
    plyta = models.ForeignKey('Plyta', verbose_name="Płyta", max_length=400, on_delete=models.CASCADE)
    cel   = models.CharField(max_length=200, verbose_name="Opis zwrotu", blank=True, default='')
    data  = models.DateField(verbose_name="Data", default=timezone.now)
    nr_sde = models.ForeignKey(NrSDE, verbose_name="Nr SDE", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    ilosc = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Ilość")
    jm = models.CharField(max_length=50, verbose_name="Jednostka", choices=CHOISES_TYPE, default='szt.')
    kwota = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota")

    def __str__(self):
        return str(self.data)

    class Meta:
        verbose_name = "Zwrot"
        verbose_name_plural = "Zwroty"


class Zestawienie(models.Model):
    rokk  = models.IntegerField(default=datetime.datetime.now().year, verbose_name="Rok Nr SDE")
    plyta = models.ForeignKey('Plyta', verbose_name="Płyta", max_length=400, on_delete=models.CASCADE)
    dok_id= models.CharField(max_length=20, verbose_name="Dok. ID", blank=True, default='')
    data  = models.DateField(verbose_name="Data", default=timezone.now)
    operacja = models.CharField(max_length=200, verbose_name="Operacja", blank=True, default='')
    opis  = models.CharField(max_length=200, verbose_name="Opis", blank=True, default='')
    ilosc = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Ilość")
    jm = models.CharField(max_length=50, verbose_name="Jednostka", default='m²')
    kwota = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota")
    nr_sde = models.ForeignKey(NrSDE, verbose_name="Nr SDE", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.data)

    class Meta:
        verbose_name = "Zestawienie"
        verbose_name_plural = "Zestawienia"


class Statystyka(models.Model):
    rokk  = models.IntegerField(default=datetime.datetime.now().year, verbose_name="Rok")
    nr_sde = models.ForeignKey(NrSDE, verbose_name="Nr SDE", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    mc1 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Styczeń")
    mc2 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Luty")
    mc3 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Marzec")
    mc4 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwiecień")
    mc5 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Maj")
    mc6 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Czerwiec")
    mc7 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Lipiec")
    mc8 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Sierpień")
    mc9 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wrzesień")
    mc10 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Październik")
    mc11 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Listopad")
    mc12 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Grudzień")
    suma = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma")

    def __str__(self):
        return str(self.suma)

    class Meta:
        verbose_name = "Statystyka"
        verbose_name_plural = "Statystyki"


class StanObecny(models.Model):
    plyta = models.ForeignKey('Plyta', verbose_name="Płyta", max_length=400, on_delete=models.CASCADE)
    przychod = models.ForeignKey('Przychod', verbose_name="Przychód", max_length=400, on_delete=models.CASCADE)
    rozchod = models.ForeignKey('Rozchod', verbose_name="Rozchód", max_length=400, on_delete=models.CASCADE)
    p_ilosc = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Przychód - Ilość")
    r_ilosc = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Rozchód - Ilość")
    stan    = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Stan - Ilość")
    nadmiar = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Nadmiar - Ilość")
    p_cena_j = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Cena Jednostkowa")
    wartosc = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wartość")

    def __str__(self):
        return str(self.plyta) + " P:"+str(self.przychod)+" R:"+str(self.rozchod)

    class Meta:
        verbose_name = "StanObecny"
        verbose_name_plural = "StanyObecne"


class Inwentura(models.Model):
    rokk  = models.IntegerField(default=datetime.datetime.now().year, verbose_name="Rok")
    # nr_sde = models.ForeignKey(NrSDE, verbose_name="Nr SDE", max_length=100, on_delete=models.SET_NULL, null=True, blank=True)
    # mc1 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Styczeń")
    # mc2 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Luty")
    # mc3 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Marzec")
    # mc4 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwiecień")
    # mc5 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Maj")
    # mc6 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Czerwiec")
    # mc7 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Lipiec")
    # mc8 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Sierpień")
    # mc9 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Wrzesień")
    # mc10 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Październik")
    # mc11 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Listopad")
    # mc12 = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Grudzień")
    # suma = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Suma")

    def __str__(self):
        return str(self.suma)

    class Meta:
        verbose_name = "Inwentura"
        verbose_name_plural = "Inwentury"

# DODATKOWE TABELE

class RozchodSzczegoly(models.Model):
    rozchod = models.ForeignKey('Rozchod', verbose_name="Rozchod", on_delete=models.CASCADE)
    przychod = models.ForeignKey('Przychod', verbose_name="Przychod", on_delete=models.CASCADE)
    ilosc = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Ilość")
    cena_j = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11,
                        verbose_name="Cena jednostkowa")
    kwota = MoneyField(decimal_places=2, default=0, default_currency='PLN', max_digits=11, verbose_name="Kwota")

    def __str__(self):
        return f"Rozchod {self.rozchod.doc_id}, Przychod {self.przychod.doc_id}, Ilość: {self.ilosc}"

    class Meta:
        verbose_name = "Szczegóły Rozchodu"
        verbose_name_plural = "Szczegóły Rozchodów"


