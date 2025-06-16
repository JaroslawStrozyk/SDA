from django.conf import settings
import requests
from reportlab.lib.randomtext import subjects

from CARS.models import Auto
from COMP_REPO.models import Sklad
from COMP_REPO.views import test_data_uslugi_all
from INSURANCE.models import Ubezpieczenie, Termin
from TIMBER_WH.gen_tables import UpdateStat
from TaskAPI.models import Asp, FlagaZmiany, Rok, Waluta
from WORKER.models import Podsumowanie, Pensja, Pracownik
from .functions import TestData, TestDataUslugi, LiczbaDoTekst
from SDA.settings import GET_NBP, HIS_NBP, LST_MPK_SDE, INFO_PROGRAM
from moneyed import Money, PLN
from ORDERS.models import NrSDE as ZNrSDE, NrMPK
from LOG.logs import logi_cron
import gspread
import datetime
from .rap_temp import email_body, email_temp1, email_temp2, ubezpieczenie, ubezpieczenie_p, insurance, insurance_after, \
    term, term_after, timber, timber_after, faktura_body, delegacja_body
from HIP.models import Profil
from SERVICES.models import Usluga
import time
import socket
from datetime import datetime
import datetime
# TEST
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
EMAIL_USER = 'smartinfo@smartdesign-expo.com'
EMAIL_PASS = 'Smart2018!@#'
EMAIL_SMTP = 'poczta.blanet.pl:587'



cred = settings.GOOGLE_CRED


# TEST

def test_email():
    send_to = "jarek@smartdesign-expo.com"

    osoba="Karolina Czabaj"
    targi="Gitex 2025"
    stoisko="Ricoh"
    rodzaj_fv="PROFORMA"
    termin="2025-02-27"
    kwota="500,00 €"
    za_co=""
    projekt_specyfikacja=""
    zgloszenie="2025-02-27 08:45:43"
    sda_wersja= INFO_PROGRAM[0]['WERSJA']
    subject = "Testowa wiadomość"
    body = faktura_body(osoba, targi, stoisko, rodzaj_fv, termin, kwota, za_co, projekt_specyfikacja, zgloszenie,sda_wersja)
    msg_email(send_to, subject, body)

    time.sleep(3)

    osoba="Bartosz Ługowski"
    targi="PSB Kielce"
    data_od="2025-03-02"
    data_do="2025-03-04"
    kasa_pln="1500"
    kasa_euro="0.0"
    kasa_funt="0.0"
    kasa_inna="0.0"
    kasa_karta="0,00 €"
    zgloszenie="2025-02-28 12:49:02"
    sda_wersja= INFO_PROGRAM[0]['WERSJA']
    subject = "Testowa wiadomość"
    body = delegacja_body(osoba, targi, data_od, data_do, kasa_pln, kasa_euro, kasa_funt, kasa_inna, kasa_karta, zgloszenie, sda_wersja)
    msg_email(send_to, subject, body)








def msg_email(send_to, subject, body):
    msg = MIMEMultipart()
    sender = EMAIL_USER
    password = EMAIL_PASS
    msg['From'] = sender
    msg['To'] = send_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    text=msg.as_string()
    server = smtplib.SMTP(EMAIL_SMTP)
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender, send_to, text)
    server.close()


def gen_new_mc():
    brok = datetime.now().year
    bmc = datetime.now().month

    if not Pensja.objects.filter(rok=brok, miesiac=bmc).exists():
        for pr in Pracownik.objects.filter(pracuje=True, lp_biuro=True):
            pr_id = Pracownik.objects.get(id=pr.id)
            os = pr.nazwisko + " " + pr.imie
            p = Pensja(rok=brok, miesiac=bmc, osoba=os, pracownik=pr_id, wynagrodzenie=pr.pensja_ust, stawka_wyj=pr.stawka_wyj, stawka_wyj_rob=pr.stawka_wyj_rob)
            p.save()




def TimberStat():
    UpdateStat(2023)


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
        logi_cron(0, str(adres), 0, 'sda')

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
        logi_cron(1, str(adres), 0, 'sda')

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
        logi_cron(0, str(adres), 0, 'sda')

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
        logi_cron(1, str(adres), 0, 'sda')

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
        a.stp = TestData(str(au.ps), shift, au.koniecl, au.sprzedany, au.arch, False)
        a.stdrl = 0
        a.stdzl = TestData(str(au.dzl), lshift, au.koniecl, au.sprzedany, au.arch, True)
        a.save()

    logi_cron(2, "", 0, 'sda')
    # ServiceDataTest()


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


def ServiceSendMsg():
    pass

    # adres = ''
    # tytul = ''
    # info = ''
    # data = datetime.datetime.now().strftime('%Y-%m-%d')
    # ub = Ubezpieczenie.objects.all().filter(stu__gte=2)
    # te = Termin.objects.all().filter(stt__gte=2)
    # cel = settings.INSURANCE_TO_TARGET
    #
    # if cel == 1:
    #     adres = settings.INSURANCE_SKYPE_DO_USERS
    #     tytul = ''
    #
    # if cel == 2: # EMAIL
    #     adres = settings.INSURANCE_EMAIL_DO_USERS
    #     tytul = 'INFORMACJE Z SDA MODUŁU SERVICES'
    #
    #     for u in ub:
    #         tst = u.stu
    #         if tst == 2:
    #             info += insurance(u.data_do, u.firma, u.nazwa, u.dotyczy)
    #         if tst == 3:
    #             info += insurance_after(u.data_do, u.firma, u.nazwa, u.dotyczy)
    #
    #     for t in te:
    #         tst = t.stt
    #         if tst == 2:
    #             info += term(t.data_do, t.firma, t.dotyczy)
    #         if tst == 3:
    #             info += term_after(t.data_do, t.firma, t.dotyczy)
    #
    #     title = 'Usługi'
    #     cz1 = email_body(title, data)
    #     cz2 = email_temp2()
    #
    #
    #     if info != '':
    #         info = cz1 + info + cz2
    #         f = open("/home/edatabit/Pulpit/"+tytul+".html", "w")
    #         f.write(info)
    #         f.close()
    #
    #         # for adr in adres:
    #         #     asp = Asp.objects.create(cel=cel, adres=adr, tytul=tytul, info=info, data=data)
    #         #     asp.save()


def InsuranceDataTest():
    shift = settings.INSURANCE_DATA_SHIFT
    ubezpieczenia = Ubezpieczenie.objects.all().exclude(data_do=None)
    terminy = Termin.objects.all().exclude(data_do=None)

    for ub in ubezpieczenia:
        dw = str(ub.data_do)
        fl = TestDataUslugi(dw, shift)
        ub.stu = fl
        ub.save()

    for te in terminy:
        dw = str(te.data_do)
        fl = TestDataUslugi(dw, shift)
        te.stt = fl
        te.save()


def InsuranceSendMsg():

    adres = ''
    tytul = ''
    info = ''
    data = datetime.datetime.now().strftime('%Y-%m-%d')
    ub = Ubezpieczenie.objects.all().filter(stu__gte=2)
    te = Termin.objects.all().filter(stt__gte=2)
    cel = settings.INSURANCE_TO_TARGET

    if cel == 1:
        adres = settings.INSURANCE_SKYPE_DO_USERS
        tytul = ''

    if cel == 2: # EMAIL
        adres = settings.INSURANCE_EMAIL_DO_USERS
        tytul = 'INFORMACJE Z SDA MODUŁU INSURANCE'

        for u in ub:
            tst = u.stu
            if tst == 2:
                info += insurance(u.data_do, u.firma, u.nazwa, u.dotyczy)
            if tst == 3:
                info += insurance_after(u.data_do, u.firma, u.nazwa, u.dotyczy)

        for t in te:
            tst = t.stt
            if tst == 2:
                info += term(t.data_do, t.firma, t.dotyczy)
            if tst == 3:
                info += term_after(t.data_do, t.firma, t.dotyczy)

        title = 'Ubezpieczenia i Terminy'
        cz1 = email_body(title, data)
        cz2 = email_temp2()

        if info != '':
            info = cz1 + info + cz2
            # f = open("/home/edatabit/Pulpit/"+tytul+".html", "w")
            # f.write(info)
            # f.close()

            for adr in adres:
                asp = Asp.objects.create(cel=cel, adres=adr, tytul=tytul, info=info, data=data)
                asp.save()


def TimberDataTest():
    test_data_uslugi_all()


def TimberSendMsg():

    adres = ''
    tytul = ''
    info = ''
    data = datetime.datetime.now().strftime('%Y-%m-%d')
    sk = Sklad.objects.filter(status__gte=1).distinct('nr_sde')
    cel = settings.TIMBER_TO_TARGET

    if cel == 1:
        adres = settings.TIMBER_SKYPE_DO_USERS
        tytul = ''

    if cel == 2: # EMAIL
        adres = settings.TIMBER_EMAIL_DO_USERS
        tytul = 'INFORMACJE Z SDA MODUŁU PRZECHOWALNIA'

        for s in sk:
            tst = s.status
            if tst == 1:
                info += timber(s.czas_do, s.magazyn, s.nr_sde.nazwa, s.nr_sde.targi, s.nr_sde.klient, s.nr_sde.stoisko, s.nr_sde.pm)
            if tst == 2:
                info += timber_after(s.czas_do, s.magazyn, s.nr_sde.nazwa, s.nr_sde.targi, s.nr_sde.klient, s.nr_sde.stoisko, s.nr_sde.pm)

        title = 'Lista elementów stoisk przechowywanych dla innych firm.'
        cz1 = email_body(title, data)
        cz2 = email_temp2()

        if info != '':
            info = cz1 + info + cz2
            # f = open("/home/edatabit/Pulpit/"+tytul+".html", "w")
            # f.write(info)
            # f.close()

            for adr in adres:
                asp = Asp.objects.create(cel=cel, adres=adr, tytul=tytul, info=info, data=data)
                asp.save()






'''

Usługi

'''


def AllUpdate():
    hn = socket.gethostname()
    MINUTE = datetime.datetime.now().minute

    '''
    Wysyłanie danych o okreslonych minutach w godzinie (co 15min.)
    '''
    if MINUTE in {0, 15, 30, 45}:
        SendData(hn)



def SendData(hn):

    # if hn != 'S540':
    #    try:
    #        start_time = time.time()
    #        WriteANALIZAtoGS(hn)
    #        time.sleep(1)
    #        AllMPKWriteToGoogle(hn)
    #        time.sleep(1)
    #        AllSDEWriteToGoogle(hn)
    #        t = round((time.time() - start_time), 3)
    #        s = "Plik Google - dane za rok 2021, Odczyt, zapis prawidłowy. "
    #        logi_cron(3, s, t, 'sda')
    #        time.sleep(1)
    #    except:
    #        s = "Plik Google - dane za rok 2021, Problem z odczytem lub zapisem."
    #        logi_cron(4, s, 0, 'sda')


    if hn != 'S540':

        # try:
        #     start_time = time.time()
        #     SDA_SDEtoGS(2022, hn)
        #     time.sleep(1)
        #     SDA_KosztyToGS(2022, hn)
        #     time.sleep(1)
        #     SDA_RealizacjaToGS(2022, hn)
        #     time.sleep(1)
        #     SDA_MPKtoGS(2022, hn)
        #     # time.sleep(1)
        #     # SDA_InfoToGS(2022, hn)
        #
        #     t =  round((time.time() - start_time), 3)
        #     s =  "Plik Google - dane za rok 2022,  prawidłowy zapis pakietu danych w DOCS. "
        #     logi_cron(3, s, t, 'sda')
        # except:
        #     s = "Plik Google - dane za rok 2022, Problem z zapisem do DOCS."
        #     logi_cron(4, s, 0, 'sda')


        # try:
        #     start_time = time.time()
        #     # SDA_InfoToGS(2023, hn)
        #     # time.sleep(1)
        #     SDA_SDEtoGS(2023, hn)
        #     time.sleep(1)
        #     SDA_KosztyToGS(2023, hn)
        #     time.sleep(1)
        #     SDA_MPKtoGS(2023, hn)
        #     time.sleep(1)
        #     SDA_PensjatoGS(2023, hn)
        #
        #     t = round((time.time() - start_time), 3)
        #     s =  "Plik Google - dane za rok 2023,  prawidłowy zapis pakietu danych w DOCS. "
        #     logi_cron(3, s, t, 'sda')
        # except:
        #     s = "Plik Google - dane za rok 2023, Problem z zapisem do DOCS."
        #     logi_cron(4, s, 0, 'sda')


        try:
            start_time = time.time()
            # SDA_InfoToGS(2023, hn)
            # time.sleep(1)
            SDA_SDEtoGS(2024, hn)
            time.sleep(1)
            SDA_KosztyToGS(2024, hn)
            time.sleep(1)
            SDA_MPKtoGS(2024, hn)
            time.sleep(1)
            # SDA_PensjatoGS(2023, hn)

            t = round((time.time() - start_time), 3)
            s =  "Plik Google - dane za rok 2024,  prawidłowy zapis pakietu danych w DOCS. "
            logi_cron(3, s, t, 'sda')
        except:
            s = "Plik Google - dane za rok 2024, Problem z zapisem do DOCS."
            logi_cron(4, s, 0,'sda')


        try:
            start_time = time.time()

            SDA_SDEtoGS(2025, hn)

            t = round((time.time() - start_time), 3)
            s =  "Plik Google - dane za rok 2025,  prawidłowy zapis pakietu danych w DOCS. "
            logi_cron(3, s, t, 'sda')
        except:
            s = "Plik Google - dane za rok 2025, Problem z zapisem do DOCS."
            logi_cron(4, s, 0,'sda')




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

def AllSDEWriteToGoogle(hn):
    WriteSDEtoGS(hn)
    WriteSDEtoGS1(hn)
    j = TestPozStart()
    SDEtoGS_KosztyProdukcji(j,hn)


def AllMPKWriteToGoogle(hn):
    WriteMPKtoGS(hn)


def TestPozStart():
    fname = 'PRODUKACJA - pensje 21'
    file_key = '1R0gvfgwquqEjUQEM7JJSxdC7Uo1R7Tyh_fx2By5uKYs'
    arkusz = 'projekty SDE'
    handler = GetGStoWR(fname, file_key, arkusz, cred)

    cell = handler.find("001_2021")

    return int(cell.row)


def WriteSDEtoGS(hn):
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
    cells.append(gspread.Cell(i, 7, 'UWAGI \n(zc: ' + dt +  ') ('+hn+')'))
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


def WriteSDEtoGS1(hn):
    fname = '2021 _SDE_plan finansowy_realizacja_2021'
    file_key = '1X31CMbPMdSo4whN2w_PcHQwFCcRINdN8E3eeSY6AbcM'
    arkusz = 'Nr zleceń SmartDesignExpo'
    handler = GetGStoWR(fname, file_key, arkusz, cred)

    tab = ZNrSDE.objects.filter(rokk=2021).order_by('nazwa_id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 2, 'Ostatnia aktualizacja: ' + dt + ' [' + gd + ' ] ('+hn+')'))
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


def SDEtoGS_KosztyProdukcji(j, hn):
    fname = '2021 _SDE_plan finansowy_realizacja_2021'
    file_key = '1X31CMbPMdSo4whN2w_PcHQwFCcRINdN8E3eeSY6AbcM'
    arkusz = 'SDE_koszty_produkcji'
    handler = GetGStoWR(fname, file_key, arkusz, cred)

    tab = ZNrSDE.objects.filter(rok=2021, rokk=2021).order_by('nazwa_id')  # SDE z 2021

    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 2, 'Ostatnia aktualizacja: ' + dt + ' [' + gd + ' ] ('+hn+')'))
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


def WriteMPKtoGS(hn):
    fname = '2021 _SDE_plan finansowy_realizacja_2021'
    file_key = '1X31CMbPMdSo4whN2w_PcHQwFCcRINdN8E3eeSY6AbcM'
    arkusz = 'KOSZTY STAŁE'
    handler = GetGStoWR(fname, file_key, arkusz, cred)

    tab = NrMPK.objects.filter(rok=2021).order_by('id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 2, 'Ostatnia aktualizacja: ' + dt + ' [' + gd + ' ] ('+hn+')'))
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


def WriteANALIZAtoGS(hn):

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
    cells.append(gspread.Cell(i, 1, 'Ostatnia aktualizacja: '+dt+' ['+gd+ ' ] ('+hn+')'))
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

    logi_cron(5, '', 0, 'sda')


'''
 'Nr zleceń SmartDesignExpo 2019, 2020, 2021 i 2022', '1Ev5MQW6GAg3XXsqads58orF_3WrMA35XCgKCYPFrB70', '2022', ''
'''
def SDA_InfoToGS(rokk, hn):
    crd = settings.GOOGLE_CRED
    if rokk == 2022:
        set_docs = settings.GOOGLE_DOCS_2022
    elif rokk == 2023:
        set_docs = settings.GOOGLE_DOCS_2023
    elif rokk == 2024:
        set_docs = settings.GOOGLE_DOCS_2024

    fname = set_docs[3][0]
    file_key = set_docs[3][1]
    arkusz = set_docs[3][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = ZNrSDE.objects.filter(rokk=rokk).order_by('nazwa_id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    cz = datetime.datetime.now().strftime("%H:%M:%S")
    zc = "Ostatnia aktualizacja: "+dt+" [ "+cz+" ] ("+hn+")"

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
 'Realizacja 2022, 2023, 2024, 2025', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'SDA [Kody SDE]'
'''
def SDA_SDEtoGS(rokk, hn):
    crd = settings.GOOGLE_CRED
    # set_docs = settings.GOOGLE_DOCS_2022
    if rokk == 2022:
        set_docs = settings.GOOGLE_DOCS_2022
    elif rokk == 2023:
        set_docs = settings.GOOGLE_DOCS_2023
    elif rokk == 2024:
        set_docs = settings.GOOGLE_DOCS_2024
    elif rokk == 2025:
        set_docs = settings.GOOGLE_DOCS_2025

    fname = set_docs[0][0]
    file_key = set_docs[0][1]
    arkusz = set_docs[0][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = ZNrSDE.objects.filter(rokk=rokk).order_by('nazwa_id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    cz = datetime.datetime.now().strftime("%H:%M:%S")
    zc = "Ostatnia aktualizacja: "+dt+" [ "+cz+" ] ("+hn+")"

    cells = []
    i = 1

    if rokk == 2022:
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
    elif rokk == 2023 or rokk == 2024 or rokk == 2025:
        cells.append(gspread.Cell(i, 1, zc))
        i += 1
        cells.append(gspread.Cell(i, 1, 'Nr zlecenia'))
        cells.append(gspread.Cell(i, 2, 'Nazwa Klienta/Agencja'))
        cells.append(gspread.Cell(i, 3, 'Nazwa Targów'))
        cells.append(gspread.Cell(i, 4, 'Nazwa STOISKA'))
        cells.append(gspread.Cell(i, 5, 'FAKTURA SPRZEDAŻOWA \n(data sprzedaży na FV)'))
        cells.append(gspread.Cell(i, 6, 'Project Manager'))
        cells.append(gspread.Cell(i, 7, 'Powierzchnia\nstoiska'))
        cells.append(gspread.Cell(i, 8, 'Powierzchnia\npiętra'))
        cells.append(gspread.Cell(i, 9, 'UWAGI'))
        for r in tab:
            i += 1
            cells.append(gspread.Cell(i, 1, r.nazwa))
            cells.append(gspread.Cell(i, 2, r.klient))
            cells.append(gspread.Cell(i, 3, r.targi))
            cells.append(gspread.Cell(i, 4, r.opis))
            cells.append(gspread.Cell(i, 5, r.mcs + " " + r.rks))
            cells.append(gspread.Cell(i, 6, r.pm))
            cells.append(gspread.Cell(i, 7, r.pow_stoisko))
            cells.append(gspread.Cell(i, 8, r.pow_pietra))
            cells.append(gspread.Cell(i, 9, r.uwagi))

    handler.update_cells(cells)


'''
 'Realizacja 2022/2023', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'SDA [Koszty produkcji]'
'''
def SDA_KosztyToGS(rokk, hn):
    crd = settings.GOOGLE_CRED
    if rokk == 2022:
        set_docs = settings.GOOGLE_DOCS_2022
    elif rokk == 2023:
        set_docs = settings.GOOGLE_DOCS_2023
    elif rokk == 2024:
        set_docs = settings.GOOGLE_DOCS_2024

    fname = set_docs[1][0]
    file_key = set_docs[1][1]
    arkusz = set_docs[1][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = ZNrSDE.objects.filter(rokk=rokk).order_by('nazwa_id')  # SDE z 2022, rok=2021,

    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    zc = "Ostatnia aktualizacja: " + dt + " [ " + gd + " ] ("+hn+")"
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 1, zc))
    i += 1
    cells.append(gspread.Cell(i, 1, 'Nr zlecenia'))
    cells.append(gspread.Cell(i, 2, 'Nazwa Klienta/Agencja'))
    cells.append(gspread.Cell(i, 3, 'Nazwa Projektu'))
    cells.append(gspread.Cell(i, 4, 'Koszty \nbezpośrednie'))
    cells.append(gspread.Cell(i, 5, 'Koszty \ngotówkowe'))
    if rokk == 2023 or rokk == 2024:
        cells.append(gspread.Cell(i, 7, '402-11-1'))
        cells.append(gspread.Cell(i, 8, '402-11-2'))
        cells.append(gspread.Cell(i, 9, '403-16-1'))
        cells.append(gspread.Cell(i, 10, '403-16-2'))
        cells.append(gspread.Cell(i, 11, '403-16-3'))
        cells.append(gspread.Cell(i, 12, '403-16-4'))
        cells.append(gspread.Cell(i, 13, '403-16-5'))
        cells.append(gspread.Cell(i, 14, '403-16-6'))
        cells.append(gspread.Cell(i, 15, '403-16-7'))

        #cells.append(gspread.Cell(i, 7, 'Premie\ni delegacje'))
        # cells.append(gspread.Cell(i, 17, 'Powierzchnia\nstoiska'))
        # cells.append(gspread.Cell(i, 18, 'Powierzchnia\npiętra'))
        # cells.append(gspread.Cell(i, 10, 'Delegacje'))
        cells.append(gspread.Cell(i, 17, 'Magazyn\ndrewna'))
        cells.append(gspread.Cell(i, 18, 'Magazyn\nwewnętrzny'))

        cells.append(gspread.Cell(i, 20, '[Delegacja]\nRóżnica'))
        cells.append(gspread.Cell(i, 21, '[Delegacja]\nWyjazd'))
        cells.append(gspread.Cell(i, 22, '[Pracownik]\nWyjazd'))
        cells.append(gspread.Cell(i, 23, '[Pracownik]\nPremia'))
    else:
        cells.append(gspread.Cell(i, 7, 'Premie\ni delegacje'))
        cells.append(gspread.Cell(i, 8, 'Powierzchnia\nstoiska'))
        cells.append(gspread.Cell(i, 9, 'Powierzchnia\npiętra'))
        cells.append(gspread.Cell(i, 10, 'Delegacje'))
        cells.append(gspread.Cell(i, 12, 'Magazyn\ndrewna'))
        cells.append(gspread.Cell(i, 13, 'Magazyn\nwewnętrzny'))
    i += 1
    for r in tab:
        cells.append(gspread.Cell(i, 1, r.nazwa))
        cells.append(gspread.Cell(i, 2, r.opis))
        cells.append(gspread.Cell(i, 3, r.targi))
        cells.append(gspread.Cell(i, 4, MtF(r.sum_direct)))
        cells.append(gspread.Cell(i, 5, MtF(r.sum_cash)))
        if rokk == 2023 or rokk == 2024:
            cells.append(gspread.Cell(i, 7, MtF(r.mpk_402111)))
            cells.append(gspread.Cell(i, 8, MtF(r.mpk_402112)))
            cells.append(gspread.Cell(i, 9, MtF(r.mpk_403161)))
            cells.append(gspread.Cell(i, 10, MtF(r.mpk_403162)))
            cells.append(gspread.Cell(i, 11, MtF(r.mpk_403163)))
            cells.append(gspread.Cell(i, 12, MtF(r.mpk_403164)))
            cells.append(gspread.Cell(i, 13, MtF(r.mpk_403165)))
            cells.append(gspread.Cell(i, 14, MtF(r.mpk_403166)))
            cells.append(gspread.Cell(i, 15, MtF(r.mpk_403167)))

            #cells.append(gspread.Cell(i, 7, MtF(r.sum_premie) + MtF(r.sum_deleg)))
            # cells.append(gspread.Cell(i, 17, r.pow_stoisko))
            # cells.append(gspread.Cell(i, 18, r.pow_pietra))
            # #cells.append(gspread.Cell(i, 10, MtF(r.deleg_sum)))
            cells.append(gspread.Cell(i, 17, MtF(r.magazyn_dre)))
            cells.append(gspread.Cell(i, 18, MtF(r.magazyn_wewn)))

            cells.append(gspread.Cell(i, 20, MtF(r.del_roznica)))
            cells.append(gspread.Cell(i, 21, MtF(r.del_wyjazd)))
            cells.append(gspread.Cell(i, 22, MtF(r.sum_deleg))) #deleg_sum
            cells.append(gspread.Cell(i, 23, MtF(r.sum_premie)))

            # cells.append(gspread.Cell(i, 12, MtF(r.mpk_402111)))
            # cells.append(gspread.Cell(i, 13, MtF(r.mpk_402112)))
            # cells.append(gspread.Cell(i, 14, MtF(r.mpk_403161)))
            # cells.append(gspread.Cell(i, 15, MtF(r.mpk_403162)))
            # cells.append(gspread.Cell(i, 16, MtF(r.mpk_403163)))
            # cells.append(gspread.Cell(i, 17, MtF(r.mpk_403164)))
            # cells.append(gspread.Cell(i, 18, MtF(r.mpk_403165)))
            # cells.append(gspread.Cell(i, 19, MtF(r.mpk_403166)))
            # cells.append(gspread.Cell(i, 20, MtF(r.mpk_403167)))
            #
            # cells.append(gspread.Cell(i, 7, MtF(r.sum_premie) + MtF(r.sum_deleg)))
            # cells.append(gspread.Cell(i, 8, r.pow_stoisko))
            # cells.append(gspread.Cell(i, 9, r.pow_pietra))
            # cells.append(gspread.Cell(i, 10, MtF(r.deleg_sum)))
            # cells.append(gspread.Cell(i, 22, MtF(r.magazyn_dre)))
            # cells.append(gspread.Cell(i, 23, MtF(r.magazyn_wewn)))



        else:
            cells.append(gspread.Cell(i, 7, MtF(r.sum_premie) + MtF(r.sum_deleg)))
            cells.append(gspread.Cell(i, 8, r.pow_stoisko))
            cells.append(gspread.Cell(i, 9, r.pow_pietra))
            cells.append(gspread.Cell(i, 10, MtF(r.deleg_sum)))
            cells.append(gspread.Cell(i, 12, MtF(r.magazyn_dre)))
            cells.append(gspread.Cell(i, 13, MtF(r.magazyn_wewn)))
        i += 1
    handler.update_cells(cells)


'''
 'Realizacja 2022', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'SDA [Koszty stałe]'
'''
def SDA_MPKtoGS(rokk, hn):
    crd = settings.GOOGLE_CRED
    #set_docs = settings.GOOGLE_DOCS_2022
    if rokk == 2022:
        set_docs = settings.GOOGLE_DOCS_2022
    elif rokk == 2023:
        set_docs = settings.GOOGLE_DOCS_2023
    elif rokk == 2024:
        set_docs = settings.GOOGLE_DOCS_2024

    fname = set_docs[2][0]
    file_key = set_docs[2][1]
    arkusz = set_docs[2][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = NrMPK.objects.filter(rok=rokk).order_by('id')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    about = settings.INFO_PROGRAM
    wersja = about[0].get("WERSJA")

    zc = "Ostatnia aktualizacja: " + dt + " [" + gd + "] ("+hn.upper()+"/SDA "+wersja+")"
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
        if rokk == 2022:
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
        else:
            if r.id not in LST_MPK_SDE:
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


'''
 'Realizacja 2022', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'REALIZACJA'
'''
def SDA_RealizacjaToGS(rokk, hn):
    crd = settings.GOOGLE_CRED
    #set_docs = settings.GOOGLE_DOCS_2022
    if rokk == 2022:
        set_docs = settings.GOOGLE_DOCS_2022
    elif rokk == 2023:
        set_docs = settings.GOOGLE_DOCS_2023
    fname = set_docs[4][0]
    file_key = set_docs[4][1]
    arkusz = set_docs[4][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = Podsumowanie.objects.filter(rok=rokk).order_by('miesiac')

    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    gd = datetime.datetime.now().strftime("%H:%M:%S")
    zc = "Ostatnia aktualizacja: " + dt + " [ " + gd + " ] ("+hn+")"
    cells = []
    i = 1
    cells.append(gspread.Cell(i, 1, zc))
    i += 5
    for r in tab:
        cells.append(gspread.Cell(i, 3, MtF(r.suma_biuro)))
        i += 1
    handler.update_cells(cells)


'''
 'Realizacja 2023', '1U_d-Xc_YiYrCklnRIfjlfb3hSaoqD634F9sOzhUhQv0', 'SDA [Pensje]'
'''
def SDA_PensjatoGS(rokk, hn):
    crd = settings.GOOGLE_CRED
    # set_docs = settings.GOOGLE_DOCS_2022
    if rokk == 2022:
        set_docs = settings.GOOGLE_DOCS_2022
    elif rokk == 2023:
        set_docs = settings.GOOGLE_DOCS_2023
    elif rokk == 2024:
        set_docs = settings.GOOGLE_DOCS_2024

    fname = set_docs[5][0]
    file_key = set_docs[5][1]
    arkusz = set_docs[5][2]
    handler = GetGStoWR(fname, file_key, arkusz, crd)

    tab = Pensja.objects.filter(rok=rokk, miesiac__gt=0).order_by('miesiac', 'osoba')
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    cz = datetime.datetime.now().strftime("%H:%M:%S")
    zc = "Ostatnia aktualizacja: "+dt+" [ "+cz+" ] ("+hn+")"

    cells = []
    i = 1

    if rokk == 2022:
        pass

    elif rokk == 2023:
        cells.append(gspread.Cell(i, 1, zc))
        i += 1
        cells.append(gspread.Cell(i, 1, 'Miesiąc'))
        cells.append(gspread.Cell(i, 2, 'Nazwisko i Imię'))
        cells.append(gspread.Cell(i, 3, 'Pensja'))
        cells.append(gspread.Cell(i, 4, 'PPK'))
        cells.append(gspread.Cell(i, 5, 'Przelew'))
        cells.append(gspread.Cell(i, 6, 'Obciążenia'))
        cells.append(gspread.Cell(i, 7, 'Różnica delegacji'))
        cells.append(gspread.Cell(i, 8, 'Wyjazd wartość'))
        cells.append(gspread.Cell(i, 9, 'Premia z SDA'))
        cells.append(gspread.Cell(i, 10, 'RAZEM'))
        for r in tab:
            i += 1
            cells.append(gspread.Cell(i, 1, LiczbaDoTekst(r.miesiac)))
            cells.append(gspread.Cell(i, 2, r.osoba))
            cells.append(gspread.Cell(i, 3, MtF(r.wynagrodzenie)))
            cells.append(gspread.Cell(i, 4, MtF(r.ppk)))
            cells.append(gspread.Cell(i, 5, MtF(r.przelew)))
            cells.append(gspread.Cell(i, 6, MtF(r.obciazenie)))
            cells.append(gspread.Cell(i, 7, MtF(r.del_rozli)))
            cells.append(gspread.Cell(i, 8, MtF(r.del_ilosc_razem)))
            cells.append(gspread.Cell(i, 9, MtF(r.premia)))
            cells.append(gspread.Cell(i, 10, MtF(r.razem)))

    handler.update_cells(cells)


# def LiczbaDoTekst(mc):
#     tmc = ''
#     if mc == 1:
#         tmc = 'Styczeń'
#     elif mc == 2:
#         tmc = 'Luty'
#     elif mc == 3:
#         tmc = 'Marzec'
#     elif mc == 4:
#         tmc = 'Kwiecień'
#     elif mc == 5:
#         tmc = 'Maj'
#     elif mc == 6:
#         tmc = 'Czerwiec'
#     elif mc == 7:
#         tmc = 'Lipiec'
#     elif mc == 8:
#         tmc = 'Sierpień'
#     elif mc == 9:
#         tmc = 'Wrzesień'
#     elif mc == 10:
#         tmc = 'Październik'
#     elif mc == 11:
#         tmc = 'Listopad'
#     elif mc == 12:
#         tmc = 'Grudzień'
#
#     return tmc
