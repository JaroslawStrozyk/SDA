from django.contrib.auth.models import Group
from TaskAPI.models import Rok, URok, Waluta
from django.conf import settings
from moneyed import Money, PLN
import datetime




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
    brok = datetime.datetime.now().strftime("%Y")
    bmc = datetime.datetime.now().strftime("%m")
    return lata, rok, brok, bmc
