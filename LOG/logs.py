from datetime import datetime
from .models import Log, ModulName, ErrorList
from SDA.settings import LOG_LOOP, LOG_FILE
from TaskAPI.models import FlagaZmiany
from next_prev import next_in_order
import os

def TestLogs():
    InitLog()


def LogiCron(i, s, kto):

    modul_id = 9 # Identyfikator modułu
    shift = 7 # Adres od którego zaczynają się komunikaty dla tego modułu
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")
    komunikat_id = shift + int(i)

    komunikat = ErrorList.objects.get(id=komunikat_id)
    modul = ModulName.objects.get(id=modul_id)

    InsertLog(data, godz, modul, komunikat, s, kto)

    # logi = Log(data=data, godz=godz, modul=modul, komunikat=komunikat, opis=s, kto=kto, status=komunikat.status, status_id=komunikat.status_id)
    # logi.save()


def LogiORD(i, s, kto):

    modul_id = 1 # Identyfikator modułu
    shift = 13 # Adres od którego zaczynają się komunikaty dla tego modułu
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")
    komunikat_id = shift + int(i)

    komunikat = ErrorList.objects.get(id=komunikat_id)
    modul = ModulName.objects.get(id=modul_id)

    InsertLog(data, godz, modul, komunikat, s, kto)


def Logi(i, s, kto):

    modul_id = 2 # Identyfikator modułu
    shift = 19 # Adres od którego zaczynają się komunikaty dla tego modułu
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")
    komunikat_id = shift + int(i)

    komunikat = ErrorList.objects.get(id=komunikat_id)
    modul = ModulName.objects.get(id=modul_id)

    InsertLog(data, godz, modul, komunikat, s, kto)


def Logi_r(i, s, kto):

    modul_id = 3 # Identyfikator modułu
    shift = 19 # Adres od którego zaczynają się komunikaty dla tego modułu
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")
    komunikat_id = shift + int(i)

    komunikat = ErrorList.objects.get(id=komunikat_id)
    modul = ModulName.objects.get(id=modul_id)

    InsertLog(data, godz, modul, komunikat, s, kto)


def InitLog():
    lenLoop = LOG_LOOP

    # test - przycinanie tablicy Log - za długa
    log = Log.objects.all()
    if len(log) > lenLoop:
        d = len(log) - lenLoop
        logs = Log.objects.all()[:d]
        for l in logs:
            Log.objects.get(pk=l.id).delete()

    if len(log) < lenLoop:
        li = lenLoop - len(log)
        for i in range(0, li):
            d = Log(opis='', kto='', status='', status_id=-1)
            d.save()


    flg = FlagaZmiany.objects.get(id=1)
    flg.loop_count = int(Log.objects.all().values_list('id').first()[0])
    flg.save()


def InsertLog(data, godz, modul, komunikat, opis, kto):
    fz = FlagaZmiany.objects.get(id=1).loop_count
    # print(fz)

    row = Log.objects.get(id=fz)
    row = next_in_order(row, loop=True)
    row.data = data
    row.godz = godz
    row.komunikat_id = komunikat.id
    row.modul_id = modul.id
    row.opis = opis
    row.kto  = kto
    row.status = komunikat.status
    row.status_id = komunikat.status_id
    row.nowy = True
    row.save()

    # print(">>> ", row.id, row.data, row.godz,row.opis,row.kto, row.status)

    flg = FlagaZmiany.objects.get(id=1)
    flg.loop_count = int(row.id)
    flg.save()


# Funkcja podpięta pod cron-a
def LogToFile():
    path = LOG_FILE
    tab = Log.objects.filter(nowy=True)

    for t in tab:
        p = path+str(t.data)
        isExist = os.path.exists(p)
        if not isExist:
            os.makedirs(p)
        name_f = p + '/' + str(t.data) + ' ' + str(t.modul) + '.log'
        f = open(name_f, 'a+')
        row = str(t.kto)+'    '+str(t.data)+'    '+str(t.godz)+'    '+str(t.modul)+'    '+str(t.status)+'   '+str(t.komunikat)+'    '+str(t.opis)+'\n'
        f.write(row)
        f.close()

        if t.status_id != 1:
            name_f = p + '/problems.log'
            f = open(name_f, 'a+')
            row = str(t.kto)+'    '+str(t.data) + '    ' + str(t.godz) + '    ' + str(t.modul) + '    ' + str(t.status) + '   ' + str(
                t.komunikat) + '    ' + str(t.opis) + '\n'
            f.write(row)
            f.close()

        r = Log.objects.get(pk=t.id)
        r.nowy = False
        r.save()

