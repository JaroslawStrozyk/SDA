from moneyed import Money, PLN
from django.db.models import Value, CharField, DecimalField
from djmoney.models.fields import MoneyField
from django.db.models import Sum
from TIMBER_WH.calculate import calc_sum_stan
from TIMBER_WH.models import Plyta, Przychod, Rozchod, Statystyka
from django.db.models import Sum

def gen_main_inwent_pdf(brok):
    zero = Money('0.00', PLN)
    out1 = Plyta.objects.filter(magazyn='MAGAZYN1', rodzaj='dre').order_by('rodzaj','nazwa').annotate(
        brak_ceny=Value(0, output_field=DecimalField()),
        suma_wart=Value(zero, output_field=MoneyField(decimal_places=2, default_currency='PLN', max_digits=11)),
        test=Value('?', output_field=CharField(max_length=200))
    ).values('id','rodzaj', 'nazwa', 'opis', 'stan', 'brak_ceny', 'suma_wart', 'test')

    for plyta in out1:
        idp = plyta['id']
        if Przychod.objects.filter(plyta_id=idp, cena_j=0, inwentura=False).count() == 0:
            plyta['brak_ceny'] = 0
            stan = plyta['stan']
            plyta['suma_wart'], plyta['test'] = calc_sum_stan(stan, Przychod.objects.filter(plyta_id=idp, inwentura=False))


    out2 = Plyta.objects.filter(magazyn='MAGAZYN2', rodzaj='dre').order_by('rodzaj','nazwa').annotate(
        brak_ceny=Value(0, output_field=DecimalField()),
        suma_wart=Value(zero, output_field=MoneyField(decimal_places=2, default_currency='PLN', max_digits=11)),
        test=Value('?', output_field=CharField(max_length=200))
    ).values('id','rodzaj', 'nazwa', 'opis', 'stan', 'brak_ceny', 'suma_wart', 'test')

    for plyta in out2:
        idp = plyta['id']
        if Przychod.objects.filter(plyta_id=idp, cena_j=0, inwentura=False).count() == 0:
            plyta['brak_ceny'] = Przychod.objects.filter(plyta_id=idp, cena_j=0, inwentura=False).count()
            stan = plyta['stan']
            plyta['suma_wart'], plyta['test'] = calc_sum_stan(stan, Przychod.objects.filter(plyta_id=idp, inwentura=False))


    out3 = Plyta.objects.filter(magazyn='MAGAZYN3', rodzaj='dre').order_by('rodzaj','nazwa').annotate(
        brak_ceny=Value(0, output_field=DecimalField()),
        suma_wart=Value(zero, output_field=MoneyField(decimal_places=2, default_currency='PLN', max_digits=11)),
        test=Value('?', output_field=CharField(max_length=200))
    ).values('id','rodzaj', 'nazwa', 'opis', 'stan', 'brak_ceny', 'suma_wart', 'test')

    for plyta in out3:
        idp = plyta['id']
        plyta['brak_ceny'] = Przychod.objects.filter(plyta_id=idp, cena_j=0, inwentura=False).count()
        stan = plyta['stan']
        plyta['suma_wart'], plyta['test'] = calc_sum_stan(stan, Przychod.objects.filter(plyta_id=idp, inwentura=False))

    return out1, out2, out3


def gen_main_inwent(brok):
    zero = Money('0.00', PLN)
    out1 = Plyta.objects.filter(magazyn='MAGAZYN1', rodzaj='dre').order_by('rodzaj','nazwa').annotate(
        brak_ceny=Value(0, output_field=DecimalField()),
        suma_wart=Value(zero, output_field=MoneyField(decimal_places=2, default_currency='PLN', max_digits=11)),
        test=Value('?', output_field=CharField(max_length=200))
    ).values('id','rodzaj', 'nazwa', 'opis', 'stan', 'brak_ceny', 'suma_wart', 'test')

    for plyta in out1:
        idp = plyta['id']
        plyta['brak_ceny'] = Przychod.objects.filter(plyta_id=idp, cena_j=0, inwentura=False).count()
        stan = plyta['stan']
        plyta['suma_wart'], plyta['test'] = calc_sum_stan(stan, Przychod.objects.filter(plyta_id=idp, inwentura=False))


    out2 = Plyta.objects.filter(magazyn='MAGAZYN2', rodzaj='dre').order_by('rodzaj','nazwa').annotate(
        brak_ceny=Value(0, output_field=DecimalField()),
        suma_wart=Value(zero, output_field=MoneyField(decimal_places=2, default_currency='PLN', max_digits=11)),
        test=Value('?', output_field=CharField(max_length=200))
    ).values('id','rodzaj', 'nazwa', 'opis', 'stan', 'brak_ceny', 'suma_wart', 'test')

    for plyta in out2:
        idp = plyta['id']
        plyta['brak_ceny'] = Przychod.objects.filter(plyta_id=idp, cena_j=0, inwentura=False).count()
        stan = plyta['stan']
        plyta['suma_wart'], plyta['test'] = calc_sum_stan(stan, Przychod.objects.filter(plyta_id=idp, inwentura=False))

    out3 = Plyta.objects.filter(magazyn='MAGAZYN3', rodzaj='dre').order_by('rodzaj', 'nazwa').annotate(
        brak_ceny=Value(0, output_field=DecimalField()),
        suma_wart=Value(zero, output_field=MoneyField(decimal_places=2, default_currency='PLN', max_digits=11)),
        test=Value('?', output_field=CharField(max_length=200))
    ).values('id', 'rodzaj', 'nazwa', 'opis', 'stan', 'brak_ceny', 'suma_wart', 'test')

    for plyta in out3:
        idp = plyta['id']
        plyta['brak_ceny'] = Przychod.objects.filter(plyta_id=idp, cena_j=0, inwentura=False).count()
        stan = plyta['stan']
        plyta['suma_wart'], plyta['test'] = calc_sum_stan(stan, Przychod.objects.filter(plyta_id=idp, inwentura=False))

    return out1, out2, out3


def gen_main_inwent_pdf_data(brok, gdata):
    zero = Money('0.00', PLN)
    out1 = Plyta.objects.filter(magazyn='MAGAZYN1', rodzaj='dre').order_by('rodzaj','nazwa').annotate(
        brak_ceny=Value(0, output_field=DecimalField()),
        i_stan=Value(0, output_field=DecimalField()),
        suma_wart=Value(zero, output_field=MoneyField(decimal_places=2, default_currency='PLN', max_digits=11)),
        test=Value('?', output_field=CharField(max_length=200))
    ).values('id','rodzaj', 'nazwa', 'opis', 'stan', 'i_stan', 'brak_ceny', 'suma_wart', 'test')

    for plyta in out1:
        idp = plyta['id']
        przychod = Przychod.objects.filter(plyta_id=idp, inwentura=False, data__lte=gdata).aggregate(Sum('ilosc'))['ilosc__sum']
        rozchod = Rozchod.objects.filter(plyta_id=idp, inwentura=False, data__lte=gdata).aggregate(Sum('ilosc'))['ilosc__sum']

        if przychod is None:
            przychod = 0

        if rozchod is None:
            rozchod = 0

        stan = przychod - rozchod
        # print("*", idp, plyta['nazwa'], przychod, rozchod, stan)
        plyta['i_stan'] = stan
        plyta['suma_wart'], plyta['test'] = calc_sum_stan(stan, Przychod.objects.filter(plyta_id=idp, inwentura=False, data__lte=gdata))


    out2 = Plyta.objects.filter(magazyn='MAGAZYN2', rodzaj='dre').order_by('rodzaj','nazwa').annotate(
        brak_ceny=Value(0, output_field=DecimalField()),
        suma_wart=Value(zero, output_field=MoneyField(decimal_places=2, default_currency='PLN', max_digits=11)),
        test=Value('?', output_field=CharField(max_length=200))
    ).values('id','rodzaj', 'nazwa', 'opis', 'stan', 'brak_ceny', 'suma_wart', 'test')

    for plyta in out2:
        idp = plyta['id']
        przychod = Przychod.objects.filter(plyta_id=idp, inwentura=False, data__lte=gdata).aggregate(Sum('ilosc'))['ilosc__sum']
        rozchod = Rozchod.objects.filter(plyta_id=idp, inwentura=False, data__lte=gdata).aggregate(Sum('ilosc'))['ilosc__sum']

        if przychod is None:
            przychod = 0

        if rozchod is None:
            rozchod = 0

        stan = przychod - rozchod
        # print("*", idp, plyta['nazwa'], przychod, rozchod, stan)
        plyta['i_stan'] = stan
        plyta['suma_wart'], plyta['test'] = calc_sum_stan(stan, Przychod.objects.filter(plyta_id=idp, inwentura=False, data__lte=gdata))

    out3 = ''

    return out1, out2, out3


def UpdateStat(rok_k):
    Statystyka.objects.all().delete()

    index_sde = Rozchod.objects.all().exclude(nr_sde=None).filter(rokk=rok_k, inwentura=False, plyta_id__rodzaj='dre').distinct('nr_sde') #, inwentura=True

    zero = Money('0.00', PLN)
    for ind in index_sde:
        km1 = zero
        km2 = zero
        km3 = zero
        km4 = zero
        km5 = zero
        km6 = zero
        km7 = zero
        km8 = zero
        km9 = zero
        km10 = zero
        km11 = zero
        km12 = zero
        row_sde = Rozchod.objects.filter(nr_sde=ind.nr_sde)
        for r in row_sde:
            r1 = Rozchod.objects.filter(data__month='01', pk=r.pk)
            for n in r1:
                km1 += n.kwota
            r2 = Rozchod.objects.filter(data__month='02', pk=r.pk)
            for n in r2:
                km2 += n.kwota
            r3 = Rozchod.objects.filter(data__month='03', pk=r.pk)
            for n in r3:
                km3 += n.kwota
            r4 = Rozchod.objects.filter(data__month='04', pk=r.pk)
            for n in r4:
                km4 += n.kwota
            r5 = Rozchod.objects.filter(data__month='05', pk=r.pk)
            for n in r5:
                km5 += n.kwota
            r6 = Rozchod.objects.filter(data__month='06', pk=r.pk)
            for n in r6:
                km6 += n.kwota
            r7 = Rozchod.objects.filter(data__month='07', pk=r.pk)
            for n in r7:
                km7 += n.kwota
            r8 = Rozchod.objects.filter(data__month='08', pk=r.pk)
            for n in r8:
                km8 += n.kwota
            r9 = Rozchod.objects.filter(data__month='09', pk=r.pk)
            for n in r9:
                km9 += n.kwota
            r10 = Rozchod.objects.filter(data__month='10', pk=r.pk)
            for n in r10:
                km10 += n.kwota
            r11 = Rozchod.objects.filter(data__month='11', pk=r.pk)
            for n in r11:
                km11 += n.kwota
            r12 = Rozchod.objects.filter(data__month='12', pk=r.pk)
            for n in r12:
                km12 += n.kwota

        suma = km1 + km2 + km3 + km4 + km5 + km6 + km7 + km8 + km9 + km10 + km11 + km12

        s = Statystyka(nr_sde=ind.nr_sde, mc1=km1, mc2=km2, mc3=km3, mc4=km4, mc5=km5, mc6=km6, mc7=km7, mc8=km8, mc9=km9, mc10=km10, mc11=km11, mc12=km12, suma=suma)
        s.save()


def gen_main_stat(rok_k):

    zero = Money('0.00', PLN)
    m1 = zero
    m2 = zero
    m3 = zero
    m4 = zero
    m5 = zero
    m6 = zero
    m7 = zero
    m8 = zero
    m9 = zero
    m10 = zero
    m11 = zero
    m12 = zero

    out = Statystyka.objects.all().order_by('nr_sde')
    for o in out:
        m1 += o.mc1
        m2 += o.mc2
        m3 += o.mc3
        m4 += o.mc4
        m5 += o.mc5
        m6 += o.mc6
        m7 += o.mc7
        m8 += o.mc8
        m9 += o.mc9
        m10 += o.mc10
        m11 += o.mc11
        m12 += o.mc12

    return out, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12