from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from TaskAPI.models import Rok, URok, Waluta
from django.contrib.auth.models import Group



def test_admin(request):
    gr = ''
    admini = False
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        gr = g.name
        # grupy: 	administrator, ksiegowosc, zksiegowosc, spedycja, biuro
    if gr == 'administrator':
        admini = True
    return admini


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
    return lata, rok


@login_required(login_url='error')
def logs_start(request):
    lata, rok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    tytul_tabeli = "Zestawienie kursów walut"
    about = settings.INFO_PROGRAM
    #wal = Waluta.objects.all().order_by('kod','-data')
    wal1 = Waluta.objects.filter(kod='EUR').order_by('-data')
    wal2 = Waluta.objects.filter(kod='GBP').order_by('-data')
    wal3 = Waluta.objects.filter(kod='USD').order_by('-data')
    wal4 = Waluta.objects.filter(kod='CHF').order_by('-data')
    cron = settings.CRONJOBS

    lwal = settings.GET_NBP
    s = ""
    for l in lwal:
        s = s + l + ", "
    lwal = s[:-2]

    ldni = settings.HIS_NBP

    gt = ''

    for c in cron:
        if c[1] == "TaskAPI.cron.GetNBP":
            t = c[0].split(' ')
            gt = "Godzina: "+t[1]+":"+t[0]+", Dzień miesiąca: każdy, Miesiąc: każdy, Dzień tygodnia: każdy "


    return render(request, 'MONIT/main.html',
                  {
                      'tytul_tabeli': tytul_tabeli,
                      'name_log': name_log,
                      'about': about,
                      'lwal': lwal,
                      'ldni': ldni,
                      'wal1' : wal1,
                      'wal2': wal2,
                      'wal3': wal3,
                      'wal4': wal4,
                      'gt': gt
                  })

@login_required(login_url='error')
def logs_startp(request):
    lata, rok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    tytul_tabeli = "Zestawienie kursów walut"
    about = settings.INFO_PROGRAM

    cron = settings.CRONJOBS

    lwal = settings.GET_NBP
    s = ""
    for l in lwal:
        s = s + l + ", "
    lwal = s[:-2]

    ldni = settings.HIS_NBP


    mp = settings.DELEGATIONS_TO_TARGET
    if mp == 1:
        m_p = "SKYPE"
    else:
        m_p = "E-MAIL"

    a_s = settings.DEL_SKYPE_DO_USERS
    s = ""
    for l in a_s:
        s = s + l + ", "
    a_s = s[:-2]

    a_e = settings.DEL_EMAIL_DO_USERS
    s = ""
    for l in a_e:
        s = s + l + ", "
    a_e = s[:-2]

    mp = settings.INVOICES_TO_TARGET
    if mp == 1:
        m_pf = "SKYPE"
    else:
        m_pf = "E-MAIL"

    a_sf = settings.INV_SKYPE_DO_USERS
    s = ""
    for l in a_sf:
        s = s + l + ", "
    a_sf = s[:-2]

    a_ef = settings.INV_EMAIL_DO_USERS
    s = ""
    for l in a_ef:
        s = s + l + ", "
    a_ef = s[:-2]

    mp = settings.CARS_TO_TARGET
    if mp == 1:
        m_ps = "SKYPE"
    else:
        m_ps = "E-MAIL"

    a_ss = settings.CARS_SKYPE_DO_USERS
    s = ""
    for l in a_ss:
        s = s + l + ", "
    a_ss = s[:-2]

    a_es = settings.CARS_EMAIL_DO_USERS
    s = ""
    for l in a_es:
        s = s + l + ", "
    a_es = s[:-2]

    w_pb = str(settings.CARS_DATE_SHIFT) + " dni"
    w_tl = str(settings.CARS_LEASING_SHIFT) + " dni"

    lws = str(settings.PAGIN_PAGE)

    if settings.SIMPLE_VIEW == True:
        tu = "Włączony"
    else:
        tu = "Wyłaczone"


    gt = ""
    for c in cron:
        if c[1] == "TaskAPI.cron.GetNBP":
            t = c[0].split(' ')
            gt = "Godzina: "+t[1]+":"+t[0]+", Dzień miesiąca: każdy, Miesiąc: każdy, Dzień tygodnia: każdy "


    return render(request, 'MONIT/mainp.html',
                  {
                      'tytul_tabeli': tytul_tabeli,
                      'name_log': name_log,
                      'about': about,
                      'lwal': lwal,
                      'ldni': ldni,
                      'gt': gt,
                      'm_p': m_p,
                      'a_s': a_s,
                      'a_e' : a_e,
                      'm_pf': m_pf,
                      'a_sf': a_sf,
                      'a_ef': a_ef,
                      'm_ps': m_ps,
                      'a_ss': a_ss,
                      'a_es': a_es,
                      'w_pb': w_pb,
                      'w_tl': w_tl,
                      'lws' : lws,
                      'tu'  : tu
                  })