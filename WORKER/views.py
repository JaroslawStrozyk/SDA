from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .functions import test_osoba, test_rok
from .models import Pracownik


@login_required(login_url='error')
def worker_start(request):
    lata, rok, brok, bmc = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM

    return render(request, 'WORKER/main_g.html', {
        'name_log': name_log,
        'about': about,
    })


@login_required(login_url='error')
def worker_pr(request):
    lata, rok, brok, bmc = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul_tabeli = 'Pracownicy'

    prac = Pracownik.objects.all().order_by()

    return render(request, 'WORKER/pracownik.html', {
        'name_log': name_log,
        'about': about,
        'tytul_tabeli': tytul_tabeli,
        'pracownik': prac

    })


@login_required(login_url='error')
def worker_mc(request):
    lata, rok, brok, bmc = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul_tabeli = 'Brak danych'
    bd = True
    mc_rok = str(bmc)+"-"+str(rok)

    return render(request, 'WORKER/miesiac.html', {
        'name_log': name_log,
        'about': about,
        'tytul_tabeli': tytul_tabeli,
        'brak_danych': bd,
        'mc_rok': mc_rok,
        'brok': brok,
        'bmc': bmc
    })


def gen_mc(request, bmc, brok):
    print(" >>> ", str(bmc), str(brok))
    return redirect('worker_mc')


def gen_staz(request):
    print(" >>> GEN STAŻ !!!")
    print(20/12)
    return redirect('worker_pr')