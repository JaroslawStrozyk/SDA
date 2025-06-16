from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from moneyed import Money, EUR
from datetime import date, timedelta, datetime
import re
from ORDERS.models import NrSDE
from .forms import SkladForm
from .functions import CalCost, test_osoba, testQuery, ChangeStatus, SendInformation, CalCostGen, CalSelSde, \
    UpdateDokUwagi, CalcAdd, CalcDay, format_european_currency
from .log_oper import CompRepoLog
from .models import Sklad, Firma
from simple_search import search_filter
from .pdf import sklad_pdf_out, sklad_pdf_bc_out, sklad_pdf_sim_out, ewu_pdf_bc_out
from django.db.models import Max, OuterRef, Subquery, Count
from django.http import HttpResponse
from django.utils.timezone import now

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Firma
import json
from django.db.models import F
from django.db import transaction
#import datetime
from django.urls import reverse
from django.db.models import Case, When, Value, CharField

from django.db.models import IntegerField, Case, When, Value
from django.db.models.functions import Cast, Coalesce
from django.db.models.expressions import RawSQL

LOG = CompRepoLog()


@login_required(login_url='error')
def comp_list(request, mag):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    rw = True
    admin = False
    st_pr = '^'
    fl = True

    f = ''
    query = ''
    sklad = ''
    sw = False
    t = 'Lista elementów stoisk przechowywanych dla innych firm.'

    # Ustawienie czy API jest tylko do odczytu czy nie
    if grupa == 'produkcja' or grupa == 'kierownik' or grupa == 'magazyn1':
        rw = False

    try:
        query = request.GET['SZUKAJ']
        opis = "Szukane: " + str(query)
    except:
        opis = ''

    if query != '':
        sw = True
        search_fields = [
            'nr_sde__nazwa', 'nr_sde__targi', 'nr_sde__klient', 'nr_sde__stoisko',
            'przech_nazwa', 'przech_nrpalet', 'czas_od', 'czas_do']
        se = search_filter(search_fields, testQuery(query))
        sklad = Sklad.objects.filter(se).distinct('nr_sde')
    else:
        sklad = Sklad.objects.all().distinct('nr_sde')

        # Funkcja pomocnicza do ekstrakcji klucza sortowania
        def extract_sort_key(sklad_item):
            nr_sde_str = str(sklad_item.nr_sde.nazwa)  # Konwertujemy na string na wszelki wypadek
            nr, rok = nr_sde_str.split('_')  # Rozdzielamy na numer i rok
            return int(rok), int(nr)  # Zwracamy jako tuple do sortowania (rok, numer)

        # Sortowanie zmiennej sklad
        sklad = sorted(sklad, key=extract_sort_key, reverse=True)

        update_magazyn_opis()

    try:
        st = request.GET['STAWKA']
        st = str(st)
        st = st.replace(',', '.')
        wst = Money(st, EUR)
        sde_id = request.GET['SDE_ID']
        sde_id = int(sde_id)
        CalSelSde(sde_id, wst)

        info = "STAWKA - zapis;    sde: " + str(NrSDE.objects.get(pk=sde_id).nazwa) + ", wartość: " + str(wst) + "."
        LOG.zapis_stawka(request, info)
        fl = False
    except:
        st = ''
        sde_id = 0
        #print("COMP_REPO Error: ", "Błąd konwersji !!!")

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    if fl:
        LOG.start(request, query)

    return render(request, 'COMP_REPO/comp_main.html', {
        'mag': mag,
        'sklad': sklad,
        'name_log': name_log,
        'about': about,
        'title': t,
        'rw': rw,
        'sw': sw,
        'admin': admin,
        'opis': opis,
        'st_pr': st_pr
    })

def com_sort_query(fl):
    # Przygotowanie zapytania z sortowaniem
    sklad = (
        Sklad.objects.annotate(
            pierwsza_liczba=Coalesce(
                Cast(
                    Case(
                        # Jeśli pole `przech_nrpalet` zawiera cyfry, użyj SQL do wyciągnięcia liczby
                        When(
                            przech_nrpalet__regex=r'\d+',  # Jeśli pole zawiera liczby
                            then=RawSQL(
                                "regexp_replace(przech_nrpalet, '\\D.*', '', 'g')",
                                []  # Parametry zapytania SQL, jeśli są wymagane
                            )
                        ),
                        # Dla pozostałych przypadków ustaw `0` jako wartość domyślną
                        When(
                            przech_nrpalet='',
                            then=Value('0')
                        ),
                        default=Value('0'),  # Ten fragment zastępujemy!
                        output_field=IntegerField(),
                    ),
                    output_field=IntegerField()
                ),
                Value(0),  # Domyślnie zero, jeśli wartość to NULL
            )
        )
        .filter(multi_uzycie=True, firma=fl, liczyc=True)  # Filtruj dane
        .order_by('pierwsza_liczba')  # Sortuj według liczby
    )

    return sklad


def comp_multi(request, mag, fl):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM

    upgrade_uses()

    setD = False
    t = ''
    sw = False
    opis = ''
    query = ''
    suma_c = Money('0.00', EUR)

    firma = Firma.objects.all()

    fl, is_a = parse_string(fl)
    # Jeśli 'a' to wyświetlane są wszytskie wpisy
    if is_a:
        sklad = Sklad.objects.filter(multi_uzycie=True, firma=fl).order_by('przech_nazwa')
        t = 'Lista wszystkich elementów stoisk wielokrotnego użytku.'
    else:
        try:
            query = request.GET['SZUKAJ']
            opis = "Szukane: " + str(query)
        except:
            opis = ''

        if query != '':
            sw = True
            search_fields = [
                'nr_sde__nazwa', 'nr_sde__targi', 'nr_sde__klient', 'nr_sde__stoisko',
                'przech_nazwa', 'przech_nrpalet', 'czas_od', 'czas_do']
            se = search_filter(search_fields, testQuery(query))
            sklad = Sklad.objects.filter(multi_uzycie=True, firma=fl, liczyc=True).filter(se).order_by('przech_nrpalet')
            t = opis
        else:
            # Zamiast:
            # sklad = Sklad.objects.filter(multi_uzycie=True, firma=fl, liczyc=True).order_by('przech_nrpalet')
            # stosujemy com_sort_query(fl), które lepiej sortuje po polu przech_nrpalet
            sklad = com_sort_query(fl)

            for s in sklad:
                suma_c += s.koszt_przech

            naz = Firma.objects.get(id=fl).nazwa
            t = 'Lista elementów: ' + naz.upper()
            if fl == 1:
                setD = True
            else:
                setD = False

    suma_c = format_european_currency(suma_c)

    return render(request, 'COMP_REPO/comp_multi_n.html', {
        'name_log': name_log,
        'about': about,
        'title': t,
        'sklad': sklad,
        'mag': mag,
        'fl': fl,
        'firma': firma,
        'opis': opis,
        'sw': sw,
        'suma_c': suma_c,
        'setD': setD
    })


def CalPozCost(pk):
    zero = Money('0.00', EUR)
    s = Sklad.objects.get(pk=pk)

    # Obliczenie powierzchni
    pow = s.przech_sze * s.przech_gl
    s.przech_pow = pow

    # Obliczenie różnicy dni między d_start a d_stop
    d_delta = (s.czas_do - s.czas_od).days if s.czas_od and s.czas_do else 0
    s.ilosc_dni = d_delta

    # Obliczenie stawki dziennej
    stawka_d = s.stawka / 30 if s.stawka > zero else zero

    # Koszty przechowywania liczone zawsze
    s.koszt_przech = (pow * stawka_d) * d_delta

    s.save()


@login_required(login_url='error')
def comp_medit(request, pk, mag, fl):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    stawka = Money(settings.COMP_REPO_ST, EUR)
    admin = False

    search_query = request.GET.get('SZUKAJ', '')

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    tst = Sklad.objects.get(pk=pk).blokada
    bz = Sklad.objects.get(pk=pk).blokada_zapisu
    sr = Sklad.objects.get(pk=pk) # Dla kopiowania danych do nowego rekordu
    tst = bz


    skladm = get_object_or_404(Sklad, pk=pk)
    if request.method == "POST":
        skladf = SkladForm(request.POST or None, request.FILES or None, instance=skladm, stawka=stawka, bz=bz) # initial={'stawka':stawka}
        if skladf.is_valid():
            ps = skladf.save(commit=False)

            if 'nr_sde' in skladf.changed_data:
                magazyn = request.POST.get("magazyn", "")

                nr_sde = request.POST.get("nr_sde", "")
                try:
                    nr_sde_instance = NrSDE.objects.get(pk=nr_sde)
                except NrSDE.DoesNotExist:
                    nr_sde_instance = None

                przech_nazwa = request.POST.get("przech_nazwa", "")
                przech_nrpalet = request.POST.get("przech_nrpalet", "")
                stawka_0 = request.POST.get("stawka_0", "0.00")
                stawka_1 = request.POST.get("stawka_1", "EUR")
                stawka = Money(stawka_0, stawka_1)
                przech_sze = request.POST.get("przech_sze", "")
                przech_gl = request.POST.get("przech_gl", "")
                multi_uzycie = request.POST.get("multi_uzycie", "off")

                multi_uzycie = True if multi_uzycie == 'on' else False

                multi_uzycie_id = request.POST.get("multi_uzycie_id", "")
                multi_uzycie_st = request.POST.get("multi_uzycie_st", "")
                wydano_ilosc = request.POST.get("wydano_ilosc", "")

                try:
                    wydano_data = request.POST.get("wydano_data", "")
                    wydano_data = datetime.strptime(wydano_data, '%d.%m.%Y').date()
                except ValueError:
                    wydano_data = None
                zwroco_ilosc = request.POST.get("zwroco_ilosc", "")

                try:
                    zwroco_data = request.POST.get("zwroco_data", "")
                    zwroco_data = datetime.strptime(zwroco_data, '%d.%m.%Y').date()
                except ValueError:
                    zwroco_data = None

                zwroco_uwagi = request.POST.get("zwroco_uwagi", "")

                try:
                    czas_od = request.POST.get("czas_od", "")
                    czas_od = datetime.strptime(czas_od, '%d.%m.%Y').date()
                except ValueError:
                    czas_od = None
                try:
                    czas_do = request.POST.get("czas_do", "")
                    czas_do = datetime.strptime(czas_do, '%d.%m.%Y').date()
                except ValueError:
                    czas_do = None

                try:
                    firma = request.POST.get("firma", "")
                    firma = int(firma)
                except ValueError:
                    firma = 1
                firma = Firma.objects.get(id=firma)

                sk = Sklad(
                    magazyn=magazyn, nr_sde=nr_sde_instance, przech_nazwa=przech_nazwa, przech_nrpalet=przech_nrpalet,
                    stawka=stawka, przech_zdjecie=sr.przech_zdjecie, przech_zdjecie2=sr.przech_zdjecie2,
                    przech_zdjecie3=sr.przech_zdjecie3, przech_zdjecie4=sr.przech_zdjecie4, uszkodz_zdjecie1=sr.uszkodz_zdjecie1,
                    uszkodz_zdjecie2=sr.uszkodz_zdjecie2, uszkodz_zdjecie3=sr.uszkodz_zdjecie3, uszkodz_zdjecie4=sr.uszkodz_zdjecie4,
                    przech_sze=przech_sze, przech_gl=przech_gl, multi_uzycie=multi_uzycie, multi_uzycie_id=multi_uzycie_id,
                    multi_uzycie_st=multi_uzycie_st, wydano_ilosc=wydano_ilosc, zwroco_ilosc=zwroco_ilosc,
                    zwroco_uwagi=zwroco_uwagi, czas_od=czas_od, czas_do=czas_do, zwroco_data=zwroco_data, wydano_data=wydano_data,
                    firma=firma, liczyc=False
                )
                sk.save()
                #
                ChangeStatus(nr_sde)
                CalCost(nr_sde)
                #


            else:
                nr_sde = request.POST.get("nr_sde", "")
                multi_uzycie = request.POST.get("multi_uzycie", "off")
                multi_uzycie_id = request.POST.get("multi_uzycie_id", "")
                multi_uzycie_st = request.POST.get("multi_uzycie_st", "")

                ps.multi_uzycie, ps.multi_uzycie_id, ps.multi_uzycie_st = multi_user_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st)

                if admin:
                    if len(request.POST.get("faktura", "")) > 0:
                        ps.blokada = True
                    else:
                        ps.blokada = False

                ps.save()
                # CalcDay(ps.pk)
                # Powyzej zablokowane bo to samo liczy się poniżej
                CalPozCost(ps.pk)

            if search_query:
                return redirect(f"{reverse('comp_multi', kwargs={'mag': mag, 'fl': fl})}?SZUKAJ={search_query}")
            else:
                return redirect('comp_multi', mag=mag, fl=fl)
        else:
            # return redirect('error')
            return render(request, 'COMP_REPO/comp_madd.html', {
                'mag': mag,
                'form': skladf,
                'pk': 0,
                'edycja': False,
                'fl': fl,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': 'Dodawanie lub Edytowanie elementów wielokrotnie używanych.'
            })
    else:
        skladf = SkladForm(instance=skladm, stawka=stawka, bz=bz)


    return render(request, 'COMP_REPO/comp_madd.html', {
        'mag': mag,
        'form': skladf,
        'tst': tst,
        'pk': pk,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'fl': fl,
        'title': 'Dodawanie lub Edytowanie elementów wielokrotnie używanych.'
    })


@login_required(login_url='error')
def comp_detail(request, mag, pk, st):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    rw = True
    f = ''
    query = ''
    sklad = ''
    sw = False
    admin = False
    nstatus = False
    sum = ""
    nmg = ""
    fl = True
    ndok_pdf1 = ""
    ndok_pdf2 = ""
    ndok_pdf3 = ""
    ndok_pdf4 = ""
    nfv_pdf1 = ""
    nuwagi = ""
    blok_z = ""

    CalCost(pk)

    try:
        nsde = NrSDE.objects.get(pk=pk)
        nnazwa = nsde.nazwa
        ntargi = nsde.targi
        nklient = nsde.klient
        nstoisko = nsde.stoisko
        npm = nsde.pm
    except:
        nnazwa = "..."
        ntargi = ""
        nklient = ""
        nstoisko = ""
        npm = ""

    t = 'Lista elementów stoisk przechowywanych dla SDA ' + str(nnazwa)

    if grupa == 'produkcja' or grupa == 'kierownik':
        rw = False

    # Zamknięcia edycji danych
    if st == 'cs':
        sk = Sklad.objects.filter(nr_sde=pk)
        test = False
        for s in sk:
            test = s.status_pracy
            nmg = s.magazyn
            sum = s.suma
            sum_zw = s.suma_zw
            sum_np = s.suma_np
            s.status_pracy = False
            s.blokada_zapisu = True
            s.save()
        st = '^'

        if test == True:

            komunikat = 'Edycja zakończona.'
            log_info = (komunikat + "   MAGAZYN: " + nmg + "   SDE: " + nnazwa + "   TARGI: " + ntargi + "   KLIENT: "
                        + nklient + "   STOISKO: " + nstoisko + "   KOSZTY: " + str(sum) + "   SUMA_ZW: " + str(sum_zw) + "   SUMA_NP: " + str(sum_np))
            LOG.zakonczenie(request, log_info)

            SendInformation(nmg, nnazwa, ntargi, nklient, nstoisko, sum, sum_zw, sum_np, komunikat, npm)
            test = False
            fl = False

    if st == 'b1':
        sk = Sklad.objects.filter(nr_sde=pk)
        for s in sk:
            s.blokada_zapisu = True
            s.save()
        LOG.zapis_blokada(request, True)
        fl = False

    if st == 'b0':
        sk = Sklad.objects.filter(nr_sde=pk)
        for s in sk:
            s.blokada_zapisu = False
            s.save()
        LOG.zapis_blokada(request, False)
        fl = False

    if int(pk) == int(0):
        sklad = Sklad.objects.filter(nr_sde__isnull=True).order_by('przech_nrpalet').annotate(
            wynik=Case(
                When(status_pracy=False, multi_uzycie=False, then=Value("WYS")),
                When(status_pracy=False, multi_uzycie=True, then=Value("UKR")),
                When(status_pracy=True, then=Value("WYS")),
                output_field=CharField(),
            )
        )

        sorted_sklad = sklad
    else:
        sklad = Sklad.objects.filter(nr_sde=pk).annotate(
            wynik=Case(
                When(status_pracy=False, multi_uzycie=False, then=Value("WYS")),
                When(status_pracy=False, multi_uzycie=True, then=Value("UKR")),
                When(status_pracy=True, then=Value("WYS")),
                output_field=CharField(),
            )
        )

        # Funkcja pomocnicza do sortowania
        def sort_key(value):
            # Rozdzielenie numeru na część cyfrową i alfanumeryczną
            matches = re.match(r"([0-9]+)([a-zA-Z]*)", value.przech_nrpalet)
            number = int(matches.group(1)) if matches else 0
            letters = matches.group(2) if matches else ''
            return (number, letters)

        # Sortowanie wyników
        sorted_sklad = sorted(sklad, key=sort_key)

    try:
        sklads = sklad.first()
        nsuma = sklads.suma
        nsuma_zw = sklads.suma_zw
        nsuma_np = sklads.suma_np
        nuwagi = sklads.uwagi
        ndok_pdf1 = sklads.dok_pdf1.url if sklads.dok_pdf1 else None
        ndok_pdf2 = sklads.dok_pdf2.url if sklads.dok_pdf2 else None
        ndok_pdf3 = sklads.dok_pdf3.url if sklads.dok_pdf3 else None
        ndok_pdf4 = sklads.dok_pdf4.url if sklads.dok_pdf4 else None
        nfv_pdf1 = sklads.fv_pdf1.url if sklads.fv_pdf1 else None
        nsuma_pow = str(sklads.suma_pow) + ' m²'
        nstatus = sklads.status_pracy
        blok_z  = sklads.blokada_zapisu
        data_od = sklads.czas_od
        data_do = sklads.czas_do
        nr_fv   = sklads.faktura
        # print(">>> Odczyt danych do nagłówka")
    except:
        # print("*** Błąd odczytu danych do nagłówka")
        nsuma = '0,00'
        nsuma_pow = '0,0 m²'
        data_od = ''
        data_do = ''
        nr_fv = ''

    upgrade_flags_oper(f, pk)


    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    if fl:
        info = "OKNO SZCZEGÓŁY:   SDE: " + nnazwa + ", Powierzchnia: " + nsuma_pow + ", Koszt: " + str(nsuma) + ", Zwolnione: " + str(nsuma_zw) + ", Bez przypisania: " + str(nsuma_np) + "."
        LOG.start_detail(request, info)

    return render(request, 'COMP_REPO/comp_detail.html', {
        'det': pk,
        'nnazwa': nnazwa,
        'ntargi': ntargi,
        'nklient': nklient,
        'nstoisko': nstoisko,
        'npm': npm,
        'nsuma_pow': nsuma_pow,
        'nsuma': nsuma,
        'nsuma_zw': nsuma_zw,
        'nuwagi': nuwagi,
        'ndok_pdf1': ndok_pdf1,
        'ndok_pdf2': ndok_pdf2,
        'ndok_pdf3': ndok_pdf3,
        'ndok_pdf4': ndok_pdf4,
        'nfv_pdf1': nfv_pdf1,
        'nsuma_np': nsuma_np,
        'nstatus': nstatus,
        'mag': mag,
        'sklad': sorted_sklad,
        'name_log': name_log,
        'about': about,
        'title': t,
        'rw': rw,
        'sw': sw,
        'admin': admin,
        'blokz': blok_z,
        'data_od': data_od,
        'data_do': data_do,
        'nr_fv': nr_fv
    })

def multi_user_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st):
    mu = str(multi_uzycie)
    mu_id = int(multi_uzycie_id)
    mu_st = int(multi_uzycie_st)
    p_p = False
    if mu == 'on':
        m_u = True
        if mu_id == 0:
            mu_id = int(datetime.now().strftime("%y%m%d%H%M%S"))
            p_p = True
    else:
        m_u = False

    print(f"DEBUG: {m_u}, {mu_id}, {mu_st}, {p_p}")  # Debugowanie zwracanych wartości
    return m_u, mu_id, mu_st, p_p


def multi_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st, licz):
    mu = str(multi_uzycie)
    mu_id = int(multi_uzycie_id)
    mu_st = int(multi_uzycie_st)
    m_u = False
    p_p = False

    if mu == 'on':
        m_u = True
        if mu_id == 0:
            mu_id = int(datetime.now().strftime("%y%m%d%H%M%S"))
            p_p = True
    else:
        m_u = False

    if licz:
        p_p = True

    return m_u, mu_id, mu_st, p_p

@login_required(login_url='error')
def comp_add(request, mag):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    stawka = Money(settings.COMP_REPO_ST, EUR)
    admin = False
    f = ''

    if mag == 'mag1':
        f = 'Szparagowa'
    elif mag == 'mag2':
        f = 'Podolany'
    elif mag == 'mag3':
        f = 'MAGAZYN3'

    if request.method == "POST":
        skladf = SkladForm(request.POST, request.FILES or None, stawka=stawka,  mag=f)
        if skladf.is_valid():
            ps = skladf.save(commit=False)
            nr_sde = request.POST.get("nr_sde", "")
            multi_uzycie = request.POST.get("multi_uzycie", "off")
            multi_uzycie_id = request.POST.get("multi_uzycie_id", "")
            multi_uzycie_st = request.POST.get("multi_uzycie_st", "")

            ps.multi_uzycie, ps.multi_uzycie_id, ps.multi_uzycie_st, ps.liczyc = multi_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st, False)

            if len(request.POST.get("faktura", "")) > 0:
                ps.blokada = True
            else:
                ps.blokada = False

            ps.blokada_zapisu = False

            ps.save()
            pk = ps.pk

            CalcDay(pk)
            UpdateDokUwagi(pk, nr_sde)
            #CalcAdd(pk)

            ChangeStatus(nr_sde)
            ##### CalCost(nr_sde, 'n') # t: tak - wyswietlaj dane; n: nie -wyswietlaj

            LOG.add_edit(request, True, Sklad.objects.get(pk=pk))

            return redirect('comp_list', mag=mag)
        else:
            #return redirect('error')
            return render(request, 'COMP_REPO/comp_add.html', {
                'mag': mag,
                'form': skladf,
                'pk': 0,
                'edycja': False,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': 'Dodawanie nowego towaru.'
            })
    else:
        skladf = SkladForm(stawka=stawka, mag=f, d_e=True)

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    return render(request, 'COMP_REPO/comp_add.html', {
        'mag': mag,
        'form': skladf,
        'pk': 0,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': 'Dodawanie nowego towaru.'
    })


@login_required(login_url='error')
def comp_edit(request, pk, mag, det):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    stawka = Money(settings.COMP_REPO_ST, EUR)
    admin = False

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    sk = Sklad.objects.get(pk=pk)
    tst = sk.blokada
    bz = sk.blokada_zapisu
    tst = bz

    m_u = sk.multi_uzycie
    licz = sk.liczyc

    skladm = get_object_or_404(Sklad, pk=pk)
    if request.method == "POST":
        skladf = SkladForm(request.POST or None, request.FILES or None, instance=skladm, stawka=stawka, bz=bz) # initial={'stawka':stawka}
        if skladf.is_valid():
            ps = skladf.save(commit=False)
            nr_sde = request.POST.get("nr_sde", "")
            multi_uzycie = request.POST.get("multi_uzycie", "off")
            multi_uzycie_id = request.POST.get("multi_uzycie_id", "")
            multi_uzycie_st = request.POST.get("multi_uzycie_st", "")


            if admin:
                if len(request.POST.get("faktura", "")) > 0:
                    ps.blokada = True
                else:
                    ps.blokada = False

            if (m_u == False) and (multi_uzycie == "on"):
                print("Wybrano multiużycie - stwórz nową pozycję dla EWU!!!")
                ps.multi_uzycie, ps.multi_uzycie_id, ps.multi_uzycie_st, ps.liczyc = multi_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st, licz)


            if (m_u == True) and (multi_uzycie == "off"):
                print("Skasowano multiużycie - usuń pozycję dla EWU!!!")
                ps.multi_uzycie, ps.multi_uzycie_id, ps.multi_uzycie_st, ps.liczyc = multi_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st, licz)

            ps.save()

            CalcDay(ps.pk)
            UpdateDokUwagi(pk, nr_sde)
            #### CalCost(nr_sde, 't') # t: tak - wyswietlaj dane; n: nie -wyswietlaj

            LOG.add_edit(request, False, Sklad.objects.get(pk=pk))

            return redirect('comp_detail', mag=mag, pk=det, st='^')
        else:
            # return redirect('error')
            return render(request, 'COMP_REPO/comp_add.html', {
                'mag': mag,
                'form': skladf,
                'pk': 0,
                'edycja': True,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'tst': tst,
                'title': 'Edytowanie towaru. [test]'
            })
    else:
        skladf = SkladForm(instance=skladm, stawka=stawka, bz=bz) # initial={'stawka':stawka}

    return render(request, 'COMP_REPO/comp_add.html', {
        'mag': mag,
        'det': det,
        'form': skladf,
        'tst': tst,
        'pk': pk,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': 'Edytowanie towaru.'
    })


@login_required(login_url='error')
def comp_delete(request, pk, mag):
    Sklad.objects.get(pk=pk).delete()
    return redirect('comp_list', mag=mag)


@login_required(login_url='error')
def comp_pdf_sim(request, pk, mag):
    return sklad_pdf_sim_out(request, pk, mag)












#######################################################################################################################

def firma_list(request, mag, fl):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    return render(request, 'COMP_REPO/comp_multi_f.html', {
        'name_log': name_log,
        'about': about,
        'mag': mag,
        'fl': fl
    })


@require_http_methods(["GET", "POST"])
def firma_list_create(request, mag, fl):
    if request.method == 'GET':
        firmy = list(Firma.objects.values())
        return JsonResponse(firmy, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            firma = Firma.objects.create(nazwa=data['nazwa'])
            #print(f"Received data for POST...")
            firma.save()
            return JsonResponse({"id": firma.id, "nazwa": firma.nazwa}, status=201)
        except Exception as e:
            return HttpResponse(status=400)



@require_http_methods(["GET", "POST"])
def firma_detail(request, pk, mag, fl):

    try:
        firma = Firma.objects.get(pk=pk)
    except Firma.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return JsonResponse({"id": firma.id, "nazwa": firma.nazwa})

    data = json.loads(request.body)
    action = data.get('action')

    if action == 'update':
        firma.nazwa = data.get('nazwa', firma.nazwa)
        firma.save()
        return JsonResponse({"id": firma.id, "nazwa": firma.nazwa})

    elif action == 'delete':
        firma.delete()
        return HttpResponse(status=204)


def get_multi_usage_details(request):
    mltid = request.GET.get('mltid')

    # Sprawdzanie, czy mltid jest liczbą większą od zera
    if not mltid or not mltid.isdigit() or int(mltid) <= 0:
        return HttpResponse('<table class="table table-success table-bordered table-condensed" style="width: 100%;">'
                            '<tr><th style="text-align:center;">SDE</th><th style="text-align:center;">Wydanie</th>'
                            '<th style="text-align:center;">Powrót</th></tr>'
                            '<tr><td colspan="3">Brak danych do wyświetlenia.</td></tr></table>',
                            content_type='text/html')

    data = Sklad.objects.filter(multi_uzycie_id=mltid).order_by('id').values('nr_sde__nazwa', 'wydano_data', 'zwroco_data', 'liczyc', 'przech_nrpalet')
    current_date = now().date()  # Pobranie obecnej daty

    # Tworzenie tabeli HTML wewnątrz funkcji
    html_content = '<table style="width: 100%;" class="table table-bordered table-condensed">'
    html_content += ('<tr><th style="text-align:center;">SDE</th><th style="text-align:center;">Wydanie</th><th style="text-align:center;">Powrót</th><th style="text-align:center;">PALETA</th><th style="text-align:center;">P</th></tr>')

    if data:
        for item in data:
            # Sprawdzenie, czy daty nie są None
            wydano = item['wydano_data'] or ''
            zwroco = item['zwroco_data'] or ''
            liczyc = item['liczyc'] or ''
            paleta = item['przech_nrpalet'] or ''

            # Sprawdzenie, czy obecna data zawiera się pomiędzy wydano_data a zwroco_data
            if wydano and zwroco and (wydano <= current_date <= zwroco):
                style = ' style="color:red;font-size: 85%;vertical-align:middle; text-align:center;"'
            else:
                style = ' style="color:gray;font-size: 85%;vertical-align:middle; text-align:center;"'

            lliczyc = ''
            if liczyc:
                lliczyc = '℗'


            html_content += f"<tr><td{style}><strong>{item['nr_sde__nazwa']}</strong></td><td{style}>{wydano}</td><td{style}>{zwroco}</td><td{style}>{paleta}</td><td{style}>{lliczyc}</td></tr>"
    else:
        html_content += '<tr><td colspan="3">Brak danych do wyświetlenia.</td></tr>'

    html_content += '</table>'
    return HttpResponse(html_content, content_type='text/html')


def parse_string(fl):
    if not fl:  # sprawdzamy czy fl jest pusty
        return 1, False  # zwracamy 1 dla int, False dla literowego

    # Używamy wyrażeń regularnych do podziału stringu na część cyfrową i literową
    match = re.match(r"(\d+)(\D*)", fl)
    if match:
        numeric_part = int(match.group(1))  # pierwsza grupa to cyfry
        alpha_part = match.group(2)  # druga grupa to litery
    else:
        # Nie znaleziono cyfr, zwracamy domyślne wartości
        return 1, False

    # Sprawdzamy czy część literowa to 'a'
    is_a = True if alpha_part == 'a' else False

    return numeric_part, is_a


def upgrade_uses():
    # Najpierw resetujemy 'multi_uzycie_st' dla wszystkich rekordów w danym magazynie
    Sklad.objects.filter(multi_uzycie=True).update(multi_uzycie_st=0)

    # # Zliczanie wystąpień każdego 'multi_uzycie_id' z pominięciem wierszy bez daty w 'wydano_data'
    # counts = Sklad.objects.filter(
    #     multi_uzycie=True,
    #     wydano_data__isnull=False  # Filtrujemy, aby pominąć rekordy bez daty
    # ).values('multi_uzycie_id').annotate(count=Count('multi_uzycie_id'))

    counts = Sklad.objects.filter(multi_uzycie=True).values('multi_uzycie_id').annotate(count=Count('multi_uzycie_id'))

    for item in counts:
        # Uaktualniamy 'multi_uzycie_st' dla każdego 'multi_uzycie_id' z pominięciem rekordów bez daty
        Sklad.objects.filter(
            multi_uzycie=True,
            multi_uzycie_id=item['multi_uzycie_id']
        ).update(multi_uzycie_st=item['count'])


def sklad_multi(request, mag, fl):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    t = ''
    sw = False
    opis = ''
    query = ''

    firma = Firma.objects.all()

    fl, is_a = parse_string(fl)
    # Jeśli 'a' to wyświetlane są wszytskie wpisy
    if is_a:
        sklad = Sklad.objects.filter(multi_uzycie=True, firma=fl).order_by('przech_nazwa')
        t = 'Lista wszystkich elementów stoisk wielokrotnego użytku.'
    else:
        try:
            query = request.GET['SZUKAJ']
            opis = "Szukane: " + str(query)
        except:
            opis = ''

        if query != '':
            sw = True
            search_fields = [
                'nr_sde__nazwa', 'nr_sde__targi', 'nr_sde__klient', 'nr_sde__stoisko',
                'przech_nazwa', 'przech_nrpalet', 'czas_od', 'czas_do']
            se = search_filter(search_fields, testQuery(query))
            sklad = Sklad.objects.filter(se).distinct('nr_sde')
            t = opis
        else:
            # Pobieranie najwyższego id dla każdego multi_uzycie_id
            subquery = Sklad.objects.filter(
                multi_uzycie_id=OuterRef('multi_uzycie_id')
            ).values('multi_uzycie_id').annotate(max_id=Max('id')).values('max_id')

            # Filtrujemy główny queryset aby zawierał tylko rekordy z najwyższym id w danej grupie
            sklad = Sklad.objects.filter(
                id=Subquery(subquery[:1]),  # [:1] zwraca pierwszy wynik z subquery
                multi_uzycie=True,
                firma=fl
            ).order_by('przech_nazwa')

            naz = Firma.objects.get(id=fl).nazwa
            t = 'Lista elementów: ' + naz.upper()


    upgrade_uses()


    return render(request, 'COMP_REPO/sklad_multi_n.html', {
        'name_log': name_log,
        'about': about,
        'title': t,
        'sklad': sklad,
        'mag': mag,
        'fl': fl,
        'firma': firma,
        'opis': opis,
        'sw': sw
    })



def update_magazyn_opis():
    # Początek transakcji, aby wszystkie aktualizacje były atomowe
    with transaction.atomic():
        # Pobranie unikalnych wartości nr_sde
        nr_sde_values = Sklad.objects.values_list('nr_sde', flat=True).distinct()

        for nr_sde in nr_sde_values:
            # Dla każdego unikalnego nr_sde, zbierz unikalne wartości magazyn
            unique_magazyny = Sklad.objects.filter(nr_sde=nr_sde).values_list('magazyn', flat=True).distinct()

            # Utworzenie stringa z unikalnych wartości magazyn, oddzielonych przecinkami
            magazyn_opis = ', '.join(unique_magazyny)

            # Aktualizacja magazyn_opis dla wszystkich rekordów z tym nr_sde
            Sklad.objects.filter(nr_sde=nr_sde).update(magazyn_opis=magazyn_opis)



@login_required(login_url='error')
def sklad_list(request, mag):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    rw = True
    admin = False
    st_pr = '^'
    fl = True

    f = ''
    query = ''
    sklad = ''
    sw = False
    t = 'Lista elementów stoisk przechowywanych dla innych firm.'

    # Ustawienie czy API jest tylko do odczytu czy nie
    if grupa == 'produkcja' or grupa == 'kierownik' or grupa == 'magazyn1':
        rw = False

    try:
        query = request.GET['SZUKAJ']
        opis = "Szukane: " + str(query)
    except:
        opis = ''

    if query != '':
        sw = True
        search_fields = [
            'nr_sde__nazwa', 'nr_sde__targi', 'nr_sde__klient', 'nr_sde__stoisko',
            'przech_nazwa', 'przech_nrpalet', 'czas_od', 'czas_do']
        se = search_filter(search_fields, testQuery(query))
        sklad = Sklad.objects.filter(se).distinct('nr_sde')
    else:
        sklad = Sklad.objects.distinct('nr_sde')
        update_magazyn_opis()

    try:
        st = request.GET['STAWKA']
        st = str(st)
        st = st.replace(',', '.')
        wst = Money(st, EUR)
        sde_id = request.GET['SDE_ID']
        sde_id = int(sde_id)
        CalSelSde(sde_id, wst)

        info = "STAWKA - zapis;    sde: " + str(NrSDE.objects.get(pk=sde_id).nazwa) + ", wartość: " + str(wst) + "."
        LOG.zapis_stawka(request, info)
        fl = False
    except:
        st = ''
        sde_id = 0
        # print("COMP_REPO Error: ", "Błąd konwersji !!!")

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    if fl:
        LOG.start(request, query)

    return render(request, 'COMP_REPO/sklad_main.html', {
        'mag': mag,
        'sklad': sklad,
        'name_log': name_log,
        'about': about,
        'title': t,
        'rw': rw,
        'sw': sw,
        'admin': admin,
        'opis': opis,
        'st_pr': st_pr
    })


@login_required(login_url='error')
def sklad_detail(request, mag, pk, st):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    rw = True
    f = ''
    query = ''
    sklad = ''
    sw = False
    admin = False
    nstatus = False
    sum = ""
    nmg = ""
    fl = True
    ndok_pdf1 = ""
    ndok_pdf2 = ""
    ndok_pdf3 = ""
    ndok_pdf4 = ""
    nfv_pdf1 = ""
    nuwagi = ""
    blok_z = ""

    CalCost(pk)

    try:
        nsde = NrSDE.objects.get(pk=pk)
        nnazwa = nsde.nazwa
        ntargi = nsde.targi
        nklient = nsde.klient
        nstoisko = nsde.stoisko
        npm = nsde.pm
    except:
        nnazwa = "..."
        ntargi = ""
        nklient = ""
        nstoisko = ""
        npm = ""

    t = 'Lista elementów stoisk przechowywanych dla SDA ' + str(nnazwa)

    if grupa == 'produkcja' or grupa == 'kierownik':
        rw = False

    # Zamknięcia edycji danych
    if st == 'cs':
        sk = Sklad.objects.filter(nr_sde=pk)
        test = False
        for s in sk:
            test = s.status_pracy
            nmg = s.magazyn
            sum = s.suma
            sum_zw = s.suma_zw
            sum_np = s.suma_np
            s.status_pracy = False
            s.blokada_zapisu = True
            s.save()
        st = '^'

        if test == True:

            komunikat = 'Edycja zakończona.'
            log_info = (komunikat + "   MAGAZYN: " + nmg + "   SDE: " + nnazwa + "   TARGI: " + ntargi + "   KLIENT: "
                        + nklient + "   STOISKO: " + nstoisko + "   KOSZTY: " + str(sum) + "   SUMA_ZW: " + str(sum_zw) + "   SUMA_NP: " + str(sum_np))
            LOG.zakonczenie(request, log_info)

            SendInformation(nmg, nnazwa, ntargi, nklient, nstoisko, sum, sum_zw, sum_np, komunikat, npm)
            test = False
            fl = False

    if st == 'b1':
        sk = Sklad.objects.filter(nr_sde=pk)
        for s in sk:
            s.blokada_zapisu = True
            s.save()
        LOG.zapis_blokada(request, True)
        fl = False

    if st == 'b0':
        sk = Sklad.objects.filter(nr_sde=pk)
        for s in sk:
            s.blokada_zapisu = False
            s.save()
        LOG.zapis_blokada(request, False)
        fl = False

    if int(pk) == int(0):
        sklad = Sklad.objects.filter(nr_sde__isnull=True).order_by('przech_nrpalet').annotate(
            wynik=Case(
                When(status_pracy=False, multi_uzycie=False, then=Value("WYS")),
                When(status_pracy=False, multi_uzycie=True, then=Value("UKR")),
                When(status_pracy=True, then=Value("WYS")),
                output_field=CharField(),
            )
        )

        sorted_sklad = sklad
    else:
        sklad = Sklad.objects.filter(nr_sde=pk).annotate(
            wynik=Case(
                When(status_pracy=False, multi_uzycie=False, then=Value("WYS")),
                When(status_pracy=False, multi_uzycie=True, then=Value("UKR")),
                When(status_pracy=True, then=Value("WYS")),
                output_field=CharField(),
            )
        )

        # Funkcja pomocnicza do sortowania
        def sort_key(value):
            # Rozdzielenie numeru na część cyfrową i alfanumeryczną
            matches = re.match(r"([0-9]+)([a-zA-Z]*)", value.przech_nrpalet)
            number = int(matches.group(1)) if matches else 0
            letters = matches.group(2) if matches else ''
            return (number, letters)

        # Sortowanie wyników
        sorted_sklad = sorted(sklad, key=sort_key)

    try:
        sklads = sklad.first()
        nsuma = sklads.suma
        nsuma_zw = sklads.suma_zw
        nsuma_np = sklads.suma_np
        nuwagi = sklads.uwagi
        ndok_pdf1 = sklads.dok_pdf1.url if sklads.dok_pdf1 else None
        nfv_pdf1 = sklads.fv_pdf1.url if sklads.fv_pdf1 else None
        nsuma_pow = str(sklads.suma_pow) + ' m²'
        nstatus = sklads.status_pracy
        blok_z  = sklads.blokada_zapisu
        data_od = sklads.czas_od
        data_do = sklads.czas_do
        nr_fv   = sklads.faktura
        # print(">>> Odczyt danych do nagłówka")
    except:
        # print("*** Błąd odczytu danych do nagłówka")
        nsuma = '0,00'
        nsuma_pow = '0,0 m²'
        data_od = ''
        data_do = ''
        nr_fv = ''

    upgrade_flags_oper(f, pk)


    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    if fl:
        info = "OKNO SZCZEGÓŁY:   SDE: " + nnazwa + ", Powierzchnia: " + nsuma_pow + ", Koszt: " + str(nsuma) + ", Zwolnione: " + str(nsuma_zw) + ", Bez przypisania: " + str(nsuma_np) + "."
        LOG.start_detail(request, info)

    return render(request, 'COMP_REPO/sklad_detail.html', {
        'det': pk,
        'nnazwa': nnazwa,
        'ntargi': ntargi,
        'nklient': nklient,
        'nstoisko': nstoisko,
        'npm': npm,
        'nsuma_pow': nsuma_pow,
        'nsuma': nsuma,
        'nsuma_zw': nsuma_zw,
        'nuwagi': nuwagi,
        'ndok_pdf1': ndok_pdf1,
        'ndok_pdf2': ndok_pdf2,
        'ndok_pdf3': ndok_pdf3,
        'ndok_pdf4': ndok_pdf4,
        'nfv_pdf1': nfv_pdf1,
        'nsuma_np': nsuma_np,
        'nstatus': nstatus,
        'mag': mag,
        'sklad': sorted_sklad,
        'name_log': name_log,
        'about': about,
        'title': t,
        'rw': rw,
        'sw': sw,
        'admin': admin,
        'blokz': blok_z,
        'data_od': data_od,
        'data_do': data_do,
        'nr_fv': nr_fv
    })


@login_required(login_url='error')
def sklad_detail_up(request, mag, pk, st):
    # Sprawdzenie, czy żądanie jest typu POST oraz czy nagłówek X-Requested-With wskazuje na AJAX
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        data = json.loads(request.body)
        data_od = data.get("data_od", "")
        data_do = data.get("data_do", "")
        nr_fv = data.get("nr_fv", "")
        npoz = data.get("npoz", False)

        sklad = Sklad.objects.filter(nr_sde=pk)

        data_od = datetime.strptime(data_od, "%d.%m.%Y").strftime("%Y-%m-%d")
        data_do = datetime.strptime(data_do, "%d.%m.%Y").strftime("%Y-%m-%d")

        sk = sklad.first()

        fl = False
        if str(sk.czas_od) != data_od:
            fl = True
        if str(sk.czas_do) != data_do:
            fl = True

        if (fl == True) and (npoz == False):
            ChangeStatus(pk)
            CalCost(pk)


        for s in sklad:
            s.czas_od = data_od
            s.czas_do = data_do
            s.faktura = nr_fv
            s.save()


        # Construct the redirect URL and send back to JavaScript
        redirect_url = reverse('comp_detail', kwargs={'mag': mag, 'pk': pk, 'st': st})
        return JsonResponse({"success": True, "redirect_url": redirect_url})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


def upgrade_flags_oper(f, pk):
    nie_nie = 0
    nie_tak = 0
    tak_nie = 0
    tak_tak = 0
    dt_now = date.today()
    shift = 30

    test = Sklad.objects.filter(nr_sde=pk)

    for t in test:
        if t.faktura == '':
            if t.zwolnione == False:
                nie_nie += 1
        if t.faktura != '':
            if t.zwolnione == False:
                tak_nie += 1
        if t.faktura == '':
            if t.zwolnione == True:
                nie_tak += 1
        if t.faktura != '':
            if t.zwolnione == True:
                tak_tak += 1

        t.status = test_data_uslugi(dt_now, t.czas_do, shift)
        t.save()

    stat = 1 # ok
    # FV_ZW
    # print("STAT n_n:", nie_nie," t_n:", tak_nie, " n_t:", nie_tak, " t_t:", tak_tak)

    if nie_nie > 0:
        stat = 0 # Alarm

    for t in Sklad.objects.filter(nr_sde=pk):
        t.flaga_op = stat
        t.save()


def test_data_uslugi(dt_now, dt_in, shift):
    out = -1
    shift = timedelta(days=shift)
    dttest = dt_now + shift

    try:
        dtin = dt_in

        if dtin > dttest:
            out = 0
        if dtin < dttest and dtin > dt_now:
            out = 1
        if dtin < dt_now:
            out = 2
    except:
        out = -1

    return out


def test_data_uslugi_all():
    out = -1
    dt_now = date.today()
    shifti = 30
    shift = timedelta(days=shifti)
    dttest = dt_now + shift

    for t in Sklad.objects.all():

        out = -1
        try:
            dtin = t.czas_do

            if dtin > dttest:
                out = 0
            if dtin < dttest and dtin > dt_now:
                out = 1
            if dtin < dt_now:
                out = 2
        except:
            out = -1

        t.status = out
        t.save()


def multi_user_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st):
    mu = str(multi_uzycie)
    mu_id = int(multi_uzycie_id)
    mu_st = int(multi_uzycie_st)
    if mu == 'on':
        m_u = True
        bd = datetime.now().strftime("%y%m%d%H%M%S")
        if mu_id == 0:
            mu_id = int(bd)

    else:
        m_u = False

    return m_u, mu_id, mu_st


@login_required(login_url='error')
def sklad_add(request, mag):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    stawka = Money(settings.COMP_REPO_ST, EUR)
    admin = False
    f = ''

    if mag == 'mag1':
        f = 'Szparagowa'
    elif mag == 'mag2':
        f = 'Podolany'
    elif mag == 'mag3':
        f = 'MAGAZYN3'

    if request.method == "POST":
        skladf = SkladForm(request.POST, request.FILES or None, stawka=stawka,  mag=f)
        if skladf.is_valid():
            ps = skladf.save(commit=False)
            nr_sde = request.POST.get("nr_sde", "")
            multi_uzycie = request.POST.get("multi_uzycie", "off")
            multi_uzycie_id = request.POST.get("multi_uzycie_id", "")
            multi_uzycie_st = request.POST.get("multi_uzycie_st", "")

            ps.multi_uzycie, ps.multi_uzycie_id, ps.multi_uzycie_st = multi_user_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st)

            if len(request.POST.get("faktura", "")) > 0:
                ps.blokada = True
            else:
                ps.blokada = False

            ps.blokada_zapisu = False

            ps.save()
            pk = ps.pk

            UpdateDokUwagi(pk, nr_sde)

            ChangeStatus(nr_sde)
            ##### CalCost(nr_sde, 'n') # t: tak - wyswietlaj dane; n: nie -wyswietlaj

            LOG.add_edit(request, True, Sklad.objects.get(pk=pk))

            return redirect('sklad_list', mag=mag)
        else:
            #return redirect('error')
            return render(request, 'COMP_REPO/sklad_add.html', {
                'mag': mag,
                'form': skladf,
                'pk': 0,
                'edycja': False,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': 'Dodawanie nowego towaru.'
            })
    else:
        skladf = SkladForm(stawka=stawka, mag=f)

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    return render(request, 'COMP_REPO/sklad_add.html', {
        'mag': mag,
        'form': skladf,
        'pk': 0,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': 'Dodawanie nowego towaru.'
    })


@login_required(login_url='error')
def sklad_edit(request, pk, mag, det):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    stawka = Money(settings.COMP_REPO_ST, EUR)
    admin = False

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    tst = Sklad.objects.get(pk=pk).blokada
    bz = Sklad.objects.get(pk=pk).blokada_zapisu
    tst = bz

    skladm = get_object_or_404(Sklad, pk=pk)
    if request.method == "POST":
        skladf = SkladForm(request.POST or None, request.FILES or None, instance=skladm, stawka=stawka, bz=bz) # initial={'stawka':stawka}
        if skladf.is_valid():
            ps = skladf.save(commit=False)
            nr_sde = request.POST.get("nr_sde", "")
            multi_uzycie = request.POST.get("multi_uzycie", "off")
            multi_uzycie_id = request.POST.get("multi_uzycie_id", "")
            multi_uzycie_st = request.POST.get("multi_uzycie_st", "")

            ps.multi_uzycie, ps.multi_uzycie_id, ps.multi_uzycie_st = multi_user_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st)

            if admin:
                if len(request.POST.get("faktura", "")) > 0:
                    ps.blokada = True
                else:
                    ps.blokada = False

            ps.save()

            UpdateDokUwagi(pk, nr_sde)
            #### CalCost(nr_sde, 't') # t: tak - wyswietlaj dane; n: nie -wyswietlaj

            LOG.add_edit(request, False, Sklad.objects.get(pk=pk))

            return redirect('sklad_detail', mag=mag, pk=det, st='^')
        else:
            # return redirect('error')
            return render(request, 'COMP_REPO/sklad_add.html', {
                'mag': mag,
                'form': skladf,
                'pk': 0,
                'edycja': False,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'tst': tst,
                'title': 'Edytowanie towaru.'
            })
    else:
        skladf = SkladForm(instance=skladm, stawka=stawka, bz=bz) # initial={'stawka':stawka}

#    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
#        admin = True

    #tst = Sklad.objects.get(pk=pk).blokada

    return render(request, 'COMP_REPO/sklad_add.html', {
        'mag': mag,
        'det': det,
        'form': skladf,
        'tst': tst,
        'pk': pk,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': 'Edytowanie towaru.'
    })


@login_required(login_url='error')
def sklad_medit(request, pk, mag, fl):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    stawka = Money(settings.COMP_REPO_ST, EUR)
    admin = False

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    tst = Sklad.objects.get(pk=pk).blokada
    bz = Sklad.objects.get(pk=pk).blokada_zapisu
    sr = Sklad.objects.get(pk=pk) # Dla kopiowania danych do nowego rekordu
    tst = bz


    skladm = get_object_or_404(Sklad, pk=pk)
    if request.method == "POST":
        skladf = SkladForm(request.POST or None, request.FILES or None, instance=skladm, stawka=stawka, bz=bz) # initial={'stawka':stawka}
        if skladf.is_valid():
            ps = skladf.save(commit=False)

            if 'nr_sde' in skladf.changed_data:
                magazyn = request.POST.get("magazyn", "")

                nr_sde = request.POST.get("nr_sde", "")
                try:
                    nr_sde_instance = NrSDE.objects.get(pk=nr_sde)
                except NrSDE.DoesNotExist:
                    nr_sde_instance = None

                przech_nazwa = request.POST.get("przech_nazwa", "")
                przech_nrpalet = request.POST.get("przech_nrpalet", "")
                stawka_0 = request.POST.get("stawka_0", "0.00")
                stawka_1 = request.POST.get("stawka_1", "EUR")
                stawka = Money(stawka_0, stawka_1)
                przech_sze = request.POST.get("przech_sze", "")
                przech_gl = request.POST.get("przech_gl", "")
                multi_uzycie = request.POST.get("multi_uzycie", "off")

                multi_uzycie = True if multi_uzycie == 'on' else False

                multi_uzycie_id = request.POST.get("multi_uzycie_id", "")
                multi_uzycie_st = request.POST.get("multi_uzycie_st", "")
                wydano_ilosc = request.POST.get("wydano_ilosc", "")

                try:
                    wydano_data = request.POST.get("wydano_data", "")
                    wydano_data = datetime.strptime(wydano_data, '%d.%m.%Y').date()
                except ValueError:
                    wydano_data = None
                zwroco_ilosc = request.POST.get("zwroco_ilosc", "")

                try:
                    zwroco_data = request.POST.get("zwroco_data", "")
                    zwroco_data = datetime.strptime(zwroco_data, '%d.%m.%Y').date()
                except ValueError:
                    zwroco_data = None

                zwroco_uwagi = request.POST.get("zwroco_uwagi", "")

                try:
                    czas_od = request.POST.get("czas_od", "")
                    czas_od = datetime.strptime(czas_od, '%d.%m.%Y').date()
                except ValueError:
                    czas_od = None
                try:
                    czas_do = request.POST.get("czas_do", "")
                    czas_do = datetime.strptime(czas_do, '%d.%m.%Y').date()
                except ValueError:
                    czas_do = None

                try:
                    firma = request.POST.get("firma", "")
                    firma = int(firma)
                except ValueError:
                    firma = 1
                firma = Firma.objects.get(id=firma)

                sk = Sklad(
                    magazyn=magazyn, nr_sde=nr_sde_instance, przech_nazwa=przech_nazwa, przech_nrpalet=przech_nrpalet,
                    stawka=stawka, przech_zdjecie=sr.przech_zdjecie, przech_zdjecie2=sr.przech_zdjecie2,
                    przech_zdjecie3=sr.przech_zdjecie3, przech_zdjecie4=sr.przech_zdjecie4, uszkodz_zdjecie1=sr.uszkodz_zdjecie1,
                    uszkodz_zdjecie2=sr.uszkodz_zdjecie2, uszkodz_zdjecie3=sr.uszkodz_zdjecie3, uszkodz_zdjecie4=sr.uszkodz_zdjecie4,
                    przech_sze=przech_sze, przech_gl=przech_gl, multi_uzycie=multi_uzycie, multi_uzycie_id=multi_uzycie_id,
                    multi_uzycie_st=multi_uzycie_st, wydano_ilosc=wydano_ilosc, zwroco_ilosc=zwroco_ilosc,
                    zwroco_uwagi=zwroco_uwagi, czas_od=czas_od, czas_do=czas_do, zwroco_data=zwroco_data, wydano_data=wydano_data,
                    firma=firma
                )
                sk.save()
                #
                ChangeStatus(nr_sde)
                CalCost(nr_sde)
                #


            else:
                nr_sde = request.POST.get("nr_sde", "")
                multi_uzycie = request.POST.get("multi_uzycie", "off")
                multi_uzycie_id = request.POST.get("multi_uzycie_id", "")
                multi_uzycie_st = request.POST.get("multi_uzycie_st", "")

                ps.multi_uzycie, ps.multi_uzycie_id, ps.multi_uzycie_st = multi_user_objects(multi_uzycie, multi_uzycie_id, multi_uzycie_st)

                if admin:
                    if len(request.POST.get("faktura", "")) > 0:
                        ps.blokada = True
                    else:
                        ps.blokada = False

                ps.save()

            ### CalCost(nr_sde)

            return redirect('sklad_multi', mag=mag, fl=fl)
        else:
            # return redirect('error')
            return render(request, 'COMP_REPO/sklad_madd.html', {
                'mag': mag,
                'form': skladf,
                'pk': 0,
                'edycja': False,
                'fl': fl,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': 'Dodawanie lub Edytowanie elementów wielokrotnie używanych.'
            })
    else:
        skladf = SkladForm(instance=skladm, stawka=stawka, bz=bz)


    return render(request, 'COMP_REPO/sklad_madd.html', {
        'mag': mag,
        'form': skladf,
        'tst': tst,
        'pk': pk,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'fl': fl,
        'title': 'Dodawanie lub Edytowanie elementów wielokrotnie używanych.'
    })


@login_required(login_url='error')
def sklad_delete(request, pk, mag):
    Sklad.objects.get(pk=pk).delete()
    return redirect('sklad_list', mag=mag)


@login_required(login_url='error')
def ewu_delete(request, pk, fl, mag):
    Sklad.objects.get(pk=pk).delete()
    return redirect('sklad_multi', mag=mag, fl=fl)


@login_required(login_url='error')
def sklad_pdf(request, pk, mag):
    return sklad_pdf_out(request, pk, mag)


@login_required(login_url='error')
def sklad_pdf_bc(request, pk, mag):
    return sklad_pdf_bc_out(request, pk, mag)


@login_required(login_url='error')
def sklad_pdf_sim(request, pk, mag):
    return sklad_pdf_sim_out(request, pk, mag)


@login_required(login_url='error')
def sklad_pdf_dok(request, fl, sde):
    sklad = Sklad.objects.filter(nr_sde=sde).first()
    print(">>>", sklad)
    return ""

@login_required(login_url='error')
def ewu_pdf_bc(request, pk, mag):
    # Pobieranie najwyższego id dla każdego multi_uzycie_id
    subquery = Sklad.objects.filter(
        multi_uzycie_id=OuterRef('multi_uzycie_id')
    ).values('multi_uzycie_id').annotate(max_id=Max('id')).values('max_id')

    # Filtrujemy główny queryset aby zawierał tylko rekordy z najwyższym id w danej grupie
    sklad = Sklad.objects.filter(
        id=Subquery(subquery[:1]),  # [:1] zwraca pierwszy wynik z subquery
        multi_uzycie=True,
        firma=pk
    ).order_by('przech_nazwa')

    naz = Firma.objects.get(id=pk).nazwa
    naz = naz.upper()

    return ewu_pdf_bc_out(request, pk, mag, sklad, naz)
