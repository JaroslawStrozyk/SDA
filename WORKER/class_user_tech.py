from datetime import datetime, timedelta
from django.conf import settings
from TaskAPI.models import Rok, URok
from django.contrib.auth.models import Group


class UserTech:
    def name_log(self, request):
        name_log = request.user.first_name + " " + request.user.last_name
        return name_log

    def inicjaly(self, request):
        name_log = request.user.first_name + " " + request.user.last_name
        inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
        return inicjaly

    def about(self):
        return settings.INFO_PROGRAM

    def test_rok(self, request):
        tst = Rok.objects.all().order_by('rok')
        lata = []
        for t in tst:
            lata.append(t.rok)
        name_log = request.user.first_name + " " + request.user.last_name
        inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'

        brok = datetime.now().strftime("%Y")
        bmc = datetime.now().strftime("%m")

        try:
            rok = URok.objects.get(nazwa=inicjaly).rok
        except:
            p = URok(nazwa=inicjaly, rok=int(brok))
            p.save()
            rok = int(brok)

        return lata, rok, brok, bmc

    def biezacy_miesiac(self):
        return datetime.now().strftime("%m")

    def tst_admin(self, request):
        gr = ''
        admini = False
        query_set = Group.objects.filter(user=request.user)
        for g in query_set:
            gr = g.name
        if gr == 'administrator' or gr == 'ksiegowosc':
            admini = True
        return admini

    def tst_osoba(self, request):
        name_log = request.user.first_name + " " + request.user.last_name
        inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
        return name_log, inicjaly