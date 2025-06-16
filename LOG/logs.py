from datetime import datetime

import numpy as np

from .models import LogSystem, ModulName, ErrorList
from SDA.settings import LOG_LOOP, LOG_FILE
from TaskAPI.models import FlagaZmiany
from next_prev import next_in_order
import os

def TestLogs():
    InitLog()


def logi_cron(i, s, czas, kto):

    modul_id = 9    # Identyfikator modułu
    shift = 7       # Adres od którego zaczynają się komunikaty dla tego modułu
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")
    komunikat_id = shift + int(i)

    komunikat = ErrorList.objects.get(id=komunikat_id)
    modul = ModulName.objects.get(id=modul_id)

    InsertLog(data, godz, modul, komunikat, s, czas, kto, 0)


def logi_order(i, s, czas, kto, stat):

    modul_id = 1     # Identyfikator modułu
    shift = 13       # Adres od którego zaczynają się komunikaty dla tego modułu
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")
    komunikat_id = shift + int(i)

    komunikat = ErrorList.objects.get(id=komunikat_id)
    modul = ModulName.objects.get(id=modul_id)

    InsertLog(data, godz, modul, komunikat, s, czas, kto, stat)


def LogiWORK(i, s, kto, stat):

    modul_id = 4 # Identyfikator modułu
    shift = 22 # Adres od którego zaczynają się komunikaty dla tego modułu
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")
    komunikat_id = shift + int(i)

    komunikat = ErrorList.objects.get(id=komunikat_id)
    modul = ModulName.objects.get(id=modul_id)

    InsertLog(data, godz, modul, komunikat, s, 0, kto, stat)


def Logi(i, s, kto):

    modul_id = 2 # Identyfikator modułu
    shift = 19 # Adres od którego zaczynają się komunikaty dla tego modułu
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")
    komunikat_id = shift + int(i)

    komunikat = ErrorList.objects.get(id=komunikat_id)
    modul = ModulName.objects.get(id=modul_id)

    InsertLog(data, godz, modul, komunikat, s, 0, kto, 0)


def Logi_r(i, s, kto):

    modul_id = 3 # Identyfikator modułu
    shift = 19 # Adres od którego zaczynają się komunikaty dla tego modułu
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")
    komunikat_id = shift + int(i)

    komunikat = ErrorList.objects.get(id=komunikat_id)
    modul = ModulName.objects.get(id=modul_id)

    InsertLog(data, godz, modul, komunikat, s, 0, kto, 0)


def InitLog():
    lenLoop = LOG_LOOP

    # test - przycinanie tablicy Log - za długa
    log = LogSystem.objects.all()
    if len(log) > lenLoop:
        d = len(log) - lenLoop
        logs = LogSystem.objects.all()[:d]
        for l in logs:
            LogSystem.objects.get(pk=l.id).delete()

    if len(log) < lenLoop:
        li = lenLoop - len(log)
        for i in range(0, li):
            d = LogSystem(opis='', kto='', status='', status_id=-1)
            d.save()

    flg = FlagaZmiany.objects.get(id=1)
    flg.loop_count = int(LogSystem.objects.all().values_list('id').first()[0])
    flg.save()


def InsertLog(data, godz, modul, komunikat, opis, czas, kto, stat):
    if LogSystem.objects.all().count() == 0: # Przy resecie tabeli wywołuje się ta procedura
        InitLog()

    fz = FlagaZmiany.objects.get(id=1).loop_count
    row = LogSystem.objects.get(id=fz)
    row = next_in_order(row, loop=True)
    row.data = data
    row.godz = godz
    row.komunikat_id = komunikat.id
    row.modul_id = modul.id
    row.opis = opis
    row.czas = czas
    row.kto  = kto
    row.status = komunikat.status
    if stat == 0:
        row.status_id = komunikat.status_id
    else:
        row.status_id = stat

    row.nowy = True
    row.save()

    flg = FlagaZmiany.objects.get(id=1)
    flg.loop_count = int(row.id)
    flg.save()



def LogToFile():
    path = LOG_FILE
    tab = LogSystem.objects.filter(nowy=True).order_by('data', 'godz')

    headers = ['Kto', 'Data', 'Godz', 'Moduł', 'Status', 'Komunikat', 'Opis']
    max_lengths = [len(header) for header in headers]

    all_logs = {}
    problem_logs = []

    for t in tab:
        log_entry = [str(t.kto), str(t.data), str(t.godz), str(t.modul), str(t.status), str(t.komunikat), str(t.opis)]

        # Update max_lengths for pretty printing
        for i, entry in enumerate(log_entry):
            max_lengths[i] = max(max_lengths[i], len(entry))

        date_str = str(t.data)
        module_str = str(t.modul)

        # Initialize dictionary for date if not present
        if date_str not in all_logs:
            all_logs[date_str] = {}

        # Initialize list for module if not present under the specific date
        if module_str not in all_logs[date_str]:
            all_logs[date_str][module_str] = []

        all_logs[date_str][module_str].append(log_entry)

        if t.status_id != 1:
            problem_logs.append((date_str, log_entry))

        r = LogSystem.objects.get(pk=t.id)
        r.nowy = False
        r.save()

    def write_logs(log_entries, filename):
        existing_entries = set()
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    existing_entries.add(line.strip())

        with open(filename, 'a+') as f:
            if not existing_entries:  # Plik jest nowy
                f.write(header_line + '\n')
                f.write(separator_line + '\n')

            for entry in log_entries:
                log_line = ' | '.join([entry[i].ljust(max_lengths[i]) for i in range(len(entry))])
                if log_line.strip() not in existing_entries:
                    f.write(log_line + '\n')
                    existing_entries.add(log_line.strip())

    header_line = ' | '.join([headers[i].ljust(max_lengths[i]) for i in range(len(headers))])
    max_entry_length = sum(max_lengths) + (3 * (len(max_lengths) - 1))
    separator_line = '-' * max_entry_length

    for date_str, modules in all_logs.items():
        date_path = os.path.join(path, date_str)
        if not os.path.exists(date_path):
            os.makedirs(date_path)

        for module_str, log_entries in modules.items():
            log_filename = os.path.join(date_path, f'{date_str} {module_str}.log')
            unique_logs = list(dict.fromkeys(map(tuple, log_entries)))
            write_logs(unique_logs, log_filename)

    for date_str, log_entry in problem_logs:
        problem_log_path = os.path.join(path, date_str, 'problemy.log')
        unique_problem_logs = list(
            dict.fromkeys(map(tuple, [entry[1] for entry in problem_logs if entry[0] == date_str])))
        write_logs(unique_problem_logs, problem_log_path)






























#def LogToFile():
#    path = LOG_FILE
#    tab = LogSystem.objects.filter(nowy=True).order_by('data', 'godz')

#    headers = ['Kto', 'Data', 'Godz', 'Moduł', 'Status', 'Komunikat', 'Opis']
#    max_lengths = [len(header) for header in headers]

#    all_logs = []
#    problem_logs = []

#    for t in tab:
#        log_entry = [str(t.kto), str(t.data), str(t.godz), str(t.modul), str(t.status), str(t.komunikat), str(t.opis)]

#        # Update max_lengths for pretty printing
#        for i, entry in enumerate(log_entry):
#            max_lengths[i] = max(max_lengths[i], len(entry))

#        all_logs.append(log_entry)
#        if t.status_id != 1:
#            problem_logs.append(log_entry)

#        r = LogSystem.objects.get(pk=t.id)
#        r.nowy = False
#        r.save()

#    header_line = ' | '.join([headers[i].ljust(max_lengths[i]) for i in range(len(headers))])
#    max_entry_length = sum(max_lengths) + (3 * (len(max_lengths) - 1))
#    separator_line = '-' * max_entry_length

#    def write_logs(log_entries, filename):
#        existing_entries = set()
#        if os.path.exists(filename):
#            with open(filename, 'r') as f:
#                for line in f:
#                    existing_entries.add(line.strip())

#        with open(filename, 'a+') as f:
#            if not existing_entries:  # Plik jest nowy
#                f.write(header_line + '\n')
#                f.write(separator_line + '\n')

#            for entry in log_entries:
#                log_line = ' | '.join([entry[i].ljust(max_lengths[i]) for i in range(len(entry))])
#                if log_line.strip() not in existing_entries:
#                    f.write(log_line + '\n')
#                    existing_entries.add(log_line.strip())

#    unique_all_logs = list(dict.fromkeys(map(tuple, all_logs)))
#    unique_problem_logs = list(dict.fromkeys(map(tuple, problem_logs)))

#    for t in tab:
#        p = os.path.join(path, str(t.data))
#        if not os.path.exists(p):
#            os.makedirs(p)

#        name_f = os.path.join(p, f'{t.data} {t.modul}.log')
#        write_logs(unique_all_logs, name_f)

#        if problem_logs:
#            problem_log = os.path.join(p, 'problems.log')
#            write_logs(unique_problem_logs, problem_log)

