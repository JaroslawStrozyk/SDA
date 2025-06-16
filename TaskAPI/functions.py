import datetime





# from RK.models import Waluta

from django.core.mail import EmailMessage
from django.conf import settings

from ORDERS.models import NrSDE
#from .models import Log

#import requests

from django.db import connection


# def do_logu(modul, usr,uwagi):
#     dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     tb = Log(data=dt, modul=modul, usr=usr, uwagi=uwagi)
#     tb.save()

def get_user_label(request):
    return request.user.first_name + " " + request.user.last_name

# def email_from_targi(subject, message):
#     sender = settings.EMAIL_HOST_USER
#     to_send = ['dace@smartdesign-expo.com', ]
#     msg = EmailMessage(subject, message, sender, to_send)
#     msg.content_subtype = "html"
#     msg.send()



def trans_month(amc):
    pmc = ''
    if amc == 'January':
        pmc = 'Styczeń'
    if amc == 'February':
        pmc = 'Luty'
    if amc == 'March':
        pmc = 'Marzec'
    if amc == 'April':
        pmc = 'Kwiecień'
    if amc == 'May':
        pmc = 'Maj'
    if amc == 'June':
        pmc = 'Czerwiec'
    if amc == 'July':
        pmc = 'Lipiec'
    if amc == 'August':
        pmc = 'Sierpień'
    if amc == 'September':
        pmc = 'Wrzesień'
    if amc == 'October':
        pmc = 'Październik'
    if amc == 'November':
        pmc = 'Listopad'
    if amc == 'December':
        pmc = 'Grudzień'
    return pmc


def intstr_month(amc):
    pmc = ''
    if amc == '01':
        pmc = 'Styczeń'
    if amc == '02':
        pmc = 'Luty'
    if amc == '03':
        pmc = 'Marzec'
    if amc == '04':
        pmc = 'Kwiecień'
    if amc == '05':
        pmc = 'Maj'
    if amc == '06':
        pmc = 'Czerwiec'
    if amc == '07':
        pmc = 'Lipiec'
    if amc == '08':
        pmc = 'Sierpień'
    if amc == '09':
        pmc = 'Wrzesień'
    if amc == '10':
        pmc = 'Październik'
    if amc == '11':
        pmc = 'Listopad'
    if amc == '12':
        pmc = 'Grudzień'

    if amc == '1':
        pmc = 'Styczeń'
    if amc == '2':
        pmc = 'Luty'
    if amc == '3':
        pmc = 'Marzec'
    if amc == '4':
        pmc = 'Kwiecień'
    if amc == '5':
        pmc = 'Maj'
    if amc == '6':
        pmc = 'Czerwiec'
    if amc == '7':
        pmc = 'Lipiec'
    if amc == '8':
        pmc = 'Sierpień'
    if amc == '9':
        pmc = 'Wrzesień'
    if amc == '10':
        pmc = 'Październik'
    if amc == '11':
        pmc = 'Listopad'
    if amc == '12':
        pmc = 'Grudzień'
    return pmc


def TestData(ind, sh, koniecl, sprzedany, arch, p_l):
    out = 0
    if sprzedany==False and arch==False:

        dtnow = datetime.datetime.now()
        dtin = datetime.datetime.strptime(ind, '%Y-%m-%d')
        shift = datetime.timedelta(days=sh)
        dttest = dtnow + shift

        if dtin > dttest:
            out = 0
        if dtin < dttest and dtin > dtnow:
            out = 1
        if dtin < dtnow:
            out = 2

        if p_l==True and koniecl==True:
            out = 0
    return out


def TestDataT(ind, sh, koniecl, sprzedany, arch, p_l):
    out = 0
    if sprzedany==False and arch==False:
        try:
            dtnow = datetime.datetime.now()
            dtin = datetime.datetime.strptime(ind, '%Y-%m-%d')
            shift = datetime.timedelta(days=sh)
            dttest = dtnow + shift

            if dtin > dttest:
                out = 1
            if dtin < dttest and dtin > dtnow:
                out = 2
            if dtin < dtnow:
                out = 3

            if p_l==True and koniecl==True:
                out = 0
        except:
            out=0

    return out



def pobierz_Dane(kod):
    print (kod)


def TestDataUslugi(ind, sh):
    out = 0

    dtnow = datetime.datetime.now()
    dtin = datetime.datetime.strptime(ind, '%Y-%m-%d')
    shift = datetime.timedelta(days=sh)
    dttest = dtnow + shift

    if dtin > dttest:
        out = 1
    if dtin < dttest and dtin > dtnow:
        out = 2
    if dtin < dtnow:
        out = 3

    return out


def upgrade_sum_SDA():
    for nr in NrSDE.objects.all():
        s1 = nr.sum_premie
        s2 = nr.sum_deleg
        nr.sum_pre_del = s1 + s2
        nr.save()


def LiczbaDoTekst(mc):
    tmc = ''
    if mc == 1:
        tmc = 'Styczeń'
    elif mc == 2:
        tmc = 'Luty'
    elif mc == 3:
        tmc = 'Marzec'
    elif mc == 4:
        tmc = 'Kwiecień'
    elif mc == 5:
        tmc = 'Maj'
    elif mc == 6:
        tmc = 'Czerwiec'
    elif mc == 7:
        tmc = 'Lipiec'
    elif mc == 8:
        tmc = 'Sierpień'
    elif mc == 9:
        tmc = 'Wrzesień'
    elif mc == 10:
        tmc = 'Październik'
    elif mc == 11:
        tmc = 'Listopad'
    elif mc == 12:
        tmc = 'Grudzień'

    return tmc
