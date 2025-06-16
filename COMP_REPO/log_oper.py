from concurrent.futures import ThreadPoolExecutor
import datetime

from LOG.logs import InsertLog
from LOG.models import ModulName, ErrorList
from .functions import test_osoba

class CompRepoLog:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)

    def start(self, request, query):
        if query != '':
            self.log_action(request, 'OKNO GŁÓWNE - szukanie: ' + query)
        else:
            self.log_action(request, 'OKNO GŁÓWNE - przegląd')

    def zapis_stawka(self, request, info):
        self.log_action(request, info)

    def zakonczenie(self, request, log_info):
        self.log_action(request, log_info)

    def zapis_blokada(self, request, stat):
        if stat:
            log_info = "EDYCJA ZABLOKOWANA."
        else:
            log_info = "EDYCJA ODBLOKOWANA."
        self.log_action(request, log_info)

    def start_detail(self, request, info):
        self.log_action(request, info)

    def add_edit(self, request, sw, s):
        if sw:
            info = "ZAPIS NOWEJ POZYCJI:   Magazyn: " + s.magazyn + ", SDE: " + s.nr_sde.nazwa + ", Nazwa towaru: " + s.przech_nazwa + ", Zwolnione: " + str(s.zwolnione) + ", Od: " + str(s.czas_od) + ", Do: " + str(s.czas_do) + ", Stawka: " + str(s.stawka)
        else:
            info = "ZAPIS EDYCJI:   Magazyn: " + s.magazyn + ", SDE: " + s.nr_sde.nazwa + ", Nazwa towaru: " + s.przech_nazwa + ", Zwolnione: " + str(s.zwolnione) + ", Od: " + str(s.czas_od) + ", Do: " + str(s.czas_do) + ", Stawka: " + str(s.stawka)
        self.log_action(request, info)

    def log_action(self, request, action):
        # Funkcja do wykonania w tle
        def log_to_db():
            name_log, inicjaly, grupa = test_osoba(request)
            data = datetime.datetime.now().strftime('%Y-%m-%d')
            godz = datetime.datetime.now().strftime('%H:%M:%S')

            komunikat = ErrorList.objects.get(id=24)
            modul = ModulName.objects.get(id=5)

            InsertLog(data, godz, modul, komunikat, action, 0, inicjaly, 0)

        # Wywołanie funkcji w tle
        self.executor.submit(log_to_db)

