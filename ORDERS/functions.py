from django.contrib.auth.models import Group

from ORDERS.models import NrMPK
from TaskAPI.models import Rok, URok, Waluta
from django.conf import settings
from moneyed import Money, PLN
import datetime

# Function to parse each value in the file
def custom_parser(val):
    val = val.strip()
    if val in ['True', 'False']:
        return val == 'True'  # Convert to boolean
    try:
        return int(val)  # Convert to integer
    except ValueError:
        return val.strip("'")  # Remove single quotes for strings
def SetNewYear():
    tst = NrMPK.objects.filter(rok=2024).count()
    if tst == 0:
        file_path = 'MPK_2024A.csv'
        data = []
        with open(file_path, 'r') as file:
            # Skipping the first line (header)
            next(file)
            for i, line in enumerate(file):
                parsed_line = [custom_parser(val) for val in line.split(';')]
                data.append(parsed_line)

        for d in data:
            nazwa = d[0].strip().strip('"')
            opis = d[2].strip().strip('"')
            rok = d[3]
            lsde = d[4]

            mpk = NrMPK(nazwa=nazwa, opis=opis, rok=rok, lsde=lsde)
            mpk.save()
        print("Operacja wykonana prawidłowo.")
    else:
        print("Operacja odrzucona bo 2024 już istnieje !!!")


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

    if inicjaly == 'J.S.' or inicjaly == 'M.O.' or inicjaly == 'J.M.':
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
    zero = Money('00.00', 'PLN')
    suma_c = zero
    fsc = False
    tab = settings.CURRENCIES
    for t in tab:
        DICT[t] = Money('00.00', t)

    for zam in zamowienia:
        c = zam.kwota_netto.currency
        d = zam.kwota_netto.amount
        suma_c += Money(zam.kwota_netto_pl.amount, zam.kwota_netto_pl.currency)
        DICT[str(c)] = Money(d, c) + DICT[str(c)]
    #print(DICT)
    if suma_c > zero:
        suma_c += DICT['PLN']
        fsc = True


    suma = ''
    for i in DICT.items():
        tst = Money('00.00', i[1].currency)
        if i[1] != tst:
            suma += str(i[1].currency) + ': ' + str(i[1].amount) + ' / '
    suma = suma[:-3]
    DICT.clear()
    if len(suma)==0:
        suma = str(zero)
    return suma, suma_c, fsc


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

#
#  Kontrola danych
#  0-zielone; 1-czerwone; 10-białe;
#
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
    if (tsde == '') and (tmpk == ''):
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
