from TaskAPI.models import Rok, URok, Waluta
from datetime import datetime, timedelta
import tabula
from moneyed import Money, PLN

#from .calculate import licz_dni
from .models import Podsumowanie, Pensja
from django.contrib.auth.models import Group







# def test_admin(request):
#     gr = ''
#     admini = False
#     query_set = Group.objects.filter(user=request.user)
#     for g in query_set:
#         gr = g.name
#     if gr == 'administrator' or gr == 'ksiegowosc':
#         admini = True
#     return admini


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
    return name_log, inicjaly


def test_rok(request):
    tst = Rok.objects.all().order_by('rok')
    lata = []
    for t in tst:
        lata.append(t.rok)
    name_log, inicjaly = test_osoba(request)

    brok = datetime.now().strftime("%Y")
    bmc = datetime.now().strftime("%m")

    try:
        rok = URok.objects.get(nazwa=inicjaly).rok
    except:
        p = URok(nazwa=inicjaly, rok=int(brok))
        p.save()
        rok = int(brok)

    return lata, rok, brok, bmc


#
# Konwersja miesiecy z liczb na opis
#
def konw_mc(bmc):
    str = ""

    if bmc == '01' or bmc=='1' or bmc == 1:
        str += "Styczeń"
    elif bmc == '02' or bmc=='2' or bmc == 2:
        str += "Luty"
    elif bmc == '03' or bmc =='3' or bmc == 3:
        str += "Marzec"
    elif bmc == '04' or bmc =='4' or bmc == 4:
        str += "Kwiecień"
    elif bmc == '05' or bmc =='5' or bmc == 5:
        str += "Maj"
    elif bmc == '06' or bmc =='6' or bmc == 6:
        str += "Czerwiec"
    elif bmc == '07' or bmc =='7' or bmc == 7:
        str += "Lipiec"
    elif bmc == '08' or bmc =='8' or bmc == 8:
        str += "Sierpień"
    elif bmc == '09' or bmc =='9' or bmc == 9:
        str += "Wrzesień"
    elif bmc == '10' or bmc ==10:
        str += "Październik"
    elif bmc == '11' or bmc ==11:
        str += "Listopad"
    elif bmc == '12' or bmc ==12:
        str += "Grudzień"

    return str


#
# Upload file
#
def FileToDB(file_n, file_r):

    tab_data = []
    data = ''
    err = ''

    table = tabula.read_pdf(file_n, pages=1, guess=False, pandas_options={'header': None})
    tab = table[0].values.tolist()

    for r in tab:
        st = str(r[0])
        if st.find("Lista płac skrócona") != -1:
           data = r[0].split(" ")[-1]

    if data != '':
        tdata = data.split(".")
        mc  = tdata[1]
        rok = tdata[2]

        table = tabula.read_pdf(file_r, pages=1)
        tab = table[0].values.tolist()

        f = 0
        for t in tab:

            if f == 0:
                f += 1
            else:
                d = [rok, mc, t[1].split(" ")[0], t[1].split(" ")[1], t[8]]
                tab_data.append(d)
    else:
        err = 'Problem z konwersją.'

    return err, tab_data


def KonwertMC(bmc):
    str = ""

    bmc = bmc.upper()
    bmc = bmc.strip()
    bmc = bmc.strip("*")


    if bmc == 'STYCZEŃ':
        str += "01"
    elif bmc == 'LUTY':
        str += "02"
    elif bmc == 'MARZEC':
        str += "03"
    elif bmc == 'KWIECIEŃ':
        str += "04"
    elif bmc == 'MAJ':
        str += "05"
    elif bmc == 'CZERWIEC':
        str += "06"
    elif bmc == 'LIPIEC':
        str += "07"
    elif bmc == 'SIERPIEŃ':
        str += "08"
    elif bmc == 'WRZESIEŃ':
        str += "09"
    elif bmc == 'PAŹDZIERNIK':
        str += "10"
    elif bmc == 'LISTOPAD':
        str += "11"
    elif bmc == 'GRUDZIEŃ':
        str += "12"

    return str


def NFileToDB(file_n):

    tab_data = []
    err = ''

    try:

        table = tabula.read_pdf(file_n, pages="all", pandas_options={'header': None})
        for i in range(0, len(table)):
            tab = table[i].values.tolist()
            for t in tab:
                if isinstance(t[0], str):
                    if t[0]!='Lp.':
                        kd = t[2].split(" ")
                        # print("=>>", t, type(t))
                        # print("==>", kd, type(kd))
                        # km = kd[0]
                        # print(">>> ", km, type(km))
                        mc = KonwertMC(kd[0])
                        rk = kd[1]
                        naz = t[1].split(" ")[0]
                        prz = t[4]
                        b_b = t[5]
                        d = [rk, mc, naz, prz, b_b]
                        tab_data.append(d)
    except:
        err = 'Problem z konwersją.'

    return err, tab_data


#
# Konwersja przecinków na spacje przy tysiącach
#
def testQuery(query):
    query = str(query)
    if query.find(",") > -1:
        try:
            q = query.replace(",", ".")
            t = q.split(" ")
            if len(t) > 1:
                q = t[0] + t[1]
            else:
                q = t[0]
            query = q
        except:
            pass
    return query


#
# Przepisanie sumy do tabeli podsumowań
#
def DoPodsumowanie(rok, mc, suma):

    try:
        pod = Podsumowanie.objects.get(miesiac=mc, rok=rok)
        pod.suma_biuro = suma
        pod.save()
    except:
        po = Podsumowanie(miesiac=mc, rok=rok, suma_biuro=suma)
        po.save()


#
# Test miesiąca dla edycji miesiąca beżącego i archiwalnego
#
def testMiesiac(pk, bmc):
    p = Pensja.objects.get(pk=pk)
    tst = p.miesiac

    if tst < 10:
        m_c = '0'+str(tst)
    else:
        m_c = str(tst)

    if m_c == bmc:
        return True, m_c
    else:
        return False, m_c



# def prac_stawka_wyj(pensja):
#     pens = Money(str(pensja), PLN)
#     pens = (pens/168) * 8
#     return pens







