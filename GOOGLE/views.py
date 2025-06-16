from django.shortcuts import render, redirect
from ORDERS.models import NrSDE, NrMPK, Zamowienie
from CASH_ADVANCES.models import Pozycja
from django.contrib.auth.decorators import login_required
from django.conf import settings

from SDA.settings import LST_MPK_SDE
from TaskAPI.models import Rok, URok, Waluta
from django.contrib.auth.models import Group
from moneyed import Money, PLN


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
def gog_start(request):
    lata, rok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    if rok == 2021:
        tytul = settings.GOOGLE_DOCS_2021[0][3]
    elif rok == 2022:
        tytul = settings.GOOGLE_DOCS_2022[0][3]
    elif rok == 2023:
        tytul = settings.GOOGLE_DOCS_2023[0][3]
    elif rok == 2024:
        tytul = settings.GOOGLE_DOCS_2024[0][3]
    elif rok == 2025:
        tytul = settings.GOOGLE_DOCS_2025[0][3]

    sde = NrSDE.objects.filter(rokk=rok).order_by('-nazwa_id')

    return render(request, 'GOOGLE/gog_main.html', {
        'sde': sde,
        'tytul_tabeli': tytul,
        'name_log': name_log,
        'admini': test_admin(request),
        'about': about,
    })


@login_required(login_url='error')
def gog_kp(request):
    lata, rok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul = "Nie przesyłane !!!"
    if rok == 2021:
        tytul = settings.GOOGLE_DOCS_2021[1][3]
    elif rok == 2022:
        tytul =  settings.GOOGLE_DOCS_2022[1][3]
    elif rok == 2023:
        tytul = settings.GOOGLE_DOCS_2023[1][3]
    elif rok == 2024:
        tytul = settings.GOOGLE_DOCS_2024[1][3]

    nrsde = NrSDE.objects.filter(rokk=rok).order_by('-nazwa_id')
    tzero = Money('00.00', PLN)
    zero = 0

    temp_file = 'GOOGLE/gog_kp.html'
    return render(request, temp_file, {
        'nrsde': nrsde,
        'tzero': tzero,
        'zero': zero,
        'tytul_tabeli': tytul,
        'name_log': name_log,
        'admini': test_admin(request),
        'about': about,
    })

@login_required(login_url='error')
def gog_kp_det(request,pk):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tzero = Money('00.00', PLN)
    tzero_curr = tzero.currency

    sde = NrSDE.objects.get(pk=pk)
    zlecenie = sde.nazwa
    suma  = sde.sum_cash
    opis = sde.opis
    #
    # print(">>>", pk, sde.nazwa, sde.sum_cash)
    zam_dane = Pozycja.objects.filter(nr_sde_id__nazwa=zlecenie)
    # for d in dane:
    #     print(d.opis, d.kwota_netto, d.kwota_netto_pl)
    #return redirect('gog_kp')
    return render(request, 'GOOGLE/gog_kpd.html', {
        'zlecenie': zlecenie,
        'opis': opis,
        'suma': suma,
        'zam_dane': zam_dane,
        'tzero': tzero,
        'tzero_curr': tzero_curr,
        'name_log': name_log,
        'admini': test_admin(request),
        'about': about,
    })




#@login_required(login_url='error')
# def gog_kbp(request):
#     lata, rok = test_rok(request)
#     name_log, inicjaly = test_osoba(request)
#     about = settings.INFO_PROGRAM
#     tytul = 'Zamówienia SDE ⇨ ? [SDE z 2020 płacone w 2021]'
#
#     nrsde = NrSDE.objects.filter(rokk=rok - 1).order_by('-nazwa_id')
#     tzero = Money('00.00', PLN)
#
#     return render(request, 'GOOGLE/gog_kbp.html', {
#         'nrsde': nrsde,
#         'tzero': tzero,
#         'tytul_tabeli': tytul,
#         'name_log': name_log,
#         'admini': test_admin(request),
#         'about': about,
#     })
#
#
# @login_required(login_url='error')
# def gog_kg(request):
#     lata, rok = test_rok(request)
#     name_log, inicjaly = test_osoba(request)
#     about = settings.INFO_PROGRAM
#
#     if rok == 2021:
#         tytul = settings.GOOGLE_DOCS_2021[1][3]
#     elif rok == 2022:
#         tytul =  settings.GOOGLE_DOCS_2022[1][3]
#
#     nrsde = NrSDE.objects.filter(rokk=rok).order_by('-nazwa_id')
#     tzero = Money('00.00', PLN)
#     if rok < 2022:
#         temp_file = 'GOOGLE/gog_kg.html'
#     else:
#         temp_file = 'GOOGLE/gog_nkg.html'
#     return render(request, temp_file, {
#         'nrsde': nrsde,
#         'tzero': tzero,
#         'tytul_tabeli': tytul,
#         'name_log': name_log,
#         'admini': test_admin(request),
#         'about': about,
#     })

# @login_required(login_url='error')
# def gog_kgp(request):
#     lata, rok = test_rok(request)
#     name_log, inicjaly = test_osoba(request)
#     about = settings.INFO_PROGRAM
#     tytul = 'Zaliczki SDE ⇨ ? [SDE z 2020 płacone w 2021]'
#
#     nrsde = NrSDE.objects.filter(rokk=rok-1).order_by('-nazwa_id')
#     tzero = Money('00.00', PLN)
#
#     return render(request, 'GOOGLE/gog_kgp.html', {
#         'nrsde': nrsde,
#         'tzero': tzero,
#         'tytul_tabeli': tytul,
#         'name_log': name_log,
#         'admini': test_admin(request),
#         'about': about,
#     })


@login_required(login_url='error')
def gog_ks(request):
    lata, rok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    #lst = [210, 211, 240, 241, 242, 243, 244, 245, 246]
    tytul = "Nie przesyłane !!!"

    if rok == 2021:
        tytul = settings.GOOGLE_DOCS_2021[1][3]
    elif rok == 2022:
        tytul =  settings.GOOGLE_DOCS_2022[2][3]
    elif rok == 2023:
        tytul =  settings.GOOGLE_DOCS_2023[2][3]
    elif rok == 2024:
        tytul =  settings.GOOGLE_DOCS_2024[2][3]

    nrmpk = NrMPK.objects.filter(rok=rok).order_by('id')
    tzero = Money('00.00', PLN)
    for mpk in nrmpk:
        mpk.suma = mpk.sum_zal + mpk.sum_zam
        mpk.save()

    return render(request, 'GOOGLE/gog_ks.html', {
        'nrmpk': nrmpk,
        'lst': LST_MPK_SDE,
        'tzero': tzero,
        'tytul_tabeli': tytul,
        'name_log': name_log,
        'admini': test_admin(request),
        'about': about,
    })


# @login_required(login_url='error')
# def gog_ksp(request):
#     lata, rok = test_rok(request)
#     name_log, inicjaly = test_osoba(request)
#     about = settings.INFO_PROGRAM
#     tytul = 'Zamówienia + Zaliczki MPK ⇨ ? [SDE z 2020 płacone w 2021]'
#
#     nrmpk = NrMPK.objects.filter(rok=rok-1).order_by('nazwa')
#     tzero = Money('00.00', PLN)
#     for mpk in nrmpk:
#         mpk.suma = mpk.sum_zal + mpk.sum_zam
#         mpk.save()
#
#     return render(request, 'GOOGLE/gog_ksp.html', {
#         'nrmpk': nrmpk,
#         'tzero': tzero,
#         'tytul_tabeli': tytul,
#         'name_log': name_log,
#         'admini': test_admin(request),
#         'about': about,
#     })
