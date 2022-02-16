from django.contrib.auth.models import Group
from TaskAPI.models import Rok, URok, Waluta
from django.conf import settings
from moneyed import Money, PLN

from datetime import datetime, timedelta




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
    rok = URok.objects.get(nazwa=inicjaly).rok
    brok = datetime.now().strftime("%Y")
    bmc = datetime.now().strftime("%m")
    return lata, rok, brok, bmc


#
# Tylko dla dodawania i edycji
#
def prac_staz(st, dat_zat):
    roz = 0
    if st == 0:
        if dat_zat != "":
            d_zat = datetime.strptime(dat_zat, '%d.%m.%Y')
            t = datetime.today()
            if d_zat != None:
                roz = round((t - d_zat) / timedelta(days=365))
    else:
        roz = st
    return roz


def konw_mc(bmc):
    str = ""

    if bmc == '01':
        str += "Styczeń"
    elif bmc == '02':
        str += "Luty"
    elif bmc == '03':
        str += "Marzec"
    elif bmc == '04':
        str += "Kwiecień"
    elif bmc == '05':
        str += "Maj"
    elif bmc == '06':
        str += "Czerwiec"
    elif bmc == '07':
        str += "Lipiec"
    elif bmc == '08':
        str += "Sierpień"
    elif bmc == '09':
        str += "Wrzesień"
    elif bmc == '10':
        str += "Październik"
    elif bmc == '11':
        str += "Listopad"
    elif bmc == '12':
        str += "Grudzień"

    return str
