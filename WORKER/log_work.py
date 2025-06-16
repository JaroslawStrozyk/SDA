from concurrent.futures import ThreadPoolExecutor
import datetime

from LOG.logs import InsertLog
from LOG.models import ModulName, ErrorList
from COMP_REPO.functions import test_osoba


class WorkerLog:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)

    def start(self, request, info):
        self.log_action(request, info)


    def start_det(self, request, info):
        self.log_action(request, info)

    def add_edit(self, request, log_info):
        self.log_action(request, log_info)

    def log_action(self, request, action):
        # Funkcja do wykonania w tle
        def log_to_db():
            name_log, inicjaly, grupa = test_osoba(request)
            data = datetime.datetime.now().strftime('%Y-%m-%d')
            godz = datetime.datetime.now().strftime('%H:%M:%S')

            komunikat = ErrorList.objects.get(id=24)
            modul = ModulName.objects.get(id=6)

            InsertLog(data, godz, modul, komunikat, action, 0, inicjaly, 0)

        self.executor.submit(log_to_db)

