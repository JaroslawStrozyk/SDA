from django.contrib.auth.models import Group
from TaskAPI.models import Rok, URok, Waluta
from django.conf import settings
from moneyed import Money, PLN
import datetime





def test_admin(request):
    gr = ''
    admini = False
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        gr = g.name
        # grupy: 	administrator, ksiegowosc, zksiegowosc, spedycja, biuro
    if gr == 'administrator':
        admini = True
    return admini


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
    return name_log, inicjaly


def test_osoba1(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'

    if inicjaly == 'J.S.' or inicjaly == 'M.O.':
        rozliczenie = 1
    else:
        rozliczenie = 0
    return name_log, inicjaly, rozliczenie


def test_rok(request):
    tst = Rok.objects.all().order_by('rok')
    lata = []
    for t in tst:
        lata.append(t.rok)
    name_log, inicjaly = test_osoba(request)
    rok = URok.objects.get(nazwa=inicjaly).rok
    brok = datetime.datetime.now().strftime("%Y")
    return lata, rok, brok


def testQuery(query):
    query = str(query)
    if query.find(",") > -1:
        try:
            q = query.replace(",", ".")
            float(q)
            query = q
        except:
            pass
    return query


def suma_wartosci(zamowienia):
    DICT = {}
    tab = settings.CURRENCIES
    for t in tab:
        DICT[t] = Money('00.00', t)

    for zam in zamowienia:
        # if zam.nr_fv != '': #nr_fv
        #     c = zam.kwota_netto.currency
        #     d = zam.kwota_netto.amount
        #     DICT[str(c)] = Money(d, c) + DICT[str(c)]
        c = zam.kwota_netto.currency
        d = zam.kwota_netto.amount
        DICT[str(c)] = Money(d, c) + DICT[str(c)]
    # print(DICT)

    suma = ''
    for i in DICT.items():
        tst = Money('00.00', i[1].currency)
        if i[1] != tst:
            suma += str(i[1].currency) + ': ' + str(i[1].amount) + ' / '
    suma = suma[:-3]
    DICT.clear()
    return suma


def CalcCurrency(kwota, dataf):
    wartosc = Money('00.00', PLN)
    kurs = Money('00.00', PLN)
    data = ''

    if str(kwota.currency) != 'PLN' and str(dataf) != "":

        tab = Waluta.objects.filter(kod=kwota.currency).order_by('-data')
        tst = datetime.datetime.strptime(str(dataf), "%d.%m.%Y").strftime("%Y-%m-%d")

        poz = ''

        f = False
        ex = False
        for pt in tab:
            if f == True:
                poz = pt
                f = False
                ex = True

            if pt.data == tst:
                f = True

        if ex == False:
            ind = Waluta.objects.filter(kod=kwota.currency).order_by('-id').values('id')[0]['id']
            poz = Waluta.objects.get(id=(ind))

        wartosc = Money(str(kwota.amount * poz.kurs.amount), PLN)
        kurs = poz.kurs
        data = poz.data

    return data, wartosc, kurs


def TestValidate(wartosc_zam, kwota_netto, tsde, tmpk, data_fv, roz): #, nr_dok3
    kontrola = -1

    # kontrola wartości
    if wartosc_zam == kwota_netto:
        kontrola = 0
    if wartosc_zam > kwota_netto:
        kontrola = 1
    if wartosc_zam < kwota_netto:
        kontrola = -1
    if (wartosc_zam == kwota_netto) and (wartosc_zam.amount == Money('00.00', PLN).amount):
        kontrola = 2

    # kontrola faktury
    if data_fv == '': # or nr_dok3 == '':  # None:
        kontrola = 1

    # Kontrola celu
    ts = False
    if tsde != '':
        ts = True
    tm = False
    if tmpk != '':
        tm = True
    if (ts ^ tm) == False:  # XOR
        kontrola = 1

    # Patrycja, Michał
    if roz == True:
        kontrola = 10
    return kontrola



# Funkcje DecodeSlash i CodeSlash bardzo ważne, strona zwraca błąd jak w parametrze jest znak '/'
def DecodeSlash(st):
    st = list(st)
    for i in range(0,len(st)):
        if st[i] == "|":
            st[i] = "/"
    return "".join(st)


def CodeSlash(st):
    st = list(st)
    for i in range(0,len(st)):
        if st[i] == "/":
            st[i] = "|"
    return "".join(st)
