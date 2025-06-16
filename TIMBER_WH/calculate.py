from .models import Plyta, Przychod, Rozchod, StanObecny
from moneyed import Money, PLN



def CalcAll():
    pl = Plyta.objects.get(pk=22)
    pr = Przychod.objects.filter(plyta=pl,  inwentura=False).order_by('data')
    ro = Rozchod.objects.filter(plyta=pl,  inwentura=False).order_by('data')


    print("***")
    print("=> PL:", pl)

    print("+")
    for p in pr:
        print("|=> PR:", p.data, p.zrodlo)

    print("+")
    for r in ro:
        print("|=> RO:", r.data, r.cel)


def calc_sum_stan(stan, przychod):
    mzero = Money('0.00', PLN)
    out = mzero
    d = dict()
    tt = ''

    if stan <= 0:
        out = mzero
    else:
        #d = dict()
        for p in przychod:
            pp = p.cena_j.amount
            il = p.ilosc
            if pp not in d:
                d[pp] = il
            else:
                d[pp] = d[pp] + il

        try:
            cena_jp = list(d)[-1]
            ilosc_p = d[cena_jp]

            if stan <= ilosc_p:
                out = stan * Money(str(cena_jp), PLN)
            elif stan > ilosc_p:
                stan1 = stan - ilosc_p
                out = ilosc_p * Money(str(cena_jp), PLN)

                cena_jp = list(d)[-2]
                ilosc_p = d[cena_jp]

                out += stan1 * Money(str(cena_jp), PLN)
                # Sprawdzić na wielu przypadkach
        except:
            out = mzero

        tt="["
        for key, value in d.items():
            tt += str(key) + " zł: "+str(value) + "]["
        if len(tt) > 1:
            tt = tt[0:-2]
        tt +="]"

    return out, tt