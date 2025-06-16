from simple_search import search_filter
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ORDERS.functions import test_osoba
from django.conf import settings

from SDA.settings import LOG_FILE
from .logs import LogToFile
from .models import LogSystem
from django.http import JsonResponse, HttpResponse
import os

def list_logs(request):
    def build_tree(root_path):
        tree = {}
        for root, dirs, files in os.walk(root_path):
            relative_path = os.path.relpath(root, root_path)
            if relative_path == '.':
                relative_path = ''
            sub_tree = tree.setdefault(relative_path, {})
            for dir_name in dirs:
                sub_tree[dir_name] = {}
            for file_name in files:
                if file_name.endswith(".log"):
                    sub_tree[file_name] = None
        return tree

    logs_tree = build_tree(LOG_FILE)
    return JsonResponse({'logs': logs_tree})

def get_log_content(request):
    log_file = request.GET.get('file', None)
    if log_file:
        full_path = os.path.join(LOG_FILE, log_file)
        if os.path.exists(full_path):
            with open(full_path, 'r') as file:
                content = file.read()
            return JsonResponse({'file': log_file, 'content': content})
    return JsonResponse({'error': 'File not found'}, status=404)


@login_required(login_url='error')
def log(request):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul = "Log systemu SDA"

    log_tab = LogSystem.objects.all().exclude(status_id=-1).order_by('-data','-godz')

    return render(request, 'LOG/log.html', {
        'log_tab': log_tab,
        'name_log': name_log,
        'about': about,
        'tytul': tytul
    })

@login_required(login_url='error')
def log_arch(request):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul = "Archiwalny log SDA"

    return render(request, 'LOG/log_arch.html', {
        'name_log': name_log,
        'about': about,
        'tytul': tytul
    })




def get_logs(request):
    data = []
    logs = LogSystem.objects.all().exclude(status_id=-1).order_by('-data','-godz')
    for l in logs:
        row = {}
        row["status_id"] = l.status_id
        row["status"] = l.status
        row["data"] = str(l.data)
        row["godz"] = str(l.godz)
        row["modul"] = l.modul.nazwa
        row["komunikat"] = l.komunikat.nazwa
        row["opis"] = l.opis #.split('Czas')[0]
        # try:
        #     out = l.opis.split('Czas')[1].split(':')[1].strip().split(' ')[0].strip()
        # except:
        #     out = ''
        row["czas"] = l.czas #out
        row["kto"] = l.kto
        data.append(row)

    return JsonResponse(data, safe=False)


@login_required(login_url='error')
def log_all(request):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    log_tab = LogSystem.objects.all().exclude(status_id=-1).order_by('-data','-godz')
    lprows = len(LogSystem.objects.all().filter(status_id=-1))
    lcrows = len(LogSystem.objects.all())
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
    log_tab = LogSystem.objects.filter(kto='sda').order_by('-data','-godz')
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
    log_tab = LogSystem.objects.all().exclude(kto='sda').exclude(status_id=-1).order_by('-data','-godz')
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
        log_tab = LogSystem.objects.filter(f).exclude(status_id=-1)
        tytul = "Logi, szukasz: "+query

        return render(request, 'LOG/log_all.html', {
            'log_tab': log_tab,
            'name_log': name_log,
            'about': about,
            'tytul': tytul
        })
    else:
        return redirect('log_all')


@login_required(login_url='error')
def log_create(request):
    LogToFile()
    return redirect('log_arch')

