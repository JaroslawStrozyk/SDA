from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from WORKER.views import CompareData
from .cron import SendData
from .functions import get_user_label
from .models import Log, URok, Ustawienia
from django.conf import settings
from django.contrib.auth.decorators import login_required
import datetime
from LOG.logs import TestLogs, InitLog, LogToFile


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
    return name_log, inicjaly


def start(request):
    return render(request, 'SDA/login.html', )


def refresh(request):

    return redirect('desktop')


@login_required(login_url='error')
def task(request):
    name_log, inicjaly = test_osoba(request)

    # Przełaczanie widoków
    hip = False
    usl = False
    mag = False
    tel = False
    rka = False
    fak = False
    ube = False
    dlg = False
    dow = False
    sam = False
    zam = False
    zal = False
    kod = False
    gog = False
    emp = False
    logs = False
    monit = False

    gr = ''
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        gr = g.name

    if gr == 'administrator':
        hip = True
        usl = True
        mag = True
        tel = True
        rka = True
        fak = True
        ube = True
        dlg = True
        dow = True
        sam = True
        zam = True
        zal = True
        kod = True
        gog = True
        emp = True
        logs = True
        monit = True
    elif gr == 'ksiegowosc':
        rka = True
        fak = True
        ube = True
        dlg = True
        dow = True
        zam = True
        zal = True
        kod = True
        gog = True
        emp = True
    elif gr == 'zksiegowosc':
        rka = True
        fak = True
        ube = True
        dlg = True
        dow = True
        zam = True
        zal = True
        kod = True
    elif gr == 'spedycja':
        sam = True
    elif gr == 'biuro':
        mag = True
        dow = True
        zam = True
        zal = True
        kod = True
    elif gr == 'biuro_1':
        dow = True
        zam = True
    elif gr == 'stolarnia':
        zal = True
        zam = True
    elif gr == 'produkcja':
        zal = True

    ur = URok.objects.filter(nazwa=inicjaly)
    if len(ur) == 0:
        URok.objects.create(nazwa=inicjaly, rok=datetime.datetime.now().strftime("%Y"))

    about = settings.INFO_PROGRAM
    set = Ustawienia.objects.all().order_by('co')

    return render(request, 'SDA/dashboard.html',
                  {
                      'name_log': get_user_label(request),
                      'date_log': request.user.last_login,
                      'hip': hip,
                      'usl': usl,
                      'mag': mag,
                      'tel': tel,
                      'rka': rka,
                      'fak': fak,
                      'ube': ube,
                      'dlg': dlg,
                      'dow': dow,
                      'sam': sam,
                      'zam': zam,
                      'zal': zal,
                      'kod': kod,
                      'gog': gog,
                      'emp': emp,
                      'logs': logs,
                      'monit': monit,
                      'about': about,
                      'set': set
                  })


def error(request):
    return render(request, 'SDA/404.html', )


def log(request):
    if request.user.is_authenticated:
        name_log = get_user_label(request)
        lista_logi = Log.objects.all().order_by('-data')

        paginator = Paginator(lista_logi, 50)
        strona = request.GET.get('page')
        logi = paginator.get_page(strona)

        return render(request, 'SDA/log.html', {'name_log': name_log, 'logi': logi})
    else:
        return redirect('error')
