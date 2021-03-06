from django.conf import settings
import requests
from CARS.models import Auto
from TaskAPI.models import Asp, FlagaZmiany, Rok, Waluta
from .functions import TestData, TestDataUslugi
from SDA.settings import GET_NBP, HIS_NBP
from moneyed import Money, PLN
from ORDERS.models import NrSDE as ZNrSDE, NrMPK
from LOG.logs import LogiCron
import gspread
import datetime
from .rap_temp import email_temp1, email_temp2, ubezpieczenie, ubezpieczenie_p
from HIP.models import Profil
from SERVICES.models import Usluga
import time

cred = settings.GOOGLE_CRED


def FixYear():
    tab = ZNrSDE.objects.all()
    for r in tab:
        if r.rok == 0:
            r.rok = 2021
            r.save()


def UpdateSde():
    zsde = ZNrSDE.objects.all()
    for z in zsde:
        zs = str(z.nazwa).split('_')
        l = len(zs)
        s =''
        try:
            i  = int(zs[0])
            if l == 3:
                s = str(zs[2]) + "_"+str(zs[0])+str(zs[1])
            else:
                s = str(zs[1]) + "_"+str(zs[0])
        except:
            if l == 4:
                s = str(zs[0]) + "_"+str(zs[1]) + "_" +str(zs[2]+str(zs[3]))
            else:
                s = str(zs[0]) + "_"+str(zs[1]) + "_" + str(zs[2])
        z.nazwa_id = s
        z.save()


        # print(str(zs) + "  >>> " + s)


def test_rok():
    tst = Rok.objects.all().order_by('rok')
    lata = []
    rok = 0
    for t in tst:
        lata.append(t.rok)
        if t.flg == 1:
            rok = t.rok
    return rok


def test_Cars_manual():
    data = datetime.datetime.now().strftime('%Y-%m-%d')
    auto = Auto.objects.filter(arch=False, sprzedany=False)
    cel = 2 # #settings.CARS_TO_TARGET

    if cel == 1:
        info = ''
        for au in auto:
            tst = au.stu
            if tst == 1:
                info += "UBEZPIECZENIE[ " + str(au.us) + " ]: TERMIN PŁATNOŚCI." + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"
            if tst == 2:
                info += "UBEZPIECZENIE[ " + str(au.us) + " ]: PRZETERMINOWNE!!!" + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"

            tst = au.stp
            if tst == 1:
                info += "PRZEGLĄD[ " + str(au.ps) + " ]: ZBLIŻA SIĘ TERMIN." + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"
            if tst == 2:
                info += "PRZEGLĄD[ " + str(au.ps) + " ]: PO TERMINIE!!!" + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"

            tst = au.stdzl
            if tst == 1:
                info += "LEASING[ " + str(au.dzl) + " ]: ZBLIŻA SIĘ TERMIN." + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"
            if tst == 2:
                info += "LEASING[ " + str(au.dzl) + " ]: PO TERMINIE!!!" + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"

        adres = settings.CARS_SKYPE_DO_USERS
        tytul = ''
        LogiCron(0, str(adres), 'sda')

        if info != '':

            for adr in adres:
                asp = Asp.objects.create(cel=cel, adres=adr, tytul=tytul, info=info, data=data)
                asp.save()

    if cel == 2:
        info = ""
        for au in auto:
            tst = au.stu
            if tst == 1:
                info += ubezpieczenie(au.us, au.rodzaj, au.typ, au.rej)
            if tst == 2:
                info += ubezpieczenie_p(au.us, au.rodzaj, au.typ, au.rej)

            tst = au.stp
            if tst == 1:
                info += "<tr><td style='font-weight: bold;' width='170'>PRZEGLĄD</td><td width='120'>[ " + str(au.ps) + " ]</td><td width='10'>:</td><td style='color:blue;'>ZBLIŻA SIĘ TERMIN.</td></tr>"
                info += "<tr><td style='font-weight: bold;' colspan='2'>DOTYCZY</td><td>:</td><td style='color:blue;'>" + au.rodzaj + ", " + au.typ + ", " + au.rej + "</td></tr>"
                info += "<tr><td colspan='4'>&nbsp;</td></tr>"
            if tst == 2:
                info += "<tr><td style='font-weight: bold;' width='170'>PRZEGLĄD</td><td width='120'>[ " + str(au.ps) + " ]</td><td width='10'>:</td><td style='color:red;'>PO TERMINIE!!!</td></tr>"
                info += "<tr><td style='font-weight: bold;' colspan='2'>DOTYCZY</td><td>:</td><td style='color:red;'>" + au.rodzaj + ", " + au.typ + ", " + au.rej + "</td></tr>"
                info += "<tr><td colspan='4'>&nbsp;</td></tr>"

        for au in auto:
            tst = au.stdzl
            if tst == 1:
                info += "<tr><td style='font-weight: bold;' width='170'>LEASING</td><td width='120'>[ " + str(
                    au.dzl) + " ]</td><td width='10'>:</td><td style='color:blue;'>ZBLIŻA SIĘ TERMIN.</td></tr>"
                info += "<tr><td style='font-weight: bold;' colspan='2'>DOTYCZY</td><td>:</td><td style='color:blue;'>" + au.rodzaj + ", " + au.typ + ", " + au.rej + "</td></tr>"
                info += "<tr><td colspan='4'>&nbsp;</td></tr>"
            if tst == 2:
                info += "<tr><td style='font-weight: bold;' width='170'>LEASING</td><td width='120'>[ " + str(
                    au.dzl) + " ]</td><td width='10'>:</td><td style='color:red;'>PO TERMINIE!!!</td></tr>"
                info += "<tr><td style='font-weight: bold;' colspan='2'>DOTYCZY</td><td>:</td><td style='color:red;'>" + au.rodzaj + ", " + au.typ + ", " + au.rej + "</td></tr>"
                info += "<tr><td colspan='4'>&nbsp;</td></tr>"

        adres = ['jarek@smartdesign-expo.com',] # settings.CARS_EMAIL_DO_USERS
        tytul = 'INFORMACJE Z SDA MODUŁU CARS [test]'
        LogiCron(1, str(adres), 'sda')

        if info != '':

            cz1 = email_temp1(data)
            cz2 = email_temp2()
            info = cz1 + info + cz2

            # print(info)

            for adr in adres:
                asp = Asp.objects.create(cel=cel, adres=adr, tytul=tytul, info=info, data=data)
                asp.save()


def test_Cars():

    data = datetime.datetime.now().strftime('%Y-%m-%d')
    auto = Auto.objects.filter(arch=False, sprzedany=False)
    cel = settings.CARS_TO_TARGET

    if cel == 1:
        info = ''
        for au in auto:
            tst = au.stu
            if tst == 1:
                info += "UBEZPIECZENIE[ " + str(au.us) + " ]: TERMIN PŁATNOŚCI." + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"
            if tst == 2:
                info += "UBEZPIECZENIE[ " + str(au.us) + " ]: PRZETERMINOWNE!!!" + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"

            tst = au.stp
            if tst == 1:
                info += "PRZEGLĄD[ " + str(au.ps) + " ]: ZBLIŻA SIĘ TERMIN." + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"
            if tst == 2:
                info += "PRZEGLĄD[ " + str(au.ps) + " ]: PO TERMINIE!!!" + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"

            tst = au.stdzl
            if tst == 1:
                info += "LEASING[ " + str(au.dzl) + " ]: ZBLIŻA SIĘ TERMIN." + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"
            if tst == 2:
                info += "LEASING[ " + str(au.dzl) + " ]: PO TERMINIE!!!" + "\n"
                info += "DOTYCZY: " + au.rodzaj + ", " + au.typ + ", " + au.rej + "\n\n"

        adres = settings.CARS_SKYPE_DO_USERS
        tytul = ''
        LogiCron(0, str(adres), 'sda')

        if info != '':

            for adr in adres:
                asp = Asp.objects.create(cel=cel, adres=adr, tytul=tytul, info=info, data=data)
                asp.save()

    if cel == 2:
        info = ""
        for au in auto:
            tst = au.stu
            if tst == 1:
                info += ubezpieczenie(au.us, au.rodzaj, au.typ, au.rej)
            if tst == 2:
                info += ubezpieczenie_p(au.us, au.rodzaj, au.typ, au.rej)

            tst = au.stp
            if tst == 1:
                info += "<tr><td style='font-weight: bold;' width='170'>PRZEGLĄD</td><td width='120'>[ " + str(
                    au.ps) + " ]</td><td width='10'>:</td><td style='color:blue;'>ZBLIŻA SIĘ TERMIN.</td></tr>"
                info += "<tr><td style='font-weight: bold;' colspan='2'>DOTYCZY</td><td>:</td><td style='color:blue;'>" + au.rodzaj + ", " + au.typ + ", " + au.rej + "</td></tr>"
                info += "<tr><td colspan='4'>&nbsp;</td></tr>"
            if tst == 2:
                info += "<tr><td style='font-weight: bold;' width='170'>PRZEGLĄD</td><td width='120'>[ " + str(
                    au.ps) + " ]</td><td width='10'>:</td><td style='color:red;'>PO TERMINIE!!!</td></tr>"
                info += "<tr><td style='font-weight: bold;' colspan='2'>DOTYCZY</td><td>:</td><td style='color:red;'>" + au.rodzaj + ", " + au.typ + ", " + au.rej + "</td></tr>"
                info += "<tr><td colspan='4'>&nbsp;</td></tr>"

        for au in auto:
            tst = au.stdzl
            if tst == 1:
                info += "<tr><td style='font-weight: bold;' width='170'>LEASING</td><td width='120'>[ " + str(
                    au.dzl) + " ]</td><td width='10'>:</td><td style='color:blue;'>ZBLIŻA SIĘ TERMIN.</td></tr>"
                info += "<tr><td style='font-weight: bold;' colspan='2'>DOTYCZY</td><td>:</td><td style='color:blue;'>" + au.rodzaj + ", " + au.typ + ", " + au.rej + "</td></tr>"
                info += "<tr><td colspan='4'>&nbsp;</td></tr>"
            if tst == 2:
                info += "<tr><td style='font-weight: bold;' width='170'>LEASING</td><td width='120'>[ " + str(
                    au.dzl) + " ]</td><td width='10'>:</td><td style='color:red;'>PO TERMINIE!!!</td></tr>"
                info += "<tr><td style='font-weight: bold;' colspan='2'>DOTYCZY</td><td>:</td><td style='color:red;'>" + au.rodzaj + ", " + au.typ + ", " + au.rej + "</td></tr>"
                info += "<tr><td colspan='4'>&nbsp;</td></tr>"

        adres = settings.CARS_EMAIL_DO_USERS
        tytul = 'INFORMACJE Z SDA MODUŁU CARS'
        LogiCron(1, str(adres), 'sda')

        if info != '':

            cz1 = email_temp1(data)
            cz2 = email_temp2()
            info = cz1 + info + cz2

            for adr in adres:
                asp = Asp.objects.create(cel=cel, adres=adr, tytul=tytul, info=info, data=data)
                asp.save()


def select_Cars():

    shift = settings.CARS_DATE_SHIFT
    lshift = settings.CARS_LEASING_SHIFT

    auto = Auto.objects.all()
    for au in auto:
        a = Auto.objects.get(pk=au.id)
        a.stu = TestData(str(au.us), shift, au.koniecl, au.sprzedany, au.arch, False)
        a.stp = TestData(str(au.us), shift, au.koniecl, au.sprzedany, au.arch, False)
        a.stdrl = 0
        a.stdzl = TestData(str(au.dzl), lshift, au.koniecl, au.sprzedany, au.arch, True)
        a.save()

    LogiCron(2, "", 'sda')
    ServiceDataTest()


def ServiceDataTest():
    shift = settings.SERVICES_DATA_SHIFT
    konta = Profil.objects.all().exclude(data_waznosci=None)
    usluga = Usluga.objects.all().exclude(data_waznosci=None)

    for kt in konta:
        k = Profil.objects.get(pk=kt.id)
        dw = str(kt.data_waznosci)
        k.termin = TestDataUslugi(dw , shift)
        k.save()

    for us in usluga:
        u = Usluga.objects.get(pk=us.id)
        dw = str(us.data_waznosci)
        u.termin = TestDataUslugi(dw, shift)
        u.save()


# Co min.update danych
def AllUpdate():
    fl = FlagaZmiany.objects.all().first()

    # Wywołanie "ręczne"
    if fl.do_google > 0:
        SendData()
        fl.licznik = 0    # kasuje licznik po każdym "ręcznym" wywołaniu co ogranicza ruch w sieci
        fl.do_google = 0  # kasuje sygnał startu "ręcznego"
        fl.save()

    # Wywołanie czasowe co 15min.
    licznik = fl.licznik + 1
    if licznik > 15:
        SendData()
        licznik = 0
    fl.licznik = licznik
    fl.save()



def SendData():
    try:
        start_time = time.time()
        WriteANALIZAtoGS()
        AllMPKWriteToGoogle()
        AllSDEWriteToGoogle()
        t = "Czas transmisji: %s s." % round((time.time() - start_time), 3)
        s =  "Plik Google - dane za rok 2021, Odczyt, zapis prawidłowy. " + t
        LogiCron(3, s, 'sda')
    except:
        s = "Plik Google - dane za rok 2021, Problem z odczytem lub zapisem."
        LogiCron(4, s, 'sda')

    try:
        start_time = time.time()
        SDA_SDEtoGS(2022)
        SDA_KosztyToGS(2022)
        SDA_MPKtoGS(2022)
        SDA_InfoToGS(2022)
        t = "Czas transmisji: %s s." % round((time.time() - start_time), 3)
        s =  "Plik Google - dane za rok 2022, Odczyt, zapis prawidłowy. " + t
        LogiCron(3, s, 'sda')
    except:
        s = "Plik Google - dane za rok 2022, Problem z odczytem lub zapisem."
        LogiCron(4, s, 'sda')



def GetGStoWR(fname, file_key, arkusz, cred):
    res = []
    gc = gspread.service_account(filename=cred)
    sh = gc.open_by_key(file_key)
    worksheet = sh.worksheet(arkusz)
    return worksheet


def MtF(d):
    o = str(d.amount)
    o = float(o)
    return o


'''
                          Dokumenty   2021
'''

def AllSDEWriteToGoogle():
    WriteSDEtoGS()
    WriteSDEtoGS1()
    j = TestPozStart()
    SDEtoGS_KosztyProdukcji(j)


def AllMPKWriteToGoogle():
    WriteMPKtoGS()


def TestPozStart():
    fname = 'PRODUKACJA - pensje 21'
    file_key = '1R0gvfgwquqEjUQEM7JJSxdC7Uo1R7Tyh_fx2By5uKYs'
    arkusz = 'projekty SDE'
    handler = GetGStoWR(fname, file_key, arkusz, cred)

    cell = handler.find("001_2021")

    return int(cell.row)


def WriteSDEtoGS():
    fname = 'Nr zleceń SmartDesignExpo 2019, 2020, 2021 i 2022'
    file_key = '1Ev5MQW6GAg3XXsqads58orF_3WrMA35XCgKCYPFrB70'
    arkusz = '2021'
    handler = GetGStoWR(fname, file_key, arkusz, cred)

    tab = ZNrSDE.objects.filter(rokk=2021).order_by('nazwa_id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 1, 'Nr zlecenia'))
    cells.append(gspread.Cell(i, 2, 'Nazwa Klienta/Agencja'))
    cells.append(gspread.Cell(i, 3, 'Nazwa Targów'))
    cells.append(gspread.Cell(i, 4, 'Nazwa STOISKA'))
    cells.append(gspread.Cell(i, 5, 'FAKTURA SPRZEDAŻOWA \n(data sprzedaży na FV)'))
    cells.append(gspread.Cell(i, 6, 'Project Manager'))
    cells.append(gspread.Cell(i, 7, 'UWAGI \n(zc: ' + dt + ')'))
    for r in tab:
        i += 1
        cells.append(gspread.Cell(i, 1, r.nazwa))
        cells.append(gspread.Cell(i, 2, r.klient))
        cells.append(gspread.Cell(i, 3, r.targi))
        cells.append(gspread.Cell(i, 4, r.opis))
        cells.append(gspread.Cell(i, 5, r.mcs + " " + r.rks))
        cells.append(gspread.Cell(i, 6, r.pm))
        cells.append(gspread.Cell(i, 7, r.uwagi))

    handler.update_cells(cells)


def WriteSDEtoGS1():
    fname = '2021 _SDE_plan finansowy_realizacja_2021'
    file_key = '1X31CMbPMdSo4whN2w_PcHQwFCcRINdN8E3eeSY6AbcM'
    arkusz = 'Nr zleceń SmartDesignExpo'
    handler = GetGStoWR(fname, file_key, arkusz, cred)

    tab = ZNrSDE.objects.filter(rokk=2021).order_by('nazwa_id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 2, 'Ostatnia aktualizacja: ' + dt + ' [' + gd + ']'))
    i += 1
    cells.append(gspread.Cell(i, 1, 'Nr zlecenia'))
    cells.append(gspread.Cell(i, 2, 'Nazwa Klienta/Agencja'))
    cells.append(gspread.Cell(i, 3, 'Nazwa Projektu'))
    cells.append(gspread.Cell(i, 4, 'Nazwa Stoiska'))
    cells.append(gspread.Cell(i, 5, 'Faktura sprzedażowa \n(data sprzedaży na FV)'))
    cells.append(gspread.Cell(i, 6, 'Project Manager'))
    cells.append(gspread.Cell(i, 7, 'Uwagi'))
    for r in tab:
        i += 1
        cells.append(gspread.Cell(i, 1, r.nazwa))
        cells.append(gspread.Cell(i, 2, r.klient))
        cells.append(gspread.Cell(i, 3, r.targi))
        cells.append(gspread.Cell(i, 4, r.opis))
        cells.append(gspread.Cell(i, 5, r.mcs + " " + r.rks))
        cells.append(gspread.Cell(i, 6, r.pm))
        cells.append(gspread.Cell(i, 7, r.uwagi))

    handler.update_cells(cells)


def SDEtoGS_KosztyProdukcji(j):
    fname = '2021 _SDE_plan finansowy_realizacja_2021'
    file_key = '1X31CMbPMdSo4whN2w_PcHQwFCcRINdN8E3eeSY6AbcM'
    arkusz = 'SDE_koszty_produkcji'
    handler = GetGStoWR(fname, file_key, arkusz, cred)

    tab = ZNrSDE.objects.filter(rok=2021, rokk=2021).order_by('nazwa_id')  # SDE z 2021

    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 2, 'Ostatnia aktualizacja: ' + dt + ' [' + gd + ']'))
    i = i + 4
    #j = 12

    for r in tab:
        macro1 = '=IMPORTRANGE("https://docs.google.com/spreadsheets/d/1R0gvfgwquqEjUQEM7JJSxdC7Uo1R7Tyh_fx2By5uKYs/edit#gid=0";"projekty SDE!f' + str(j) + '")'
        j = j + 2
        macro2 = '=REALIZACJA!$B$26*I' + str(i)
        macro3 = '=REALIZACJA!$B$27*I' + str(i)
        macro4 = '=REALIZACJA!$B$25*L' + str(i)
        macro5 = '=(REALIZACJA!$B$28)'
        macro6 = '=SUMA(F' + str(i) + ': T' + str(i) + ')'
        cells.append(gspread.Cell(i, 2, r.nazwa))
        cells.append(gspread.Cell(i, 3, r.opis))
        cells.append(gspread.Cell(i, 4, r.targi))
        cells.append(gspread.Cell(i, 6, MtF(r.sum_direct)))
        cells.append(gspread.Cell(i, 7, MtF(r.sum_cash)))
        cells.append(gspread.Cell(i, 9, macro1))
        cells.append(gspread.Cell(i, 10, macro2))
        cells.append(gspread.Cell(i, 11, macro3))
        cells.append(gspread.Cell(i, 13, macro4))
        cells.append(gspread.Cell(i, 16, macro5))
        cells.append(gspread.Cell(i, 21, macro6))
        i += 1
    handler.update_cells(cells, value_input_option='USER_ENTERED')


def WriteMPKtoGS():
    fname = '2021 _SDE_plan finansowy_realizacja_2021'
    file_key = '1X31CMbPMdSo4whN2w_PcHQwFCcRINdN8E3eeSY6AbcM'
    arkusz = 'KOSZTY STAŁE'
    handler = GetGStoWR(fname, file_key, arkusz, cred)

    tab = NrMPK.objects.filter(rok=2021).order_by('id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 2, 'Ostatnia aktualizacja: ' + dt + ' [' + gd + ']'))
    i += 1
    cells.append(gspread.Cell(i, 1, 'Nr MPK'))
    cells.append(gspread.Cell(i, 2, 'Opis'))
    cells.append(gspread.Cell(i, 3, 'UWAGI'))
    cells.append(gspread.Cell(i, 4, 'Suma pozycji'))
    cells.append(gspread.Cell(i, 5, 'Styczeń'))
    cells.append(gspread.Cell(i, 6, 'Luty'))
    cells.append(gspread.Cell(i, 7, 'Marzec'))
    cells.append(gspread.Cell(i, 8, 'Kwiecień'))
    cells.append(gspread.Cell(i, 9, 'Maj'))
    cells.append(gspread.Cell(i, 10, 'Czerwiec'))
    cells.append(gspread.Cell(i, 11, 'Lipiec'))
    cells.append(gspread.Cell(i, 12, 'Sierpień'))
    cells.append(gspread.Cell(i, 13, 'Wrzesień'))
    cells.append(gspread.Cell(i, 14, 'Październik'))
    cells.append(gspread.Cell(i, 15, 'Listopad'))
    cells.append(gspread.Cell(i, 16, 'Grudzień'))
    cells.append(gspread.Cell(i, 17, 'Bez daty'))
    for r in tab:
        i += 1
        cells.append(gspread.Cell(i, 1, r.nazwa))
        cells.append(gspread.Cell(i, 2, r.opis))
        cells.append(gspread.Cell(i, 3, r.uwagi))
        sum = r.sum_zal + r.sum_zam
        cells.append(gspread.Cell(i, 4, MtF(sum)))
        cells.append(gspread.Cell(i, 5, MtF(r.st)))
        cells.append(gspread.Cell(i, 6, MtF(r.lu)))
        cells.append(gspread.Cell(i, 7, MtF(r.ma)))
        cells.append(gspread.Cell(i, 8, MtF(r.kw)))
        cells.append(gspread.Cell(i, 9, MtF(r.mj)))
        cells.append(gspread.Cell(i, 10, MtF(r.cz)))
        cells.append(gspread.Cell(i, 11, MtF(r.lp)))
        cells.append(gspread.Cell(i, 12, MtF(r.si)))
        cells.append(gspread.Cell(i, 13, MtF(r.wr)))
        cells.append(gspread.Cell(i, 14, MtF(r.pa)))
        cells.append(gspread.Cell(i, 15, MtF(r.li)))
        cells.append(gspread.Cell(i, 16, MtF(r.gr)))
        cells.append(gspread.Cell(i, 17, MtF(r.b_d)))

    handler.update_cells(cells)


def WriteANALIZAtoGS():

    fname = '2021 _SDE_plan finansowy_realizacja_2021'
    file_key = '1X31CMbPMdSo4whN2w_PcHQwFCcRINdN8E3eeSY6AbcM'
    arkusz = 'ANALIZA'
    handler = GetGStoWR(fname,file_key, arkusz, cred)
    tzero = Money('00.00', PLN)

    #tab = ZNrSDE.objects.filter(rok=2021).order_by('nazwa')
    tab1 = ZNrSDE.objects.filter(rok=2021, rokk=2020).order_by('nazwa_id') # SDE z 2020
    tab2 = ZNrSDE.objects.filter(rok=2021, rokk=2021).order_by('nazwa_id') # SDE z 2021

    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 1, 'Ostatnia aktualizacja: '+dt+' ['+gd+']'))
    i += 1
    i += 1
    for r in tab1:
        cells.append(gspread.Cell(i, 1, r.targi))
        cells.append(gspread.Cell(i, 2, r.opis))
        cells.append(gspread.Cell(i, 3, r.nazwa))
        cells.append(gspread.Cell(i, 5, MtF(r.sum_direct)))
        cells.append(gspread.Cell(i, 6, MtF(r.sum_cash)))
        i += 1
        cells.append(gspread.Cell(i, 1, ''))
        cells.append(gspread.Cell(i, 2, ''))
        cells.append(gspread.Cell(i, 3, ''))
        cells.append(gspread.Cell(i, 5, ''))
        cells.append(gspread.Cell(i, 6, ''))
        i += 1
    for r in tab2:
        cells.append(gspread.Cell(i, 1, r.targi))
        cells.append(gspread.Cell(i, 2, r.opis))
        cells.append(gspread.Cell(i, 3, r.nazwa))
        cells.append(gspread.Cell(i, 5, MtF(r.sum_direct)))
        cells.append(gspread.Cell(i, 6, MtF(r.sum_cash)))
        i += 1
        cells.append(gspread.Cell(i, 1, ''))
        cells.append(gspread.Cell(i, 2, ''))
        cells.append(gspread.Cell(i, 3, ''))
        cells.append(gspread.Cell(i, 5, ''))
        cells.append(gspread.Cell(i, 6, ''))
        i += 1

    handler.update_cells(cells)


'''
    NBP
'''
def GetNBP():
    GetCurrencyNBP(GET_NBP, HIS_NBP)


def GetCurrencyNBP(GET_NBP, HIS_NBP):

    for W in GET_NBP:
        url = 'http://api.nbp.pl/api/exchangerates/rates/a/' + W + '/last/' + str(HIS_NBP) + '/?format=json'
        waluty = requests.get(url).json()

        for w in waluty['rates']:
            wal = Money(w['mid'], PLN)
            TAB = str(w['no'])
            KOD = str(W)
            obj, created = Waluta.objects.filter(kod=KOD).get_or_create(tab=TAB)
            obj.tab = w['no']
            obj.kod = W
            obj.data = str(w['effectiveDate'])
            obj.kurs = wal
            obj.save()

    LogiCron(5, '', 'sda')


'''
 'Nr zleceń SmartDesignExpo 2019, 2020, 2021 i 2022', '1Ev5MQW6GAg3XXsqads58orF_3WrMA35XCgKCYPFrB70', '2022', ''
'''
def SDA_InfoToGS(rokk):
    crd = settings.GOOGLE_CRED
    set_docs = settings.GOOGLE_DOCS_2022
    fname = set_docs[3][0]
    file_key = set_docs[3][1]
    arkusz = set_docs[3][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = ZNrSDE.objects.filter(rokk=rokk).order_by('nazwa_id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    cz = datetime.datetime.now().strftime("%H:%M:%S")
    zc = "Ostatnia aktualizacja: "+dt+" [ "+cz+" ]"

    cells = []
    i = 1
    cells.append(gspread.Cell(i, 1, zc))
    i += 1
    cells.append(gspread.Cell(i, 1, 'Nr zlecenia'))
    cells.append(gspread.Cell(i, 2, 'Nazwa Klienta/Agencja'))
    cells.append(gspread.Cell(i, 3, 'Nazwa Targów'))
    cells.append(gspread.Cell(i, 4, 'Nazwa STOISKA'))
    cells.append(gspread.Cell(i, 5, 'FAKTURA SPRZEDAŻOWA \n(data sprzedaży na FV)'))
    cells.append(gspread.Cell(i, 6, 'Project Manager'))
    cells.append(gspread.Cell(i, 7, 'UWAGI'))
    for r in tab:
        i += 1
        cells.append(gspread.Cell(i, 1, r.nazwa))
        cells.append(gspread.Cell(i, 2, r.klient))
        cells.append(gspread.Cell(i, 3, r.targi))
        cells.append(gspread.Cell(i, 4, r.opis))
        cells.append(gspread.Cell(i, 5, r.mcs + " " + r.rks))
        cells.append(gspread.Cell(i, 6, r.pm))
        cells.append(gspread.Cell(i, 7, r.uwagi))

    handler.update_cells(cells)


'''
 'Realizacja 2022', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'SDA [Kody SDE]'
'''
def SDA_SDEtoGS(rokk):
    crd = settings.GOOGLE_CRED
    set_docs = settings.GOOGLE_DOCS_2022
    fname = set_docs[0][0]
    file_key = set_docs[0][1]
    arkusz = set_docs[0][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = ZNrSDE.objects.filter(rokk=rokk).order_by('nazwa_id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    cz = datetime.datetime.now().strftime("%H:%M:%S")
    zc = "Ostatnia aktualizacja: "+dt+" [ "+cz+" ]"

    cells = []
    i = 1
    cells.append(gspread.Cell(i, 1, zc))
    i += 1
    cells.append(gspread.Cell(i, 1, 'Nr zlecenia'))
    cells.append(gspread.Cell(i, 2, 'Nazwa Klienta/Agencja'))
    cells.append(gspread.Cell(i, 3, 'Nazwa Targów'))
    cells.append(gspread.Cell(i, 4, 'Nazwa STOISKA'))
    cells.append(gspread.Cell(i, 5, 'FAKTURA SPRZEDAŻOWA \n(data sprzedaży na FV)'))
    cells.append(gspread.Cell(i, 6, 'Project Manager'))
    cells.append(gspread.Cell(i, 7, 'UWAGI'))
    for r in tab:
        i += 1
        cells.append(gspread.Cell(i, 1, r.nazwa))
        cells.append(gspread.Cell(i, 2, r.klient))
        cells.append(gspread.Cell(i, 3, r.targi))
        cells.append(gspread.Cell(i, 4, r.opis))
        cells.append(gspread.Cell(i, 5, r.mcs + " " + r.rks))
        cells.append(gspread.Cell(i, 6, r.pm))
        cells.append(gspread.Cell(i, 7, r.uwagi))

    handler.update_cells(cells)


'''
 'Realizacja 2022', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'SDA [Koszty produkcji]'
'''
def SDA_KosztyToGS(rokk):
    crd = settings.GOOGLE_CRED
    set_docs = settings.GOOGLE_DOCS_2022
    # print(set_docs)
    fname = set_docs[1][0]
    file_key = set_docs[1][1]
    arkusz = set_docs[1][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = ZNrSDE.objects.filter(rokk=rokk).order_by('nazwa_id')  # SDE z 2022, rok=2021,

    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    zc = "Ostatnia aktualizacja: " + dt + " [ " + gd + " ]"
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 1, zc))
    i += 1
    cells.append(gspread.Cell(i, 1, 'Nr zlecenia'))
    cells.append(gspread.Cell(i, 2, 'Nazwa Klienta/Agencja'))
    cells.append(gspread.Cell(i, 3, 'Nazwa Projektu'))
    cells.append(gspread.Cell(i, 4, 'Koszty \nbezpośrednie'))
    cells.append(gspread.Cell(i, 5, 'Koszty \ngotówkowe'))
    i += 1
    for r in tab:
        cells.append(gspread.Cell(i, 1, r.nazwa))
        cells.append(gspread.Cell(i, 2, r.opis))
        cells.append(gspread.Cell(i, 3, r.targi))
        cells.append(gspread.Cell(i, 4, MtF(r.sum_direct)))
        cells.append(gspread.Cell(i, 5, MtF(r.sum_cash)))
        i += 1
    handler.update_cells(cells)


'''
 'Realizacja 2022', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'SDA [Koszty stałe]'
'''
def SDA_MPKtoGS(rokk):
    crd = settings.GOOGLE_CRED
    set_docs = settings.GOOGLE_DOCS_2022
    fname = set_docs[2][0]
    file_key = set_docs[2][1]
    arkusz = set_docs[2][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = NrMPK.objects.filter(rok=rokk).order_by('id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    zc = "Ostatnia aktualizacja: " + dt + " [ " + gd + " ]"
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 1, zc))
    cells.append(gspread.Cell(i, 4, '=SUMA(D3:D)'))
    cells.append(gspread.Cell(i, 5, '=SUMA(E3:E)'))
    cells.append(gspread.Cell(i, 6, '=SUMA(F3:F)'))
    cells.append(gspread.Cell(i, 7, '=SUMA(G3:G)'))
    cells.append(gspread.Cell(i, 8, '=SUMA(H3:H)'))
    cells.append(gspread.Cell(i, 9, '=SUMA(I3:I)'))
    cells.append(gspread.Cell(i, 10, '=SUMA(J3:J)'))
    cells.append(gspread.Cell(i, 11, '=SUMA(K3:K)'))
    cells.append(gspread.Cell(i, 12, '=SUMA(L3:L)'))
    cells.append(gspread.Cell(i, 13, '=SUMA(M3:M)'))
    cells.append(gspread.Cell(i, 14, '=SUMA(N3:N)'))
    cells.append(gspread.Cell(i, 15, '=SUMA(O3:O)'))
    cells.append(gspread.Cell(i, 16, '=SUMA(P3:P)'))
    cells.append(gspread.Cell(i, 17, '=SUMA(Q3:Q)'))
    i += 1
    cells.append(gspread.Cell(i, 1, 'Kod MPK'))
    cells.append(gspread.Cell(i, 2, 'Opis'))
    cells.append(gspread.Cell(i, 3, 'Uwagi'))
    cells.append(gspread.Cell(i, 4, 'Suma pozycji'))
    cells.append(gspread.Cell(i, 5, 'Styczeń'))
    cells.append(gspread.Cell(i, 6, 'Luty'))
    cells.append(gspread.Cell(i, 7, 'Marzec'))
    cells.append(gspread.Cell(i, 8, 'Kwiecień'))
    cells.append(gspread.Cell(i, 9, 'Maj'))
    cells.append(gspread.Cell(i, 10, 'Czerwiec'))
    cells.append(gspread.Cell(i, 11, 'Lipiec'))
    cells.append(gspread.Cell(i, 12, 'Sierpień'))
    cells.append(gspread.Cell(i, 13, 'Wrzesień'))
    cells.append(gspread.Cell(i, 14, 'Październik'))
    cells.append(gspread.Cell(i, 15, 'Listopad'))
    cells.append(gspread.Cell(i, 16, 'Grudzień'))
    cells.append(gspread.Cell(i, 17, 'Bez daty'))
    for r in tab:
        i += 1
        cells.append(gspread.Cell(i, 1, r.nazwa))
        cells.append(gspread.Cell(i, 2, r.opis))
        cells.append(gspread.Cell(i, 3, r.uwagi))
        sum = r.sum_zal + r.sum_zam
        cells.append(gspread.Cell(i, 4, MtF(sum)))
        cells.append(gspread.Cell(i, 5, MtF(r.st)))
        cells.append(gspread.Cell(i, 6, MtF(r.lu)))
        cells.append(gspread.Cell(i, 7, MtF(r.ma)))
        cells.append(gspread.Cell(i, 8, MtF(r.kw)))
        cells.append(gspread.Cell(i, 9, MtF(r.mj)))
        cells.append(gspread.Cell(i, 10, MtF(r.cz)))
        cells.append(gspread.Cell(i, 11, MtF(r.lp)))
        cells.append(gspread.Cell(i, 12, MtF(r.si)))
        cells.append(gspread.Cell(i, 13, MtF(r.wr)))
        cells.append(gspread.Cell(i, 14, MtF(r.pa)))
        cells.append(gspread.Cell(i, 15, MtF(r.li)))
        cells.append(gspread.Cell(i, 16, MtF(r.gr)))
        cells.append(gspread.Cell(i, 17, MtF(r.b_d)))

    handler.update_cells(cells, value_input_option='USER_ENTERED')







