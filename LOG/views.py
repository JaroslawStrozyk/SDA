from simple_search import search_filter
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ORDERS.functions import test_osoba
from django.conf import settings
from .models import Log


@login_required(login_url='error')
def log_all(request):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    log_tab = Log.objects.all().exclude(status_id=-1).order_by('-data','-godz')
    lprows = len(Log.objects.all().filter(status_id=-1))
    lcrows = len(Log.objects.all())
    lrows = len(log_tab)
    tytul = "Ogólny Log"

    return render(request, 'LOG/log_all.html', {
        'log_tab': log_tab,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'lrows': lrows,
        'lprows': lprows,
        'lcrows': lcrows
    })


@login_required(login_url='error')
def log_tech(request):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    log_tab = Log.objects.filter(kto='sda').order_by('-data','-godz')
    tytul = "Log techniczny"

    return render(request, 'LOG/log_tech.html', {
        'log_tab': log_tab,
        'name_log': name_log,
        'about': about,
        'tytul': tytul
    })


@login_required(login_url='error')
def log_oper(request):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    log_tab = Log.objects.all().exclude(kto='sda').exclude(status_id=-1).order_by('-data','-godz')
    tytul = "Log operacyjny"

    return render(request, 'LOG/log_oper.html', {
        'log_tab': log_tab,
        'name_log': name_log,
        'about': about,
        'tytul': tytul
    })

'''
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    log_tab = Log.objects.all().exclude(status_id=-1).order_by('-data','-godz')
    tytul = "Ogólny Log"

    return render(request, 'LOG/log_all.html', {
        'log_tab': log_tab,
        'name_log': name_log,
        'about': about,
        'tytul': tytul
    })
'''

@login_required(login_url='error')
def log_search(request):
    if request.method == "GET":
        name_log, inicjaly = test_osoba(request)
        about = settings.INFO_PROGRAM
        #log_tab = Log.objects.all().exclude(status_id=-1)


        query = request.GET['SZUKAJ']

        if query == '' or query == ' ':
            return redirect('log_all')
        search_fields = ['data', 'godz', 'modul__nazwa', 'komunikat__nazwa', 'opis', 'kto' ]
        f = search_filter(search_fields, query)
        log_tab = Log.objects.filter(f).exclude(status_id=-1)
        tytul = "Logi, szukasz: "+query

        return render(request, 'LOG/log_all.html', {
            'log_tab': log_tab,
            'name_log': name_log,
            'about': about,
            'tytul': tytul
        })
    else:
        return redirect('log_all')