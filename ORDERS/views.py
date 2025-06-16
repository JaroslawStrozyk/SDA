import decimal
from datetime import datetime
from LOG.logs import logi_order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from simple_search import search_filter
from .models import Zamowienie, NrSDE, NrMPK, FlagaSzukania
from .forms import ZamowienieForm, NrSDEForm, ZamowienieFormM
from moneyed import Money, PLN, CURRENCIES
from TaskAPI.models import URok
from django.core.paginator import Paginator
from .pdf import out_pdf_sde, out_pdf_ord
from .xls import gen_xls, out_xls_ord, out_csv_ord, out_xls_sde
from .functions import test_admin, test_osoba, test_osoba1, test_rok, testQuery, suma_wartosci, CalcCurrency
from .functions import TestValidate, DecodeSlash, CodeSlash
from SDA.settings import PAGIN_PAGE
from django.contrib.auth.models import Group

from django.http import JsonResponse
from .models import Nip
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def get_nip_details(request):

    nip_ind = request.GET.get('nip_ind', None)
    details = Nip.objects.filter(id=nip_ind).values('nip', 'kontrahent').first()

    if details:
        return JsonResponse(details)
    else:
        return JsonResponse({"error": "Nie znaleziono danych"}, status=404)


@csrf_exempt
def add_nip(request):
    new_nip = request.POST.get('nip')
    new_kontrahent = request.POST.get('kontrahent')

    new_entry = Nip.objects.create(nip=new_nip, kontrahent=new_kontrahent)
    new_entry.save()

    return JsonResponse({"new_nip_ind": new_entry.id})


def top_user(request):
    admini = False
    name_log, inicjaly = test_osoba(request)
    gr = str(Group.objects.filter(user=request.user).first())
    if gr == 'administrator' or gr == 'ksiegowosc' or gr == 'ksiegowosc1' or inicjaly == 'M.J.' or inicjaly == 'P.P.' or inicjaly == 'A.N.' or inicjaly == 'J.W.':
        admini = True
    return admini


def select_zam_via_user(req, rok, inicjaly):
    # lata, rok, brok = test_rok(req)
    # name_log, inicjaly = test_osoba(req)
    top_us = top_user(req)
    if top_us:
        zamowienia = Zamowienie.objects.filter(rokk=rok, roz=False).order_by('-pk')
    else:
        zamowienia = Zamowienie.objects.filter(rokk=rok, roz=False, inicjaly=inicjaly).order_by('-pk')
    return zamowienia


@login_required(login_url='error')
def order_start(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    tytul1 = 'Lista zamówień '
    tytul2 = str(rok)
    tytul3 = ''

    zamowienia = select_zam_via_user(request, rok, inicjaly)

    tzero = Money('00.00', PLN).amount
    nrsde = NrSDE.objects.all().order_by('nazwa')
    nr_sde = NrSDE.objects.filter(rok=rok).order_by('nazwa')
    nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')

    SDE_None = None

    paginator = Paginator(zamowienia, PAGIN_PAGE)
    strona = request.GET.get('page')
    pzamowienia = paginator.get_page(strona)

    return render(request, 'ORDERS/ord_main.html', {
        'zamowienia': pzamowienia,
        'name_log': name_log,
        'tytul_tabeli1': tytul1,
        'tytul_tabeli2': tytul2,
        'tytul_tabeli3': tytul3,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'tzero': tzero,
        'nrsde': nrsde,
        'nr_sde': nr_sde,
        'nrmpk': nrmpk,
        'SDE_None': SDE_None,
        'suma': 0,
        'szukanie': False,
        'src': '^',
        'fl' : 'main',
        'main': True,
        'search': False,
        'mpk': False,
        'sde': False,
        'b_rok': b_rok
    })


@login_required(login_url='error')
def order_start_all(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    top_us = top_user(request)
    about = settings.INFO_PROGRAM

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    tytul1 = 'Lista zamówień [wszystkie] '
    tytul2 = str(rok)
    tytul3 = ''

    if top_us:
        zamowienia = Zamowienie.objects.filter(rokk=rok).order_by('-pk')
    else:
        zamowienia = Zamowienie.objects.filter(rokk=rok, inicjaly=inicjaly).order_by('-pk') #, inicjaly=inicjaly

    #zamowienia = select_zam_via_user(request, rok, inicjaly)

    tzero = Money('00.00', PLN).amount
    nrsde = NrSDE.objects.all().order_by('nazwa')
    nr_sde = NrSDE.objects.filter(rok=rok).order_by('nazwa')
    nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')

    SDE_None = None

    paginator = Paginator(zamowienia, PAGIN_PAGE)
    strona = request.GET.get('page')
    pzamowienia = paginator.get_page(strona)

    return render(request, 'ORDERS/ord_main.html', {
        'zamowienia': pzamowienia,
        'name_log': name_log,
        'tytul_tabeli1': tytul1,
        'tytul_tabeli2': tytul2,
        'tytul_tabeli3': tytul3,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'tzero': tzero,
        'nrsde': nrsde,
        'nr_sde': nr_sde,
        'nrmpk': nrmpk,
        'SDE_None': SDE_None,
        'suma': 0,
        'szukanie': False,
        'src': '^',
        'fl' : 'main',
        'main': True,
        'search': False,
        'mpk': False,
        'sde': False,
        'b_rok': b_rok
    })

# API
@login_required(login_url='error')
def ord_setting(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM

    flagi = FlagaSzukania.objects.all()

    return render(request, 'ORDERS/ord_set.html', {
        'name_log': name_log,
        'about': about,
        'flagi': flagi,
    })


def lista_flag(request):
    flagi = FlagaSzukania.objects.all()
    return JsonResponse({'flagi': [{'id': f.id, 'nazwa': f.nazwa, 'uwagi': f.uwagi} for f in flagi]})


def dodaj_flag(request):
    if request.method == 'POST':
        nazwa = request.POST['nazwa']
        uwagi = request.POST['uwagi']
        flaga = FlagaSzukania.objects.create(nazwa=nazwa, uwagi=uwagi)
        return JsonResponse({'id': flaga.id, 'nazwa': flaga.nazwa, 'uwagi': flaga.uwagi})


def edytuj_flag(request, id):
    flaga = get_object_or_404(FlagaSzukania, pk=id)

    if request.method == 'POST':
        flaga.nazwa = request.POST['nazwa']
        flaga.uwagi = request.POST['uwagi']
        flaga.save()
        return JsonResponse({'id': flaga.id, 'nazwa': flaga.nazwa, 'uwagi': flaga.uwagi})
    else:
        # Dodajemy obsługę żądania GET, aby zwrócić dane flagi w formacie JSON
        return JsonResponse({'id': flaga.id, 'nazwa': flaga.nazwa, 'uwagi': flaga.uwagi})


def usun_flag(request, id):
    flaga = get_object_or_404(FlagaSzukania, pk=id)
    if request.method == 'POST':
        flaga.delete()
        return JsonResponse({'deleted': True})

# # Widok do pobierania listy flag (operacja Read)
# def lista_flag(request):
#     if request.method == 'GET':
#         flagi = FlagaSzukania.objects.all()
#         data = [{'id': flaga.id, 'nazwa': flaga.nazwa, 'uwagi': flaga.uwagi} for flaga in flagi]
#         return JsonResponse(data, safe=False)

# # Widok do tworzenia nowej flagi (operacja Create)
# @csrf_exempt
# def dodaj_flag(request):
#     if request.method == 'POST':
#         nazwa = request.POST.get('nazwa')
#         uwagi = request.POST.get('uwagi', '')
#
#         flaga = FlagaSzukania(nazwa=nazwa, uwagi=uwagi)
#         flaga.save()
#
#         flagi = FlagaSzukania.objects.all()
#         data = [{'id': flaga.id, 'nazwa': flaga.nazwa, 'uwagi': flaga.uwagi} for flaga in flagi]
#         return JsonResponse(data, safe=False)
#
# # Widok do pobierania danych flagi (operacja Read)
# def pobierz_flag(request, pk):
#     flaga = FlagaSzukania.objects.get(pk=pk)
#     data = {'id': flaga.id, 'nazwa': flaga.nazwa, 'uwagi': flaga.uwagi}
#     return JsonResponse(data)
#
#
# # Widok do aktualizacji flagi (operacja Update)
# @csrf_exempt
# def edytuj_flag(request, pk):
#     if request.method == 'POST':
#         flaga = FlagaSzukania.objects.get(pk=pk)
#         flaga.nazwa = request.POST.get('nazwa')
#         flaga.uwagi = request.POST.get('uwagi', '')
#         flaga.save()
#
#         flagi = FlagaSzukania.objects.all()
#         data = [{'id': flaga.id, 'nazwa': flaga.nazwa, 'uwagi': flaga.uwagi} for flaga in flagi]
#         return JsonResponse(data, safe=False)
#
# # Widok do usuwania flagi (operacja Delete)
# @csrf_exempt
# def usun_flag(request, pk):
#     if request.method == 'DELETE':
#         flaga = FlagaSzukania.objects.get(pk=pk)
#         flaga.delete()
#
#         flagi = FlagaSzukania.objects.all()
#         data = [{'id': flaga.id, 'nazwa': flaga.nazwa, 'uwagi': flaga.uwagi} for flaga in flagi]
#         return JsonResponse(data, safe=False)


# Koniec API

@login_required(login_url='error')
def order_search_er(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    top_us = top_user(request)
    about = settings.INFO_PROGRAM

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    tytul1 = 'Lista zamówień '
    tytul2 = str(rok)
    tytul3 = ''

    if top_us:
        zamowienia = Zamowienie.objects.filter(kontrola=1).order_by('-pk') # rok=rok,
    else:
        zamowienia = Zamowienie.objects.filter(kontrola=1, inicjaly=inicjaly).order_by('-pk')


    tzero = Money('00.00', PLN).amount

    nrsde = NrSDE.objects.all().order_by('nazwa')
    nr_sde = NrSDE.objects.filter(rok=rok).order_by('nazwa')
    nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')

    SDE_None = None

    paginator = Paginator(zamowienia, PAGIN_PAGE)
    strona = request.GET.get('page')
    pzamowienia = paginator.get_page(strona)

    return render(request, 'ORDERS/ord_main.html', {
        'zamowienia': pzamowienia,
        'name_log': name_log,
        'tytul_tabeli1': tytul1,
        'tytul_tabeli2': tytul2,
        'tytul_tabeli3': tytul3,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'tzero': tzero,
        'nrsde': nrsde,
        'nr_sde': nr_sde,
        'nrmpk': nrmpk,
        'SDE_None': SDE_None,
        'suma': 0,
        'szukanie': False,
        'src': '^',
        'fl': 'error',
        'b_rok': b_rok
    })


@login_required(login_url='error')
def ord_search_pro(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    top_us = top_user(request)
    about = settings.INFO_PROGRAM

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    tytul1 = 'Proformy i zaliczki: '
    tytul2 = str(rok)
    tytul3 = ''

    query = 'Proforma'

    search_fields = [
        'rodzaj_plat'
    ]
    f = search_filter(search_fields, testQuery(query))

    if top_us:
        zamowienia = Zamowienie.objects.filter(f).order_by('-pk')
    else:
        zamowienia = Zamowienie.objects.filter(f).filter(inicjaly=inicjaly).order_by('-pk')

    tzero = Money('00.00', PLN).amount

    nrsde = NrSDE.objects.all().order_by('nazwa')
    nr_sde = NrSDE.objects.filter(rok=rok).order_by('nazwa')
    nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')

    SDE_None = None

    paginator = Paginator(zamowienia, PAGIN_PAGE)
    strona = request.GET.get('page')
    pzamowienia = paginator.get_page(strona)

    return render(request, 'ORDERS/ord_main.html', {
        'zamowienia': pzamowienia,
        'name_log': name_log,
        'tytul_tabeli1': tytul1,
        'tytul_tabeli2': tytul2,
        'tytul_tabeli3': tytul3,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'tzero': tzero,
        'nrsde': nrsde,
        'nr_sde': nr_sde,
        'nrmpk': nrmpk,
        'SDE_None': SDE_None,
        'suma': 0,
        'szukanie': False,
        'src': '^',
        'fl': 'error',
        'b_rok': b_rok
    })


@login_required(login_url='error')
def order_search(request, src):
    if request.method == "GET":
        lata, rok, brok = test_rok(request)
        name_log, inicjaly = test_osoba(request)
        top_us = top_user(request)

        if int(rok) == int(brok):
            b_rok = True
        else:
            b_rok = False

        try:
            flaga = request.GET['FLAGA']
            sw = 1
        except:
            flaga = False
            sw = 0

        try:
            query = request.GET['SZUKAJ']
        except:
            if src == '^':
                query = ' '
            else:
                query = DecodeSlash(src)

        #print(">>> QUERY: [", query, "]  FLAGA:", flaga )

        if query == '' or query == ' ':
            return redirect('order_start')
        else:
            if flaga:
                search_fields = ['flaga_sz__nazwa']
            else:
                search_fields = [
                    'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_dok1', 'zal1','nr_dok2',
                    'zal2', 'nr_dok3', 'zal3', 'kwota_brutto', 'data_zam', 'data_dost', 'nr_fv', 'inicjaly','nr_sde__nazwa',
                    'nr_sde__opis', 'nr_sde__targi', 'nr_sde__klient', 'nr_mpk__nazwa', 'nr_mpk__opis', 'flaga_sz__nazwa'
                ]
            f = search_filter(search_fields, testQuery(query))
            if top_us:
                zamowienia = Zamowienie.objects.filter(f).order_by('-pk')
            else:
                zamowienia = Zamowienie.objects.filter(f).filter(inicjaly=inicjaly).order_by('-pk')

        tytul1 = 'Szukasz: '

        try:
            ind = NrMPK.objects.filter(nazwa=query).values_list('id', flat=True)[0]
            tab = NrMPK.objects.get(id=ind)
            tytul2 = tab.nazwa
            tytul3 = tab.opis
            tytul4 = ''
        except:
            try:
                ind = NrSDE.objects.filter(nazwa=query).values_list('id', flat=True)[0]
                tab = NrSDE.objects.get(id=ind)
                tytul2 = tab.nazwa
                tytul3 = "[" + tab.opis + "]"
                tytul4 = tab.targi
            except:
                tytul2 = query
                tytul3 = ''
                tytul4 = ''

        about = settings.INFO_PROGRAM
        tzero = Money('00.00', PLN).amount

        nrsde = NrSDE.objects.all().order_by('-pk')  # filter(rok=rok)
        nr_sde = NrSDE.objects.filter(rok=rok).order_by('pk')
        nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')
        try:
            fid = NrSDE.objects.filter(rok=rok).first().id
        except:
            fid = 0

        suma, suma_c, fsc = suma_wartosci(zamowienia)

        return render(request, 'ORDERS/ord_main.html', {
            'zamowienia': zamowienia,  # pzamowienia,
            'name_log': name_log,
            'tytul_tabeli1': tytul1,
            'tytul_tabeli2': tytul2,
            'tytul_tabeli3': tytul3,
            'tytul_tabeli4': tytul4,
            'admini': test_admin(request),
            'about': about,
            'lata': lata,
            'rok': rok,
            'tzero': tzero,
            'nrsde': nrsde,
            'nr_sde': nr_sde,
            'nrmpk': nrmpk,
            'fid': fid,
            'b_fid': True,
            'suma': suma,
            'suma_c': suma_c,
            'fsc': fsc,
            'szukanie': True,
            'src': CodeSlash(query),
            'fl': 'search',
            'sw': sw,
            'b_rok': b_rok
        })
    else:
        if src=='^':
            return redirect('order_start')
        else:
            return redirect('ord_search', src=src)


@login_required(login_url='error')
def order_search_sde(request, src):
    if request.method == "GET":

        try:
            query = request.GET['NRSDE']
        except:
            if src == '^':
                return redirect('order_start')
            else:
                query = str(src)


        lata, rok, brok = test_rok(request)
        name_log, inicjaly = test_osoba(request)
        top_us = top_user(request)
        tytul1 = 'Szukasz: '

        if int(rok) == int(brok):
            b_rok = True
        else:
            b_rok = False

        if top_us:
            zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=query).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=query, inicjaly=inicjaly).order_by('-pk')

        try:
            ind = NrSDE.objects.filter(nazwa=query).values_list('id', flat=True)[0]
            tab = NrSDE.objects.get(id=ind)
            tytul2 = tab.nazwa
            tytul3 = "[" + tab.opis + "]"
            tytul4 = tab.targi
        except:
            tytul2 = " "
            tytul3 = " "
            tytul4 = " "

        about = settings.INFO_PROGRAM

        nrsde = NrSDE.objects.all().order_by('-nazwa')  # filter(rok=rok)
        nr_sde = NrSDE.objects.filter(rok=rok).order_by('pk')
        nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')
        try:
            fid = NrSDE.objects.filter(rokk=rok).first().id
        except:
            fid = NrSDE.objects.filter(rokk=brok).first().id

        b_fid = True

        suma, suma_c, fsc = suma_wartosci(zamowienia)

        tzero = Money('00.00', PLN).amount

        return render(request, 'ORDERS/ord_main.html', {
            'zamowienia': zamowienia,  # pzamowienia,
            'name_log': name_log,
            'tytul_tabeli1': tytul1,
            'tytul_tabeli2': tytul2,
            'tytul_tabeli3': tytul3,
            'tytul_tabeli4': tytul4,
            'admini': test_admin(request),
            'about': about,
            'lata': lata,
            'rok': rok,
            'tzero': tzero,
            'nrsde': nrsde,
            'nr_sde': nr_sde,
            'nrmpk': nrmpk,
            'fid': fid,
            'b_fid': b_fid,
            'suma': suma,
            'suma_c': suma_c,
            'fsc': fsc,
            'szukanie': True,
            'src' : query,
            'fl': 'sde',
            'sw': 0,
            'b_rok': b_rok
        })
    else:
        return redirect('order_start')


@login_required(login_url='error')
def order_search_mpk(request, src):

    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    top_us = top_user(request)

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    about = settings.INFO_PROGRAM
    tzero = Money('00.00', PLN).amount

    if request.method == "GET":
        try:
            query = request.GET['NRMPK']
        except:
            if src == '^':
                return redirect('order_start')
            else:
                query = DecodeSlash(src)

        if top_us:
            zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=query).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=query, inicjaly=inicjaly, rok=rok).order_by('-pk')  #.filter(inicjaly=inicjaly)

        tytul1 = 'Szukasz: '
        try:
            ind = NrMPK.objects.filter(nazwa=query).values_list('id', flat=True)[0]
            tab = NrMPK.objects.get(id=ind)
            tytul2 = tab.nazwa
            tytul3 = "[" + tab.opis + "]"
        except:
            tytul2 = " "
            tytul3 = " "

        nrsde = NrSDE.objects.all().order_by('-pk')  # filter(rok=rok)
        nr_sde = NrSDE.objects.filter(rok=rok).order_by('pk')
        nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')
        try:
            fid = NrSDE.objects.filter(rok=rok).first().id
        except:
            fid = 0

        if fid == 0:
            b_fid = False
        else:
            b_fid = True

        suma, suma_c, fsc = suma_wartosci(zamowienia)

        return render(request, 'ORDERS/ord_main.html', {
            'zamowienia': zamowienia,
            'name_log': name_log,
            'tytul_tabeli1': tytul1,
            'tytul_tabeli2': tytul2,
            'tytul_tabeli3': tytul3,
            'admini': test_admin(request),
            'about': about,
            'lata': lata,
            'rok': rok,
            'tzero': tzero,
            'nrsde': nrsde,
            'nr_sde': nr_sde,
            'nrmpk': nrmpk,
            'fid': fid,
            'b_fid': b_fid,
            'suma': suma,
            'suma_c': suma_c,
            'fsc': fsc,
            'szukanie': True,
            'src': CodeSlash(query),
            'fl': 'mpk',
            'sw': 0,
            'b_rok': b_rok
        })
    else:
        return redirect('order_start')


def SetRokRokk(naz_sda, dataf):
    rok = 0
    rokk = 0

    if naz_sda != '':
        zs = str(naz_sda).split('_')
        l = len(zs)
        rok = int(zs[l - 1])

    if dataf != 0:
        rokk = int(dataf.split('.')[2])
    return rok, rokk


def CalcKwotaBrutto(trig, zal1, zal2, zal3, zal1_bi,  zal2_bi, zal3_bi):
    zero = Money('00.00', trig)
    tzero = zero.amount

    zal1_b_23 = zal1 * decimal.Decimal('1.23')
    zal2_b_23 = zal2 * decimal.Decimal('1.23')
    zal3_b_23 = zal3 * decimal.Decimal('1.23')

    if zal1_bi != tzero:
        zal1_b_23 = tzero
        sum_brutto = zal1_bi
    else:
        sum_brutto = zal1_b_23

    if zal2_bi != tzero:
        zal2_b_23 = tzero
        sum_brutto += zal2_bi
    else:
        sum_brutto += zal2_b_23

    if zal3_bi != tzero:
        zal3_b_23 = tzero
        sum_brutto += zal3_bi
    else:
        sum_brutto += zal3_b_23

    return Money(str(sum_brutto), trig)



@login_required(login_url='error')
def order_new(request, sel):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba1(request)
    about = settings.INFO_PROGRAM

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    tytul = ""
    if sel == 's':
        tytul = "Nowe zamówienie [SDE]"
        fsel = False
    elif sel == 'm':
        tytul = "Nowe zamówienie [MPK]"
        fsel = True
    else:
        tytul = "Nowe zamówienie"
        fsel = False

    if request.method == "POST":
        if sel == 's':
            orderf = ZamowienieFormM(request.POST or None, rok=rok)  # !!!
        else:
            orderf = ZamowienieForm(request.POST or None, rok=rok)

        if orderf.is_valid():
            ps = orderf.save(commit=False)

            trig = request.POST.get("zal3_1", "")
            zal_1 = Money(str(ps.zal1.amount), trig)
            zal_2 = Money(str(ps.zal2.amount), trig)
            zal_3 = Money(str(ps.zal3.amount), trig)
            ps.wartosc_zam = Money(str(ps.wartosc_zam.amount), trig)

            ps.zal1 = zal_1
            ps.zal2 = zal_2
            ps.zal3 = zal_3

            ps.kwota_netto = zal_1 + zal_2 + zal_3

            sum = zal_1 + zal_2 + zal_3

            ps.kwota_brutto = CalcKwotaBrutto(trig, zal_1.amount, zal_2.amount, zal_3.amount, ps.zal1_bi.amount,  ps.zal2_bi.amount, ps.zal3_bi.amount)

            dataf = request.POST.get("data_fv", "")
            tsde = request.POST.get("nr_sde", "")
            tmpk = request.POST.get("nr_mpk", "")
            src = request.POST.get("SRC", "")

            tzero = Money('00.00', PLN)
            if trig != tzero.currency and str(ps.kwota_netto.currency) != 'PLN':
                data, wartosc, kurs = CalcCurrency(ps.kwota_netto, dataf)
                ps.kwota_netto_pl = wartosc
                ps.kurs_walut = kurs
                if data != '':
                    ps.uwagi = "Wartość: " + str(ps.kwota_netto) + ' = ' + str(wartosc) + "; Kurs: " + str(kurs) + " [" + str(data) + "]"

            war_zam = request.POST.get("wartosc_zam_0", "")
            if war_zam == '0':
                ps.wartosc_zam = sum

            test = TestValidate(ps.wartosc_zam, ps.kwota_netto, tsde, tmpk, dataf, ps.roz)
            ps.kontrola = test

            if test == 0 or test == 10:

                if tsde != '':
                    ps.rok, ps.rokk = SetRokRokk(NrSDE.objects.get(id=tsde).nazwa, dataf)
                else:
                    ps.rok, ps.rokk = (rok, rok)

            else:
                ps.rok, ps.rokk = (rok, rok)

            ps.inicjaly = inicjaly
            ps.nr_fv = ps.nr_dok3

            o_ik = ''
            if tsde !='':
                o_ik = "SDE: " + NrSDE.objects.get(id=tsde).nazwa
            if tmpk != '':
                o_ik = o_ik + "MPK: " + NrMPK.objects.get(id=tmpk).nazwa

            s = o_ik + ", Kontrahent: "+str(ps.kontrahent)+", Kwota Netto: "+str(ps.kwota_netto)+", Data zamówienia: "+str(ps.data_zam)
            logi_order(0, s, 0, inicjaly, 0)

            ps.save()

            if src=='^' or src=="":
                return redirect('order_start')
            else:
                return redirect('ord_search', src=src)

    else:

        mpk_id = NrMPK.objects.none()
        sde_id = NrSDE.objects.none()

        if sel == 's':
            orderf = ZamowienieFormM(initial={'nr_sde': sde_id, 'nr_mpk': mpk_id}, rok=rok)  # !!!
        else:
            orderf = ZamowienieForm(initial={'nr_sde': sde_id, 'nr_mpk': mpk_id}, rok=rok)

    return render(request, 'ORDERS/ord_new.html', {
        'form': orderf,
        'potwierdzenie': rozliczenie,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'edycja': False,
        'ord_id': 0,
        'src': '^',
        'fl': 'new',
        'ma': True,
        'b_rok': b_rok,
        'rok': rok,
        'fsel': fsel
    })


@login_required(login_url='error')
def order_edit(request, pk, src, fl):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba1(request)
    about = settings.INFO_PROGRAM

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    ma = False #przekazanie flagi do form !!!
    se = False
    mp = False
    sd = False
    er = False

    tytul = "Edycja zamówienia"
    orderm = get_object_or_404(Zamowienie, pk=pk)
    if request.method == "POST":
        orderf = ZamowienieForm(request.POST or None, instance=orderm, rok=rok) #brok
        fl = request.POST.get("FL", "")
        if orderf.is_valid():
            ps = orderf.save(commit=False)

            trig = request.POST.get("zal3_1", "")
            zal_1 = Money(str(ps.zal1.amount), trig)
            zal_2 = Money(str(ps.zal2.amount), trig)
            zal_3 = Money(str(ps.zal3.amount), trig)

            ps.zal1 = zal_1
            ps.zal2 = zal_2
            ps.zal3 = zal_3
            ps.wartosc_zam = Money(str(ps.wartosc_zam.amount), trig)

            ps.kwota_netto = zal_1 + zal_2 + zal_3

            ps.kwota_brutto = CalcKwotaBrutto(trig, zal_1.amount, zal_2.amount, zal_3.amount, ps.zal1_bi.amount,  ps.zal2_bi.amount, ps.zal3_bi.amount)

            dataf = request.POST.get("data_fv", "")
            tsde  = request.POST.get("nr_sde", "")
            tmpk  = request.POST.get("nr_mpk", "")
            src   = request.POST.get("SRC", "")
            fl    = request.POST.get("FL","")

            tzero = Money('00.00', PLN)
            if trig != tzero.currency and str(ps.kwota_netto.currency) != 'PLN':
                data, wartosc, kurs = CalcCurrency(ps.kwota_netto, dataf)
                ps.kwota_netto_pl = wartosc
                ps.kurs_walut = kurs
                if data != '':
                    ps.uwagi = ps.uwagi + "\nWartość: " + str(ps.kwota_netto) + ' = ' + str(wartosc) + "; Kurs: " + str(kurs) + " [" + str(data) + "]"
            else:
                ps.kwota_netto_pl = tzero
                # ps.uwagi = ""

            test = TestValidate(ps.wartosc_zam, ps.kwota_netto, tsde, tmpk, dataf, ps.roz) #, ps.nr_dok3
            ps.kontrola = test


            if test == 0 or test == 10:

                if tsde != '':
                    try:
                        ps.rok, ps.rokk = SetRokRokk(NrSDE.objects.get(id=tsde).nazwa, dataf)
                    except:
                        ps.rok, ps.rokk = (rok, rok)
                        s = "Problem przy zapisie edytowanego wiersza. Zmienne: tsde["+str(tsde)+"], dataf["+str(dataf)+"]"
                        logi_order(4, s, 0, inicjaly, 0)
                else:
                    ps.rok, ps.rokk = (rok, rok)

            else:
                ps.rok, ps.rokk = (rok, rok)


            ps.nr_fv = ps.nr_dok3

            o_ik = ''
            if tsde !='':
                o_ik = "SDE: " + NrSDE.objects.get(id=tsde).nazwa
            if tmpk != '':
                o_ik = o_ik + "MPK: " + NrMPK.objects.get(id=tmpk).nazwa

            s = o_ik + ", Kontrahent: "+str(ps.kontrahent)+", Kwota Netto: "+str(ps.kwota_netto)+", Data zamówienia: "+str(ps.data_zam)
            logi_order(1, s, 0, inicjaly, 0)

            ps.save()

            if src=='^' or src=="":
                return redirect('order_start')
            else:
                if fl=='main':
                    return redirect('order_start')
                if fl=='search':
                    return redirect('ord_search', src=src)
                if fl=='mpk':
                    return redirect('ord_search_mpk', src=src)
                if fl=='sde':
                    return redirect('ord_search_sde', src=src)
                if fl=='error':
                    return redirect('ord_search_er')

        else:
            if fl == 'main':
                ma = True
            if fl == 'search':
                se = True
            if fl == 'mpk':
                mp = True
            if fl == 'sde':
                sd = True
            if fl == 'error':
                er = True


    else:
        orderf = ZamowienieForm(instance=orderm, rok=rok)


        if fl=='main':
            ma = True
        if fl=='search':
            se = True
        if fl=='mpk':
            mp = True
        if fl=='sde':
            sd = True
        if fl=='error':
            er = True

    return render(request, 'ORDERS/ord_new.html', {
        'form': orderf,
        'potwierdzenie': rozliczenie,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'edycja': True,
        'ord_id': pk,
        'src': src,
        'fl': fl,
        'ma': ma,
        'se': se,
        'mp': mp,
        'sd': sd,
        'er': er,
        'b_rok': b_rok,
        'rok': rok
    })


@login_required(login_url='error')
def order_delete(request, pk):

    name_log, inicjaly, rozliczenie = test_osoba1(request)

    ps = Zamowienie.objects.get(id=pk)

    o_ik = ''
    if ps.nr_sde_id != None:
        o_ik = "SDE: " + NrSDE.objects.get(id=ps.nr_sde_id).nazwa
    if ps.nr_mpk_id != None:
        o_ik = o_ik + "MPK: " + NrMPK.objects.get(id=ps.nr_mpk_id).nazwa

    s = o_ik + ", Kontrahent: " + str(ps.kontrahent) + ", Kwota Netto: " + str(ps.kwota_netto) + ", Data zamówienia: " + str(ps.data_zam)
    logi_order(2, s, 0, inicjaly, 4)
    Zamowienie.objects.get(pk=pk).delete()
    return redirect('order_start')


@login_required(login_url='error')
def order_rok_akt(request, pk):
    name_log, inicjaly = test_osoba(request)
    ur = URok.objects.all()
    for u in ur:
        if u.nazwa == inicjaly:
            u.rok = pk
            u.save()
    return redirect('order_start')


@login_required(login_url='error')
def sde_rok_akt(request, pk):
    name_log, inicjaly = test_osoba(request)
    ur = URok.objects.all()
    for u in ur:
        if u.nazwa == inicjaly:
            u.rok = pk
            u.save()
    return redirect('sde_start')


@login_required(login_url='error')
def sde_start(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM

    tytul = 'Lista pozycji SDE ' + str(rok)
    sde = NrSDE.objects.filter(rokk=rok).order_by('-nazwa_id')

    kl = "#"

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    return render(request, 'ORDERS/ord_main_sde.html', {
        'sde': sde,
        'name_log': name_log,
        'tytul_tabeli': tytul,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'klucz' : kl,
        'b_rok': b_rok
    })


@login_required(login_url='error')
def sde_search(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM

    query = request.GET['SZUKAJ']

    #print("ROK:", rok, " BROK:", brok)

    if query == '' or query == ' ':
        return redirect('sde_start')
    else:
        search_fields = [
            'nazwa', 'klient', 'targi', 'opis', 'rks', 'mcs', 'pm'
        ]
        f = search_filter(search_fields, testQuery(query))
        sde = NrSDE.objects.filter(f).filter(rokk=rok).order_by('-nazwa')

    tytul = 'Lista pozycji SDE ' + str(rok) + ', Szukasz: '+ query

    kl = query

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False


    return render(request, 'ORDERS/ord_main_sde.html', {
        'sde': sde,
        'name_log': name_log,
        'tytul_tabeli': tytul,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'klucz': CodeSlash(kl),
        'b_rok': b_rok
    })


@login_required(login_url='error')
def sde_pdf(request, kl):
    lata, rok, brok = test_rok(request)
    tytul = "SDE_" + str(rok)
    if kl == "#":
        sde = NrSDE.objects.filter(rokk=rok).order_by('nazwa')
    else:
        search_fields = [
            'nazwa', 'klient', 'targi', 'opis', 'rks', 'mcs', 'pm'
        ]
        f = search_filter(search_fields, DecodeSlash(testQuery(kl)))
        sde = NrSDE.objects.filter(f).filter(rok=rok).order_by('nazwa')
        tytul = tytul+"_"+str(DecodeSlash(kl))

    return out_pdf_sde(request, sde, tytul)


@login_required(login_url='error')
def sde_xls(request, kl):
    lata, rok, brok = test_rok(request)
    tytul = "SDE_" + str(rok)
    if kl == "#":
        sde = NrSDE.objects.filter(rokk=rok).order_by('nazwa')
    else:
        search_fields = [
            'nazwa', 'klient', 'targi', 'opis', 'rks', 'mcs', 'pm'
        ]
        f = search_filter(search_fields, DecodeSlash(testQuery(kl)))
        sde = NrSDE.objects.filter(f).filter(rok=rok).order_by('nazwa')
        tytul = tytul+"_"+str(DecodeSlash(kl))

    return out_xls_sde(request, sde, tytul)


@login_required(login_url='error')
def ord_pdf(request, src, fl, sw):
    lata, rok, brok = test_rok(request)
    top_us = top_user(request)
    name_log, inicjaly = test_osoba(request)

    opis = ""
    if src == '^' and fl == 'main':

        if top_us:
            zamowienia = Zamowienie.objects.filter(rokk=rok).order_by('-pk') # rok=rok
        else:
            zamowienia = Zamowienie.objects.filter(rokk=rok, inicjaly=inicjaly).order_by('-pk')

        if len(zamowienia) == 0:
            return redirect('order_start')


        suma, suma_c, fsc = suma_wartosci(zamowienia)
        t = '_wszystkie pozycje'
        opis = 'Wszystkie pozycje.'

    elif fl == 'search':
        if sw == '1':
            search_fields = ['flaga_sz__nazwa']
        else:
            search_fields = [
                'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_dok1', 'zal1', 'nr_dok2',
                'zal2', 'nr_dok3', 'zal3', 'kwota_brutto', 'data_zam', 'data_dost', 'nr_fv', 'inicjaly', 'nr_sde__nazwa',
                'nr_sde__opis', 'nr_sde__targi', 'nr_sde__klient', 'nr_mpk__nazwa', 'nr_mpk__opis'
            ]
        f = search_filter(search_fields, DecodeSlash(testQuery(src)))

        if top_us:
            zamowienia = Zamowienie.objects.filter(f).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(f).filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

        if len(zamowienia) == 0:
            return redirect('order_start')

        suma, suma_c, fsc = suma_wartosci(zamowienia)
        t = DecodeSlash(src)

        try:
            ind = NrMPK.objects.filter(nazwa=t).values_list('id', flat=True)[0]
            tab = NrMPK.objects.get(id=ind)
            opis = "[ "+tab.nazwa+" ] "+ tab.opis
        except:
            try:
                ind = NrSDE.objects.filter(nazwa=t).values_list('id', flat=True)[0]
                tab = NrSDE.objects.get(id=ind)
                opis = "[ " + tab.nazwa + " ] " + tab.opis + " - " + tab.targi
            except:
                opis = t

        t = "_" + t

    elif fl == 'sde':

        if top_us:
            zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

            if len(zamowienia) == 0:
                return redirect('order_start')

        suma, suma_c, fsc  = suma_wartosci(zamowienia)
        t = DecodeSlash(src)

        try:
            ind = NrMPK.objects.filter(nazwa=t).values_list('id', flat=True)[0]
            tab = NrMPK.objects.get(id=ind)
            opis = "[ "+tab.nazwa+" ] "+ tab.opis
        except:
            try:
                ind = NrSDE.objects.filter(nazwa=t).values_list('id', flat=True)[0]
                tab = NrSDE.objects.get(id=ind)
                opis = "[ " + tab.nazwa + " ] " + tab.opis + " - " + tab.targi
            except:
                opis = t

        t = "_" + t

    elif fl == 'mpk':

        if top_us:
            zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

        if len(zamowienia) == 0:
            return redirect('order_start')

        suma, suma_c, fsc = suma_wartosci(zamowienia)
        t = DecodeSlash(src)

        try:
            ind = NrMPK.objects.filter(nazwa=t).values_list('id', flat=True)[0]
            tab = NrMPK.objects.get(id=ind)
            opis = "[ "+tab.nazwa+" ] "+ tab.opis
        except:
            try:
                ind = NrSDE.objects.filter(nazwa=t).values_list('id', flat=True)[0]
                tab = NrSDE.objects.get(id=ind)
                opis = "[ " + tab.nazwa + " ] " + tab.opis + " - " + tab.targi
            except:
                opis = t

        t = "_" + t


    adata = datetime.now().strftime('%Y-%m-%d')
    tytul = "zamówienia_"+str(adata)+t

    return out_pdf_ord(request, zamowienia, tytul, suma, suma_c, fsc, opis, adata)


@login_required(login_url='error')
def ord_xls(request, src, fl, sw):
    lata, rok, brok = test_rok(request)
    top_us = top_user(request)
    name_log, inicjaly = test_osoba(request)

    opis = ""
    if src == '^' and fl == 'main':

        if top_us:
            zamowienia = Zamowienie.objects.filter(rokk=rok).order_by('-pk') # rok=rok
        else:
            zamowienia = Zamowienie.objects.filter(rokk=rok, inicjaly=inicjaly).order_by('-pk')

        if len(zamowienia) == 0:
            return redirect('order_start')


        suma, suma_c, fsc = suma_wartosci(zamowienia)
        t = '_wszystkie pozycje'
        opis = 'Wszystkie pozycje.'
    elif fl == 'search':
        if sw == '1':
            search_fields = ['flaga_sz__nazwa']
        else:
            search_fields = [
                'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_dok1', 'zal1', 'nr_dok2',
                'zal2', 'nr_dok3', 'zal3', 'kwota_brutto', 'data_zam', 'data_dost', 'nr_fv', 'inicjaly', 'nr_sde__nazwa',
                'nr_sde__opis', 'nr_sde__targi', 'nr_sde__klient', 'nr_mpk__nazwa', 'nr_mpk__opis'
            ]
        f = search_filter(search_fields, DecodeSlash(testQuery(src)))

        if top_us:
            zamowienia = Zamowienie.objects.filter(f).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(f).filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

        if len(zamowienia) == 0:
            return redirect('order_start')

        suma, suma_c, fsc = suma_wartosci(zamowienia)
        #t = DecodeSlash(src)

        # try:
        #     ind = NrMPK.objects.filter(nazwa=t).values_list('id', flat=True)[0]
        #     tab = NrMPK.objects.get(id=ind)
        #     opis = "[ "+tab.nazwa+" ] "+ tab.opis
        # except:
        #     try:
        #         ind = NrSDE.objects.filter(nazwa=t).values_list('id', flat=True)[0]
        #         tab = NrSDE.objects.get(id=ind)
        #         opis = "[ " + tab.nazwa + " ] " + tab.opis + " - " + tab.targi
        #     except:
        #         opis = t
        #
        # t = "_" + t
        #print("T1", t , type(t))

        t = "_SEARCH"

    elif fl == 'sde':

        if top_us:
            zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

            if len(zamowienia) == 0:
                return redirect('order_start')

        suma, suma_c, fsc  = suma_wartosci(zamowienia)
        t = DecodeSlash(src)

        try:
            ind = NrMPK.objects.filter(nazwa=t).values_list('id', flat=True)[0]
            tab = NrMPK.objects.get(id=ind)
            opis = "[ "+tab.nazwa+" ] "+ tab.opis
        except:
            try:
                ind = NrSDE.objects.filter(nazwa=t).values_list('id', flat=True)[0]
                tab = NrSDE.objects.get(id=ind)
                opis = "[ " + tab.nazwa + " ] " + tab.opis + " - " + tab.targi
            except:
                opis = t

        t = "_" + t

    elif fl == 'mpk':

        if top_us:
            zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

        if len(zamowienia) == 0:
            return redirect('order_start')

        suma, suma_c, fsc = suma_wartosci(zamowienia)
        t = DecodeSlash(src)

        try:
            ind = NrMPK.objects.filter(nazwa=t).values_list('id', flat=True)[0]
            tab = NrMPK.objects.get(id=ind)
            opis = "[ "+tab.nazwa+" ] "+ tab.opis
        except:
            try:
                ind = NrSDE.objects.filter(nazwa=t).values_list('id', flat=True)[0]
                tab = NrSDE.objects.get(id=ind)
                opis = "[ " + tab.nazwa + " ] " + tab.opis + " - " + tab.targi
            except:
                opis = t

        t = "_" + t


    adata = datetime.now().strftime('%Y-%m-%d')
    tytul = "zamówienia_" + str(adata) + t

    #return out_pdf_ord(request, zamowienia, tytul, suma, suma_c, fsc, opis, adata)
    return out_xls_ord(request, zamowienia, tytul, t)


@login_required(login_url='error')
def ord_csv(request, src, fl, sw):
    lata, rok, brok = test_rok(request)
    top_us = top_user(request)
    name_log, inicjaly = test_osoba(request)

    opis = ""
    if src == '^' and fl == 'main':

        if top_us:
            zamowienia = Zamowienie.objects.filter(rokk=rok).order_by('-pk') # rok=rok
        else:
            zamowienia = Zamowienie.objects.filter(rokk=rok, inicjaly=inicjaly).order_by('-pk')

        if len(zamowienia) == 0:
            return redirect('order_start')


        suma, suma_c, fsc = suma_wartosci(zamowienia)
        t = '_wszystkie pozycje'
        opis = 'Wszystkie pozycje.'
    elif fl == 'search':
        if sw == '1':
            search_fields = ['flaga_sz__nazwa']
        else:
            search_fields = [
                'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_dok1', 'zal1', 'nr_dok2',
                'zal2', 'nr_dok3', 'zal3', 'kwota_brutto', 'data_zam', 'data_dost', 'nr_fv', 'inicjaly', 'nr_sde__nazwa',
                'nr_sde__opis', 'nr_sde__targi', 'nr_sde__klient', 'nr_mpk__nazwa', 'nr_mpk__opis'
            ]
        f = search_filter(search_fields, DecodeSlash(testQuery(src)))

        if top_us:
            zamowienia = Zamowienie.objects.filter(f).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(f).filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

        if len(zamowienia) == 0:
            return redirect('order_start')

        suma, suma_c, fsc = suma_wartosci(zamowienia)
        t = src #DecodeSlash(src)

        # try:
        #     ind = NrMPK.objects.filter(nazwa=t).values_list('id', flat=True)[0]
        #     tab = NrMPK.objects.get(id=ind)
        #     opis = "[ "+tab.nazwa+" ] "+ tab.opis
        # except:
        #     try:
        #         ind = NrSDE.objects.filter(nazwa=t).values_list('id', flat=True)[0]
        #         tab = NrSDE.objects.get(id=ind)
        #         opis = "[ " + tab.nazwa + " ] " + tab.opis + " - " + tab.targi
        #     except:
        #         opis = t
        #
        # t = "_" + t
        t = "_SEARCH"
        #opis = 'Szukane pozycje.'

    elif fl == 'sde':

        if top_us:
            zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

            if len(zamowienia) == 0:
                return redirect('order_start')

        suma, suma_c, fsc  = suma_wartosci(zamowienia)
        t = DecodeSlash(src)

        try:
            ind = NrMPK.objects.filter(nazwa=t).values_list('id', flat=True)[0]
            tab = NrMPK.objects.get(id=ind)
            opis = "[ "+tab.nazwa+" ] "+ tab.opis
        except:
            try:
                ind = NrSDE.objects.filter(nazwa=t).values_list('id', flat=True)[0]
                tab = NrSDE.objects.get(id=ind)
                opis = "[ " + tab.nazwa + " ] " + tab.opis + " - " + tab.targi
            except:
                opis = t

        t = "_" + t

    elif fl == 'mpk':

        if top_us:
            zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok).order_by('-pk')
        else:
            zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

        if len(zamowienia) == 0:
            return redirect('order_start')

        suma, suma_c, fsc = suma_wartosci(zamowienia)
        t = DecodeSlash(src)

        try:
            ind = NrMPK.objects.filter(nazwa=t).values_list('id', flat=True)[0]
            tab = NrMPK.objects.get(id=ind)
            opis = "[ "+tab.nazwa+" ] "+ tab.opis
        except:
            try:
                ind = NrSDE.objects.filter(nazwa=t).values_list('id', flat=True)[0]
                tab = NrSDE.objects.get(id=ind)
                opis = "[ " + tab.nazwa + " ] " + tab.opis + " - " + tab.targi
            except:
                opis = t

        t = "_" + t


    adata = datetime.now().strftime('%Y-%m-%d')
    tytul = "zamówienia_" + str(adata) + str(t)

    #return out_pdf_ord(request, zamowienia, tytul, suma, suma_c, fsc, opis, adata)
    return out_csv_ord(request, zamowienia, tytul, t)




def SetNazwaId(nazwa):
    if nazwa != '':
        zs = str(nazwa).split('_')
        l = len(zs)
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
    else:
        s = ''
    return s


@login_required(login_url='error')
def sde_new(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM

    tytul = "Nowa pozycja SDE"
    if request.method == "POST":
        sdef = NrSDEForm(request.POST or None)
        if sdef.is_valid():
            ps = sdef.save(commit=False)
            ps.rok = brok
            ps.rokk = rok
            ps.nazwa_id = SetNazwaId(request.POST.get("nazwa", ""))

            nr_zlec = request.POST.get("nazwa", "")
            klient = request.POST.get("klient", "")
            targi = request.POST.get("targi", "")
            stoisko = request.POST.get("stoisko", "")
            opis = request.POST.get("opis", "")

            if opis != '':
                opis = ' ('+opis+')'
            if klient != '':
                klient = klient+' - '
            if targi != '':
                targi = targi + ' - '
            if stoisko != '':
                stoisko = '/'+stoisko + '/ '

            ps.opis = klient + targi + stoisko + nr_zlec + opis


            ps.save()
            return redirect('sde_start')
        else:
            return redirect('error')
    else:
        if rok != 2020:
            try:
                st = NrSDE.objects.filter(rokk=rok).last().nazwa
            except:
                st = '000_'+str(rok)
            stt = st.split('_')
            it = int(stt[0]) + 1
            if it < 10:
                sde = '00' + str(it)
            elif it < 100:
                sde = '0' + str(it)
            else:
                sde = str(it)
            sde += '_' + stt[1]
        else:
            sde = ''

        sdef = NrSDEForm(initial={'nazwa': sde, })  # 'rks': stt[1]
    return render(request, 'ORDERS/ord_new_sde.html', {
        'form': sdef,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'edycja': False,
        'sde_id': 0
    })


@login_required(login_url='error')
def sde_edit(request, pk):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM

    tytul = "Edycja pozycja SDE"
    sdem = get_object_or_404(NrSDE, pk=pk)
    if request.method == "POST":
        sdef = NrSDEForm(request.POST or None, instance=sdem)
        if sdef.is_valid():
            ps = sdef.save(commit=False)
            ps.rok = brok
            ps.rokk = rok
            ps.nazwa_id = SetNazwaId(request.POST.get("nazwa", ""))
            ps.save()
            return redirect('sde_start')
        else:
            return redirect('error')
    else:
        sdef = NrSDEForm(instance=sdem)
    return render(request, 'ORDERS/ord_new_sde.html', {
        'form': sdef,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'edycja': True,
        'sde_id': pk
    })


@login_required(login_url='error')
def sde_delete(request, pk):
    NrSDE.objects.get(pk=pk).delete()
    return redirect('sde_start')


def order_export_xls(request, rok):
    return gen_xls(rok)


@login_required(login_url='error')
def nip_start(request):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul_tabeli = "Ustawienia dla Zamówień"

    return render(request, 'ORDERS/ord_nip.html', {
        'name_log': name_log,
        'about': about,
        'tytul_tabeli': tytul_tabeli
    })


def nip_list(request):
    nips = list(Nip.objects.values().order_by('-id'))
    return JsonResponse(nips, safe=False)


# @csrf_exempt
def nip_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nip = Nip.objects.create(nip=data['nip'], kontrahent=data['kontrahent'])
        return JsonResponse({'nip': nip.nip, 'kontrahent': nip.kontrahent})


@csrf_exempt
def nip_update(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        nip = Nip.objects.get(id=id)
        nip.nip = data['nip']
        nip.kontrahent = data['kontrahent']
        nip.save()
        return JsonResponse({'nip': nip.nip, 'kontrahent': nip.kontrahent})


@csrf_exempt
def nip_delete(request, id):
    if request.method == 'DELETE':
        nip = Nip.objects.get(id=id)
        nip.delete()
        return JsonResponse({'message': 'NIP deleted'})






# @login_required(login_url='error')
# def ord_nip(request):
#     lata, rok, brok = test_rok(request)
#     name_log, inicjaly = test_osoba(request)
#     about = settings.INFO_PROGRAM
#     tytul_tabeli = "Ustawienia dla Zamówień"
#
#     nip = Nip.objects.all().order_by('-id')#.order_by('kontrahent')
#
#     return render(request, 'ORDERS/ord_nip.html', {
#         'name_log': name_log,
#         'about': about,
#         'nip': nip,
#         'tytul_tabeli': tytul_tabeli
#     })
#
#
# @require_http_methods(["POST"])
# def ord_nip_add(request):
#     print("***")
#     nip_value = request.POST.get('nip')
#     kontrahent_value = request.POST.get('kontrahent')
#     print(">>>", nip_value, kontrahent_value)
#     nip = Nip(nip=nip_value, kontrahent=kontrahent_value)
#     nip.save()
#     return JsonResponse({'status': 'success', 'nip': nip_value, 'kontrahent': kontrahent_value})
#
#
#
# @require_http_methods(["POST"])
# def update_nip(request, id):
#     nip = get_object_or_404(Nip, id=id)
#     nip.nip = request.POST.get('nip', nip.nip)
#     nip.kontrahent = request.POST.get('kontrahent', nip.kontrahent)
#     nip.save()
#     return JsonResponse({'status': 'success', 'nip': nip.nip, 'kontrahent': nip.kontrahent})
#
# @require_http_methods(["DELETE"])
# def delete_nip(request, id):
#     nip = get_object_or_404(Nip, id=id)
#     nip.delete()
#     return JsonResponse({'status': 'success'})
