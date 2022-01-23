from datetime import datetime

from LOG.logs import LogiORD
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from simple_search import search_filter
from .models import Zamowienie, NrSDE, NrMPK
from .forms import ZamowienieForm, NrSDEForm
from moneyed import Money, PLN
from TaskAPI.models import URok
from django.core.paginator import Paginator
from .pdf import out_pdf_sde, out_pdf_ord
from .xls import gen_xls
from .functions import test_admin, test_osoba, test_osoba1, test_rok, testQuery, suma_wartosci, CalcCurrency
from .functions import TestValidate, DecodeSlash, CodeSlash
from SDA.settings import PAGIN_PAGE


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
    zamowienia = Zamowienie.objects.filter(rokk=rok, roz=False).order_by('-pk') # rok=rok
    tzero = Money('00.00', PLN)

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
    about = settings.INFO_PROGRAM

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    tytul1 = 'Lista zamówień [wszystkie] '
    tytul2 = str(rok)
    tytul3 = ''
    zamowienia = Zamowienie.objects.filter(rokk=rok).order_by('-pk')
    tzero = Money('00.00', PLN)

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
def order_search_er(request):
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
    zamowienia = Zamowienie.objects.filter(kontrola=1).order_by('-pk') # rok=rok,
    tzero = Money('00.00', PLN)

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
    zamowienia = Zamowienie.objects.filter(f).order_by('-pk') # rok=rok,
    tzero = Money('00.00', PLN)

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

        if int(rok) == int(brok):
            b_rok = True
        else:
            b_rok = False

        try:
            query = request.GET['SZUKAJ']
        except:
            if src == '^':
                query = ' '
            else:
                query = DecodeSlash(src)

        if query == '' or query == ' ':
            return redirect('order_start')
        else:
            search_fields = [
                'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_dok1', 'zal1','nr_dok2',
                'zal2', 'nr_dok3', 'zal3', 'kwota_brutto', 'data_zam', 'data_dost', 'nr_fv', 'inicjaly','nr_sde__nazwa',
                'nr_sde__opis', 'nr_sde__targi', 'nr_sde__klient', 'nr_mpk__nazwa', 'nr_mpk__opis'
            ]
            f = search_filter(search_fields, testQuery(query))
            zamowienia = Zamowienie.objects.filter(f).order_by('-pk') #.filter(rok=rok)      .filter(Q(rokk=2021) | Q(rokk=2022))

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
        tzero = Money('00.00', PLN)

        nrsde = NrSDE.objects.all().order_by('-pk')  # filter(rok=rok)
        nr_sde = NrSDE.objects.filter(rok=rok).order_by('pk')
        nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')
        try:
            fid = NrSDE.objects.filter(rok=rok).first().id
        except:
            fid = 0

        suma = suma_wartosci(zamowienia)

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
            'suma': suma,
            'szukanie': True,
            'src': CodeSlash(query),
            'fl': 'search',
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
        tytul1 = 'Szukasz: '

        if int(rok) == int(brok):
            b_rok = True
        else:
            b_rok = False

        zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=query).order_by('-pk')
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
            fid = NrSDE.objects.filter(rok=rok).first().id
        except:
            fid = NrSDE.objects.filter(rok=brok).first().id

        b_fid = True

        suma = suma_wartosci(zamowienia)

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
            'tzero': Money('00.00', PLN),
            'nrsde': nrsde,
            'nr_sde': nr_sde,
            'nrmpk': nrmpk,
            'fid': fid,
            'b_fid': b_fid,
            'suma': suma,
            'szukanie': True,
            'src' : query,
            'fl': 'sde',
            'b_rok': b_rok
        })
    else:
        return redirect('order_start')


@login_required(login_url='error')
def order_search_mpk(request, src):

    lata, rok, brok = test_rok(request)
    name_log, inicjaly = test_osoba(request)

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    about = settings.INFO_PROGRAM
    tzero = Money('00.00', PLN)

    if request.method == "GET":
        try:
            query = request.GET['NRMPK']
        except:
            if src == '^':
                return redirect('order_start')
            else:
                query = DecodeSlash(src)


        zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=query).filter(rok=rok).order_by('-pk')

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

        suma = suma_wartosci(zamowienia)

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
            'szukanie': True,
            'src': CodeSlash(query),
            'fl': 'mpk',
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


@login_required(login_url='error')
def order_new(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba1(request)
    about = settings.INFO_PROGRAM

    tytul = "Nowe zamówienie"
    if request.method == "POST":
        orderf = ZamowienieForm(request.POST or None, rok=brok)
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
            ps.kwota_brutto = Money(str(ps.kwota_brutto.amount), trig)

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
                    ps.uwagi = "[" + str(data) + "] Wartość: " + str(ps.kwota_netto) + '/' + str(
                        wartosc) + " Kurs: " + str(kurs)

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
            LogiORD(0, s, inicjaly)

            ps.save()

            if src=='^' or src=="":
                return redirect('order_start')
            else:
                return redirect('ord_search', src=src)
        else:
            return redirect('error')
    else:
        mpk_id = NrMPK.objects.none()
        sde_id = NrSDE.objects.none()
        orderf = ZamowienieForm(initial={'nr_sde': sde_id, 'nr_mpk': mpk_id}, rok=brok)  # 'sposob_plat': '-', 'rodzaj_plat': '-',
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
        'ma': True
    })


@login_required(login_url='error')
def order_edit(request, pk, src, fl):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba1(request)
    about = settings.INFO_PROGRAM

    tytul = "Edycja zamówienia"
    orderm = get_object_or_404(Zamowienie, pk=pk)
    if request.method == "POST":
        orderf = ZamowienieForm(request.POST or None, instance=orderm, rok=brok)
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
            ps.kwota_brutto = Money(str(ps.kwota_brutto.amount), trig)

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
                    ps.uwagi = ps.uwagi + "\n[" + str(data) + "] Wartość: " + str(ps.kwota_netto) + '/' + str(
                        wartosc) + " Kurs: " + str(kurs)

            test = TestValidate(ps.wartosc_zam, ps.kwota_netto, tsde, tmpk, dataf, ps.roz) #, ps.nr_dok3
            ps.kontrola = test


            if test == 0 or test == 10:

                if tsde != '':
                    try:
                        ps.rok, ps.rokk = SetRokRokk(NrSDE.objects.get(id=tsde).nazwa, dataf)
                    except:
                        ps.rok, ps.rokk = (rok, rok)
                        s = "Problem przy zapisie edytowanego wiersza. Zmienne: tsde["+str(tsde)+"], dataf["+str(dataf)+"]"
                        LogiORD(4, s, inicjaly)
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
            LogiORD(1, s, inicjaly)

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
            return redirect('error')

    else:
        orderf = ZamowienieForm(instance=orderm, rok=brok)
        ma = False
        se = False
        mp = False
        sd = False
        er = False
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
        'er': er
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
    LogiORD(2, s, inicjaly)
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

    if query == '' or query == ' ':
        return redirect('sde_start')
    else:
        search_fields = [
            'nazwa', 'klient', 'targi', 'opis', 'rks', 'mcs', 'pm'
        ]
        f = search_filter(search_fields, testQuery(query))
        sde = NrSDE.objects.filter(f).filter(rok=rok).order_by('-nazwa')

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
def ord_pdf(request, src, fl):
    lata, rok, brok = test_rok(request)
    opis = ""
    if src == '^' and fl == 'main':
        zamowienia = Zamowienie.objects.filter(rokk=rok).order_by('-pk') # rok=rok
        suma = str(suma_wartosci(zamowienia))
        t = '_wszystkie pozycje'
        opis = 'Wszystkie pozycje.'
    elif fl == 'search':
        search_fields = [
            'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_dok1', 'zal1', 'nr_dok2',
            'zal2', 'nr_dok3', 'zal3', 'kwota_brutto', 'data_zam', 'data_dost', 'nr_fv', 'inicjaly', 'nr_sde__nazwa',
            'nr_sde__opis', 'nr_sde__targi', 'nr_sde__klient', 'nr_mpk__nazwa', 'nr_mpk__opis'
        ]
        f = search_filter(search_fields, DecodeSlash(testQuery(src)))
        zamowienia = Zamowienie.objects.filter(f).filter(rok=rok).order_by('-pk')
        suma = str(suma_wartosci(zamowienia))
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

        zamowienia = Zamowienie.objects.filter(nr_sde__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok).order_by('-pk')
        suma = str(suma_wartosci(zamowienia))
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

        zamowienia = Zamowienie.objects.filter(nr_mpk__nazwa=DecodeSlash(testQuery(src))).filter(rok=rok).order_by('-pk')
        suma = str(suma_wartosci(zamowienia))
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

    return out_pdf_ord(request, zamowienia, tytul, suma, opis, adata)


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
            opis = request.POST.get("opis", "")

            if opis != '':
                opis = ' ('+opis+')'
            if klient != '':
                klient = klient+' - '
            if targi != '':
                targi = targi + ' - '

            ps.opis = klient + targi + nr_zlec + opis


            ps.save()
            return redirect('sde_start')
        else:
            return redirect('error')
    else:
        if rok != 2020:
            st = NrSDE.objects.filter(rokk=rok).last().nazwa
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

