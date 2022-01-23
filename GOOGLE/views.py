from django.shortcuts import render
from ORDERS.models import NrSDE, NrMPK
from django.contrib.auth.decorators import login_required
from django.conf import settings
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
    if rok == 2021:
        tytul = settings.GOOGLE_DOCS_2021[1][3]
    elif rok == 2022:
        tytul =  settings.GOOGLE_DOCS_2022[1][3]

    nrsde = NrSDE.objects.filter(rokk=rok).order_by('-nazwa_id')
    tzero = Money('00.00', PLN)
    # if rok < 2022:
    #     temp_file = 'GOOGLE/gog_kb.html'
    # else:
    #     temp_file = 'GOOGLE/gog_kp.html'
    temp_file = 'GOOGLE/gog_kp.html'
    return render(request, temp_file, {
        'nrsde': nrsde,
        'tzero': tzero,
        'tytul_tabeli': tytul,
        'name_log': name_log,
        'admini': test_admin(request),
        'about': about,
    })



    # if rok < 2022:
    #     return render(request, 'GOOGLE/gog_kb.html', {
    #         'nrsde': nrsde,
    #         'tzero': tzero,
    #         'tytul_tabeli': tytul,
    #         'name_log': name_log,
    #         'admini': test_admin(request),
    #         'about': about,
    #     })
    # else:
    #     return render(request, 'GOOGLE/gog_nkb.html', {
    #         'nrsde': nrsde,
    #         'tzero': tzero,
    #         'tytul_tabeli': tytul,
    #         'name_log': name_log,
    #         'admini': test_admin(request),
    #         'about': about,
    #     })


@login_required(login_url='error')
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

    if rok == 2021:
        tytul = settings.GOOGLE_DOCS_2021[1][3]
    elif rok == 2022:
        tytul =  settings.GOOGLE_DOCS_2022[2][3]


    nrmpk = NrMPK.objects.filter(rok=rok).order_by('nazwa')
    tzero = Money('00.00', PLN)
    for mpk in nrmpk:
        mpk.suma = mpk.sum_zal + mpk.sum_zam
        mpk.save()

    return render(request, 'GOOGLE/gog_ks.html', {
        'nrmpk': nrmpk,
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