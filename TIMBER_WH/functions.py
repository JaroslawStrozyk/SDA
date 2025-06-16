from moneyed import Money, PLN
from django.contrib.auth.models import Group
from ORDERS.models import NrSDE
from .calc_data import rozlicz_rozchod
from .models import Plyta, Przychod, Rozchod, Zwrot
import re

def CalcIDProd():
    prod = Plyta.objects.all().order_by('id')
    lp = 0
    for p in prod:
        lp += 1
        p.prod_id = lp
        p.save()
    przy = Przychod.objects.all().order_by('id')
    lp = 0
    for p in przy:
        lp += 1
        d_i = "P."+str(p.plyta.id)+"."+str(lp)
        p.doc_id = d_i
        p.save()

    roz = Rozchod.objects.all().order_by('id')
    lp = 0
    for r in roz:
        lp += 1
        d_i = "R."+str(r.plyta.id)+"."+str(lp)
        r.doc_id = d_i
        r.save()
    zwrot = Zwrot.objects.all().order_by('id')
    lp = 0
    for z in zwrot:
        lp += 1
        d_i = "Z."+str(z.plyta.id)+"."+str(lp)
        z.doc_id = d_i
        z.save()


def Cal_All_States():
    for p in Plyta.objects.all():
        Cal_States_r(p.id,'')


def Cal_All_Poz():
    for plyta in Plyta.objects.filter(magazyn='MAGAZYN1', rodzaj='dre'):
        rozlicz_rozchod(plyta)
    for plyta in Plyta.objects.filter(magazyn='MAGAZYN2', rodzaj='dre'):
        rozlicz_rozchod(plyta)
    for plyta in Plyta.objects.filter(magazyn='MAGAZYN3', rodzaj='dre'):
        rozlicz_rozchod(plyta)



def Cal_States_r(pk, sde):
    plyta = Plyta.objects.get(pk=pk)
    rozlicz_rozchod(plyta)

    upgrade_mag_sde(sde)




# def Cal_States_r(pk, sde):
#     plyta = Plyta.objects.get(pk=pk)
#     przychod = Przychod.objects.filter(plyta=pk, inwentura=False).order_by('-id')[:10]
#
#     zero = Money('0.00', 'PLN')
#
#     #
#     # Srednia z cen plyt
#     #
#     # zero = Money('0.00', 'PLN')
#     # avr  = zero
#     # count = 0
#     # for p in przychod:
#     #     cena = p.cena_j
#     #     if cena != zero:
#     #         count += 1
#     #         avr += cena
#     #
#     # if count > 0:
#     #     avr = avr/count
#     #
#     # plyta.cena = avr
#     # plyta.save()
#
#     #
#     # Zamiast średniej dodajemy ostatnią cenę płyt
#     #
#     try:
#         cen = przychod.first().cena_j
#     except:
#         cen = zero
#     plyta.cena = cen
#     plyta.save()
#
#
#     plyta = Plyta.objects.get(pk=pk)
#     przychod = Przychod.objects.filter(plyta=pk, inwentura=False)
#     rozchod = Rozchod.objects.filter(plyta=pk, inwentura=False)
#
#     cena_jedn = plyta.cena
#
#     przychod_ilosc = 0
#     p_jm = 'm²'
#     for p in przychod:
#         p.cena = p.ilosc * p.cena_j
#         przychod_ilosc += p.ilosc
#         p_jm = p.jm
#         p.save()
#
#     rozchod_ilosc = 0
#     for r in rozchod:
#         r.kwota = r.ilosc * cena_jedn
#         rozchod_ilosc += r.ilosc
#         r.save()
#
#     calc = przychod_ilosc - rozchod_ilosc
#     #print(">>>", calc)
#
#     plyta.jm = p_jm
#     plyta.stan = calc
#     plyta.save()
#
#     upgrade_mag_sde(sde)


def upgrade_mag_sde(sde):
    if sde != '':
        out_d = Money('0.00', PLN)
        out_w = Money('0.00', PLN)
        try:
            NSDE = NrSDE.objects.get(pk=sde)

            rozchod = Rozchod.objects.filter(nr_sde=sde)
            for r in rozchod:
                rodzaj = r.plyta.rodzaj
                print("rodzaj:", rodzaj, type(rodzaj))
                if rodzaj == 'dre':
                    out_d += r.kwota
                else:
                    out_w += r.kwota

            NSDE.magazyn_dre = out_d
            NSDE.magazyn_wewn = out_w
            NSDE.save()
        except:
            #print("Błąd: Timber_WH-functions-l116 !!!")
            pass


def upgrade_mag_sde_all(rok):
    try:
        NSDE = NrSDE.objects.filter(rok=rok)

        for rsde in NSDE:
            rid = rsde.id
            # print("SDE:", rid, rsde.nazwa)
            rozchod = Rozchod.objects.filter(nr_sde=rid)
            out_d = Money('0.00', PLN)
            out_w = Money('0.00', PLN)
            for r in rozchod:
                rodzaj = r.plyta.rodzaj
                # print(">>> RP:", rodzaj, r.kwota)
                if rodzaj == 'dre':
                    out_d += r.kwota
                else:
                    out_w += r.kwota
            # print("=== SUMA: dre",out_d, " wew", out_w)

            rsde.magazyn_dre = out_d
            rsde.magazyn_wewn = out_w
            rsde.save()
    except:
        #print("Błąd: Timber_WH-functions-l116 !!!")
        pass


def check_gr(request, mag1, mag2, mag3, mag4, mag5):
    fmag = False

    gr = ''
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        gr = g.name

    if gr=='magazyn':
        if mag1 == True:
            fmag = True
        elif mag2 == True:
            fmag = True
        elif mag3 == True:
            fmag = True
        elif mag4 == True:
            fmag = True
        elif mag5 == True:
            fmag = True

    elif gr=='magazyn1':
        if mag1 == True:
            fmag = True
        elif mag2 == True:
            fmag = False
        elif mag3 == True:
            fmag = False


    elif gr=='magazyn2':
        if mag1 == True:
            fmag = False
        elif mag2 == True:
            fmag = True
        elif mag3 == True:
            fmag = False
    else:
        fmag = True

    return fmag


def check_group(request,mag):
    fmag = False

    gr = ''
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        gr = g.name

    if gr=='magazyn':
        if mag == 'mag1':
            fmag = True
        elif mag == 'mag2':
            fmag = True
        elif mag == 'mag3':
            fmag = True
        elif mag == 'mag4':
            fmag = True
        elif mag == 'mag5':
            fmag = True


    elif gr=='magazyn1':
        if mag == 'mag1':
            fmag = True
        elif mag == 'mag2':
            fmag = False
        elif mag == 'mag3':
            fmag = False
        elif mag == 'mag4':
            fmag = False


    elif gr=='magazyn2':
        if mag == 'mag1':
            fmag = False
        elif mag == 'mag2':
            fmag = True
        elif mag == 'mag3':
            fmag = False
        elif mag == 'mag4':
            fmag = False
    else:
        fmag = True

    return fmag


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


def test_osoba(request, mag, fl):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'


    grupa = ''
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        grupa = g.name

    # Ustawiwnie uprawnień tylko do odczytu
    rw = True
    if inicjaly == 'L.Z.' or inicjaly == 'M.G.' or grupa == 'produkcja' or grupa == 'kierownik':
        rw = False

    if grupa == 'magazyn2a' and mag == 'mag1':
        rw = False

    if grupa == 'magazyn2' and mag == 'mag1':
        rw = False

    if grupa == 'magazyn' and mag == 'mag1':
        rw = False

    # Widok przycisku statystyki
    fls = False
    if fl == 'dre' and rw == True:
        fls = True

    if inicjaly == 'K.G.':
        fls = True

    return name_log, inicjaly, grupa, rw, fls


def format_european_currency_pln(value):
    # Konwersja na string, jeśli wartość jest typu Money
    if not isinstance(value, str):
        value = str(value)

    # Usuwanie znaku waluty, zakładając, że jest na końcu
    match = re.match(r"([\d,\.]+)\s*zł", value)
    if not match:
        raise ValueError("Nieprawidłowy format wartości walutowej.")

    numeric_part = match.group(1)

    # Zamiana separatorów: najpierw zamiana przecinków na tymczasowy znak, aby nie stracić danych
    numeric_part = numeric_part.replace(',', 'TEMP').replace('.', ',').replace('TEMP', ' ')

    # Dodanie znaku waluty
    formatted_value = numeric_part + " zł"
    return formatted_value
