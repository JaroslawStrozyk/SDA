from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from moneyed import Money, EUR
from ORDERS.models import NrSDE
from .forms import SkladForm, SkladFormD, EKForm, OKForm, SkladFormDet
from .functions import CalCost, test_osoba, testQuery, ChangeStatus, SendInformation, CalCostGen, CalSelSde
from .models import Sklad, Firma, ElementKatalogowy, OkresPrzechowywania
from simple_search import search_filter
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Firma, HistoriaPalety
import json
from django.db.models import F
from django.db.models import Max, Min, Sum, Count, Q, Case, When, BooleanField, Value, Exists, OuterRef, Subquery, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .calc_func import UpgradeSum, force_recalculation, update_element_katalogowy_status, UpgradeDependence, update_summary, UpgradeDependence
from .pdf import sklad_pdf_out, sklad_pdf_bc_out, sklad_pdf_sim_out, ewu_pdf_bc_out, nkat_pdf_out


def set_status_pracy(pk, st):
    sk = Sklad.objects.get(id=pk).nr_sde
    Sklad.objects.filter(nr_sde=sk).update(status_pracy=st)


@login_required(login_url='error')
def ncomp_list(request, mag):
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
        # sklad = Sklad.objects.filter(se).distinct('nr_sde_id')
        sklad = Sklad.objects.filter(se).order_by('nr_sde_id').distinct('nr_sde_id')
    else:
        sklad = Sklad.objects.all().order_by('nr_sde_id', 'id').distinct('nr_sde_id')
        for s in sklad:
            UpgradeSum(s.nr_sde_id)
            #print(">>> ", s.id)


        # Znajdź minimalne ID dla każdego nr_sde
        min_ids = Sklad.objects.values('nr_sde').annotate(min_id=Min('id')).values_list('min_id', flat=True)

        # Pobierz rekordy z tymi ID
        sklad = Sklad.objects.filter(id__in=min_ids)

        # Funkcja pomocnicza do ekstrakcji klucza sortowania
        def extract_sort_key(sklad_item):
            nr_sde_str = str(sklad_item.nr_sde.nazwa)  # Konwertujemy na string na wszelki wypadek
            nr, rok = nr_sde_str.split('_')  # Rozdzielamy na numer i rok
            return int(rok), int(nr)  # Zwracamy jako tuple do sortowania (rok, numer)

        # Sortowanie zmiennej sklad
        sklad = sorted(sklad, key=extract_sort_key, reverse=True)

        # update_magazyn_opis()

    try:
        st = request.GET['STAWKA']
        st = str(st)
        st = st.replace(',', '.')
        wst = Money(st, EUR)
        sde_id = request.GET['SDE_ID']
        sde_id = int(sde_id)
        CalSelSde(sde_id, wst)

        info = "STAWKA - zapis;    sde: " + str(NrSDE.objects.get(pk=sde_id).nazwa) + ", wartość: " + str(wst) + "."
        # LOG.zapis_stawka(request, info)
        fl = False
    except:
        st = ''
        sde_id = 0
        #print("COMP_REPO Error: ", "Błąd konwersji !!!")

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    if fl:
        pass
        # LOG.start(request, query)

    return render(request, 'COMP_REPO_NEW/comp_main.html', {
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
def ncomp_detail(request, mag, pk, st):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    rw = True
    sw = False
    admin = False
    st_sum = False
    sum = ""
    nmg = ""
    ndok_pdf1 = ""
    ndok_pdf2 = ""
    ndok_pdf3 = ""
    ndok_pdf4 = ""
    nfv_pdf1 = ""
    nuwagi = ""
    blok_z = ""

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

    # Test i Zamknięcia edycji danych
    if st == 'cs':
        zero = Money('00.00', EUR)
        sk = Sklad.objects.filter(nr_sde=pk)
        st = sk.first().stawka
        # print("SK.SKLADKA: ", st, zero)
        if st == zero:
            stat = 2
        else:
            stat = 3

        for s in sk:
            s.status_pracy = stat
            s.save()
        st = '^'

        # if test == True:
        #
        #     komunikat = 'Edycja zakończona.'
        #     log_info = (komunikat + "   MAGAZYN: " + nmg + "   SDE: " + nnazwa + "   TARGI: " + ntargi + "   KLIENT: "
        #                 + nklient + "   STOISKO: " + nstoisko + "   KOSZTY: " + str(sum) + "   SUMA_ZW: " + str(sum_zw) + "   SUMA_NP: " + str(sum_np))
        #     # LOG.zakonczenie(request, log_info)
        #
        #     SendInformation(nmg, nnazwa, ntargi, nklient, nstoisko, sum, sum_zw, sum_np, komunikat, npm)
        #     test = False
        #     fl = False

    if st == 'b1':
        sk = Sklad.objects.filter(nr_sde=pk)
        for s in sk:
            s.blokada_zapisu = True
            s.save()
        # LOG.zapis_blokada(request, True)
        fl = False

    if st == 'b0':
        sk = Sklad.objects.filter(nr_sde=pk)
        for s in sk:
            s.blokada_zapisu = False
            s.save()
        # LOG.zapis_blokada(request, False)
        fl = False


    # Główne wywołanie danych
    sklad = Sklad.objects.filter(nr_sde=pk).order_by('przech_nrpalet')

    UpgradeSum(pk)

    try:
        sklads = sklad.first()
        nsuma = sklads.suma
        nsumazw = sklads.suma_zw.amount
        if nsumazw > 0.00:
            st_sum = True
        else:
            st_sum = False

        nsuma_pow = str(sklads.suma_pow) + ' m²'
        nuwagi = sklads.uwagi
        ndok_pdf1 = sklads.dok_pdf1.url if sklads.dok_pdf1 else None
        ndok_pdf2 = sklads.dok_pdf2.url if sklads.dok_pdf2 else None
        ndok_pdf3 = sklads.dok_pdf3.url if sklads.dok_pdf3 else None
        ndok_pdf4 = sklads.dok_pdf4.url if sklads.dok_pdf4 else None

        if sklads.okres and sklads.okres.fv_pdf and sklads.okres.fv_pdf.url:
            nfv_pdf1 = sklads.okres.fv_pdf.url
        else:
            nfv_pdf1 = ""

        firma_pk = sklads.firma.id    if sklads.firma.id else 0
        firma_n  = sklads.firma.nazwa if sklads.firma.nazwa else None
        nstatus = sklads.status_pracy if sklads.status_pracy else 0
        
    except:
        print("*** Błąd odczytu danych do nagłówka")
        return redirect('ncomp_list', mag=mag)
        nsuma = '0,00'
        nsuma_pow = '0,0 m²'
        nstatus = 0


    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True



    return render(request, 'COMP_REPO_NEW/comp_detail.html', {
        'det': pk,
        'pk': pk,
        'nnazwa': nnazwa,
        'ntargi': ntargi,
        'nklient': nklient,
        'nstoisko': nstoisko,
        'npm': npm,
        'nsuma_pow': nsuma_pow,
        'nsuma': nsuma,
        'st_sum': st_sum,
        'nuwagi': nuwagi,
        'ndok_pdf1': ndok_pdf1,
        'ndok_pdf2': ndok_pdf2,
        'ndok_pdf3': ndok_pdf3,
        'ndok_pdf4': ndok_pdf4,
        'nfv_pdf1': nfv_pdf1,
        'nstatus': nstatus,
        'mag': mag,
        'sklad': sklad,
        'name_log': name_log,
        'about': about,
        'title': t,
        'rw': rw,
        'sw': sw,
        'admin': admin,
        'blokz': blok_z,
        'firma_pk': firma_pk,
        'firma_n': firma_n
    })


@login_required(login_url='error')
def ncomp_add(request, mag):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    admin = False

    title = 'Dodawanie nowego towaru.'

    # Pobieramy ID firmy z parametru GET lub sesji, jeśli istnieje
    firma_id = request.GET.get('firma_id', None)
    if not firma_id and 'firma_id' in request.session:
        firma_id = request.session.get('firma_id')

    if request.method == "POST":
        skladf = SkladForm(request.POST, request.FILES or None)
        if skladf.is_valid():
            ps = skladf.save(commit=False)

            ps.blokada_zapisu = False

            ps.save()

            # Ustawienie STATUS na poziom "EDYCJA" - zoptymalizowana wersja
            set_status_pracy(ps.pk, 1)

            return redirect('ncomp_list', mag=mag)
        else:
            return render(request, 'COMP_REPO_NEW/comp_add.html', {
                'mag': mag,
                'form': skladf,
                'pk': 0,
                'edycja': False,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': title
            })
    else:
        # Przekazujemy ID firmy do formularza przy jego tworzeniu
        skladf = SkladForm(firma_id=firma_id)

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    return render(request, 'COMP_REPO_NEW/comp_add.html', {
        'mag': mag,
        'form': skladf,
        'pk': 0,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': title
    })


@login_required(login_url='error')
def ncomp_add_d(request, mag, pk, id):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    admin = False
    fi = Firma.objects.get(pk=id).nazwa
    sk = Sklad.objects.filter(nr_sde=pk).first().nr_sde.nazwa

    title = 'Dodawanie nowego towaru dla '

    # Pobieramy ID firmy z parametru GET lub sesji, jeśli istnieje
    firma_id = request.GET.get('firma_id', None)
    if not firma_id and 'firma_id' in request.session:
        firma_id = request.session.get('firma_id')

    if request.method == "POST":
        skladf = SkladFormDet(request.POST, request.FILES or None)
        if skladf.is_valid():
            ps = skladf.save(commit=False)
            ps.blokada_zapisu = False
            ps.save()

            # Ustawienie STATUS na poziom "EDYCJA" - zoptymalizowana wersja
            set_status_pracy(ps.pk, 1)

            return redirect('ncomp_detail', mag=mag, pk=pk, st='^')
        else:
            return render(request, 'COMP_REPO_NEW/comp_add_d.html', {
                'mag': mag,
                'form': skladf,
                'pk': pk,
                'edycja': False,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': title
            })
    else:
        # Przekazujemy ID firmy do formularza przy jego tworzeniu
        skladf = SkladFormDet(firma_id=firma_id, sde_pk=pk, firma_pk=id)

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    return render(request, 'COMP_REPO_NEW/comp_add_d.html', {
        'mag': mag,
        'form': skladf,
        'pk': pk,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': title,
        'fi': fi,
        'sk': sk
    })


@login_required(login_url='error')
def get_filtered_data(request):
    """
    Widok zwracający przefiltrowane dane dla okresu i elementu katalogowego
    na podstawie wybranej firmy.
    """
    firma_id = request.GET.get('firma_id')

    if not firma_id or int(firma_id) <= 1:
        # Wszystkie rekordy dla indeksu 0 lub 1
        okresy = []
        for okres in OkresPrzechowywania.objects.all():
            okresy.append({
                'id': okres.id,
                'display_text': f"{okres.nazwa} ({okres.data_od.strftime('%d.%m.%Y')} - {okres.data_do.strftime('%d.%m.%Y')})"
            })

        elementy = []
        for element in ElementKatalogowy.objects.all():
            elementy.append({
                'id': element.id,
                'display_text': f"{element.nazwa} - {element.opis}"
            })
    else:
        # Filtrowanie rekordów dla konkretnej firmy
        okresy = []
        for okres in OkresPrzechowywania.objects.filter(firma_id=firma_id):
            okresy.append({
                'id': okres.id,
                'display_text': f"{okres.nazwa} ({okres.data_od.strftime('%d.%m.%Y')} - {okres.data_do.strftime('%d.%m.%Y')})"
            })

        elementy = []
        for element in ElementKatalogowy.objects.filter(firma_id=firma_id):
            elementy.append({
                'id': element.id,
                'display_text': f"{element.nazwa} - {element.opis}"
            })

    return JsonResponse({
        'okresy': okresy,
        'elementy': elementy
    })


@login_required(login_url='error')
def ncomp_edit(request, pk, mag, det):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    admin = False

    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True

    sk = Sklad.objects.get(pk=pk)

    # Zapisz poprzedni stan okresu, aby wykryć zmianę
    poprzedni_okres_id = sk.okres_id if sk.okres else None

    bz = sk.blokada_zapisu
    tst = bz

    skladm = get_object_or_404(Sklad, pk=pk)
    if request.method == "POST":
        skladf = SkladForm(request.POST or None, request.FILES or None, instance=skladm)
        if skladf.is_valid():
            ps = skladf.save(commit=False)

            # Wykryj, czy okres został dodany podczas edycji
            nowy_okres_id = ps.okres_id if ps.okres else None
            zmiana_okresu = poprzedni_okres_id != nowy_okres_id

            # Zapisz rekord
            ps.save()

            # Ustawienie STATUS na poziom "EDYCJA" - zoptymalizowana wersja
            set_status_pracy(ps.pk, 1)

            # Jeżeli okres został dodany lub zmieniony, wymuś przeliczenie
            if zmiana_okresu and nowy_okres_id is not None:
                force_recalculation(ps.pk)

            return redirect('ncomp_detail', mag=mag, pk=det, st='^')
        else:
            # return redirect('error')
            return render(request, 'COMP_REPO_NEW/comp_add.html', {
                'mag': mag,
                'form': skladf,
                'pk': 0,
                'edycja': True,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'tst': tst,
                'title': 'Edytowanie towaru.'
            })
    else:
        skladf = SkladForm(instance=skladm)

    return render(request, 'COMP_REPO_NEW/comp_add.html', {
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
def ncomp_doc_edit(request, mag, det):
    title = 'Edycja dokumentów.'
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    stawka = Money(settings.COMP_REPO_ST, EUR)
    admin = False
    if inicjaly == 'J.S.' or inicjaly == 'D.K.':
        admin = True
    sk = Sklad.objects.filter(nr_sde=det).first()
    bz = sk.blokada_zapisu
    tst = bz
    skladm = get_object_or_404(Sklad, pk=sk.id)
    if request.method == "POST":
        skladf = SkladFormD(request.POST or None, request.FILES or None, instance=skladm)
        if skladf.is_valid():
            ps = skladf.save(commit=False)

            # Pobierz uwagi z POST
            d_uwagi = request.POST.get("uwagi", "")

            # Sprawdź, czy mamy zazanaczone pola "clear" dla plików
            clear_dok_pdf1 = request.POST.get("dok_pdf1-clear") == "on"
            clear_dok_pdf2 = request.POST.get("dok_pdf2-clear") == "on"
            clear_dok_pdf3 = request.POST.get("dok_pdf3-clear") == "on"
            clear_dok_pdf4 = request.POST.get("dok_pdf4-clear") == "on"
            clear_fv_pdf1 = request.POST.get("fv_pdf1-clear") == "on"

            # Pobierz pliki z FILES jeśli istnieją
            d_dok_pdf1 = request.FILES.get("dok_pdf1", None)
            d_dok_pdf2 = request.FILES.get("dok_pdf2", None)
            d_dok_pdf3 = request.FILES.get("dok_pdf3", None)
            d_dok_pdf4 = request.FILES.get("dok_pdf4", None)
            d_fv_pdf1 = request.FILES.get("fv_pdf1", None)

            # Zapisz zaktualizowany rekord
            ps.uwagi = d_uwagi

            # Zastosuj pliki lub wyczyść pola
            if d_dok_pdf1:
                ps.dok_pdf1 = d_dok_pdf1
            elif clear_dok_pdf1:
                ps.dok_pdf1 = None

            if d_dok_pdf2:
                ps.dok_pdf2 = d_dok_pdf2
            elif clear_dok_pdf2:
                ps.dok_pdf2 = None

            if d_dok_pdf3:
                ps.dok_pdf3 = d_dok_pdf3
            elif clear_dok_pdf3:
                ps.dok_pdf3 = None

            if d_dok_pdf4:
                ps.dok_pdf4 = d_dok_pdf4
            elif clear_dok_pdf4:
                ps.dok_pdf4 = None

            if d_fv_pdf1:
                ps.fv_pdf1 = d_fv_pdf1
            elif clear_fv_pdf1:
                ps.fv_pdf1 = None

            ps.save()

            # Zaktualizuj pozostałe rekordy o tym samym nr_sde
            for skl in Sklad.objects.filter(nr_sde=det).exclude(pk=ps.pk):
                skl.uwagi = d_uwagi

                # Zastosuj takie same zmiany dla pozostałych rekordów
                if d_dok_pdf1:
                    skl.dok_pdf1 = d_dok_pdf1
                elif clear_dok_pdf1:
                    skl.dok_pdf1 = None

                if d_dok_pdf2:
                    skl.dok_pdf2 = d_dok_pdf2
                elif clear_dok_pdf2:
                    skl.dok_pdf2 = None

                if d_dok_pdf3:
                    skl.dok_pdf3 = d_dok_pdf3
                elif clear_dok_pdf3:
                    skl.dok_pdf3 = None

                if d_dok_pdf4:
                    skl.dok_pdf4 = d_dok_pdf4
                elif clear_dok_pdf4:
                    skl.dok_pdf4 = None

                if d_fv_pdf1:
                    skl.fv_pdf1 = d_fv_pdf1
                elif clear_fv_pdf1:
                    skl.fv_pdf1 = None

                skl.save()

            return redirect('ncomp_detail', mag=mag, pk=det, st='^')
        else:
            return render(request, 'COMP_REPO_NEW/comp_doc_edit.html', {
                'mag': mag,
                'form': skladf,
                'edycja': True,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'tst': tst,
                'title': title
            })
    else:
        skladf = SkladFormD(instance=skladm)
    return render(request, 'COMP_REPO_NEW/comp_doc_edit.html', {
        'mag': mag,
        'det': det,
        'form': skladf,
        'tst': tst,
        'pk': 0,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': title
    })


@login_required(login_url='error')
def ncomp_delete(request, pk, mag, det):

    sk = Sklad.objects.get(pk=pk)

    el = ElementKatalogowy.objects.get(id=sk.element_katalogowy_id)
    el.aktywny = False
    el.save()

    sk.delete()

    return redirect('ncomp_detail', mag=mag, pk=det, st='^')


# PRZYCISKI Z GÓRNEJ BELKI

def nfirma_list(request, mag, fl):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    return render(request, 'COMP_REPO_NEW/comp_firma.html', {
        'name_log': name_log,
        'about': about,
        'mag': mag,
        'fl': fl
    })


@require_http_methods(["GET", "POST"])
def nfirma_list_create(request, mag, fl):
    if request.method == 'GET':
        #firmy = list(Firma.objects.values())
        firmy = list(Firma.objects.order_by('nazwa').values())
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
def nfirma_detail(request, pk, mag, fl):

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


@login_required(login_url='error')
def nkat_lista(request, mag, st, zm):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    t = "Katalog przechowywanych elementów."
    # firma = Firma.objects.all().order_by('nazwa')
    firma = Firma.objects.annotate(
        custom_order=Case(
            When(pk=1, then=Value(0)),  # Firma z pk=1 będzie pierwsza
            default=Value(1),  # Wszystkie inne firmy mają niższy priorytet
            output_field=IntegerField(),
        )
    ).order_by('custom_order', 'nazwa')  # Najpierw wg priorytetu, potem wg nazwy
    if zm == '0':
        zmk = True
    else:
        zmk = False
    # Aktualizacja pól wydany i licznik w ElementKatalogowy
    update_element_katalogowy_status()
    try:
        query = request.GET['SZUKAJ']
    except:
        query = ''
    if query != '':
        search_fields = ['nazwa', 'opis']
        se = search_filter(search_fields, testQuery(query))
        if st == '0' or st == '1':
            katalog = ElementKatalogowy.objects.filter(aktywny=zmk).filter(se)
            sw = False
            opis = ''
        else:
            katalog = ElementKatalogowy.objects.filter(firma=st, aktywny=zmk).filter(se)
            sw = True
            opis = ' - ' + Firma.objects.get(pk=st).nazwa + ' - ' + query
    else:
        if st == '0':
            katalog = ElementKatalogowy.objects.all()
            sw = False
            opis = ''
            t = 'Katalog wszystkich przechowywanych elementów.'
        elif st == '1':
            katalog = ElementKatalogowy.objects.filter(aktywny=zmk).order_by('firma', 'nazwa')
            sw = False
            opis = ''
        else:
            katalog = ElementKatalogowy.objects.filter(firma=st, aktywny=zmk)
            sw = True
            t = 'Elementy dla: '
            opis = Firma.objects.get(pk=st).nazwa

    # ZOPTYMALIZOWANY KOD: Pobierz dane o paletach jednym zapytaniem
    katalog_ids = list(katalog.values_list('id', flat=True))

    # Jedno zapytanie dla wszystkich najnowszych palet
    ostatnie_palety = {}
    if katalog_ids:
        # Subquery dla najnowszej daty każdego składu
        newest_dates = HistoriaPalety.objects.filter(
            sklad__element_katalogowy__in=katalog_ids
        ).values('sklad_id').annotate(
            max_date=Max('data_zmiany')
        )

        # Pobierz najnowsze palety na podstawie dat
        for item in newest_dates:
            najnowsza = HistoriaPalety.objects.filter(
                sklad_id=item['sklad_id'],
                data_zmiany=item['max_date']
            ).first()
            if najnowsza:
                element_id = najnowsza.sklad.element_katalogowy_id
                if element_id not in ostatnie_palety:
                    ostatnie_palety[element_id] = najnowsza.numer_palety

    # Dodaj pola nr_palety do elementów
    for element in katalog:
        element.nr_palety = ostatnie_palety.get(element.id, '-')

    # Dodajemy paginację tylko dla st=='1'
    if st > '0':
        page = request.GET.get('page', 1)
        paginator = Paginator(katalog, 100)  # 100 elementów na stronę, możesz dostosować
        try:
            katalog_paginated = paginator.page(page)
        except PageNotAnInteger:
            katalog_paginated = paginator.page(1)
        except EmptyPage:
            katalog_paginated = paginator.page(paginator.num_pages)
        return render(request, 'COMP_REPO_NEW/comp_kat_lista.html', {
            'st': st,
            'mag': mag,
            'katalog': katalog_paginated,
            'name_log': name_log,
            'about': about,
            'title': t,
            'firma': firma,
            'sw': sw,
            'opis': opis,
            'zm': zm,
            'zmk': zmk,
            'is_paginated': True,
            'paginator': paginator
        })
    else:
        return render(request, 'COMP_REPO_NEW/comp_kat_lista.html', {
            'st': st,
            'mag': mag,
            'katalog': katalog,
            'name_log': name_log,
            'about': about,
            'title': t,
            'firma': firma,
            'sw': sw,
            'opis': opis,
            'zm': zm,
            'zmk': zmk,
            'is_paginated': False
        })











#
# @login_required(login_url='error')
# def nkat_lista(request, mag, st, zm):
#     name_log, inicjaly, grupa = test_osoba(request)
#     about = settings.INFO_PROGRAM
#     t = "Katalog przechowywanych elementów."
#     # firma = Firma.objects.all().order_by('nazwa')
#     firma = Firma.objects.annotate(
#         custom_order=Case(
#             When(pk=1, then=Value(0)),  # Firma z pk=1 będzie pierwsza
#             default=Value(1),  # Wszystkie inne firmy mają niższy priorytet
#             output_field=IntegerField(),
#         )
#     ).order_by('custom_order', 'nazwa')  # Najpierw wg priorytetu, potem wg nazwy
#     if zm == '0':
#         zmk = True
#     else:
#         zmk = False
#     # Aktualizacja pól wydany i licznik w ElementKatalogowy
#     update_element_katalogowy_status()
#     try:
#         query = request.GET['SZUKAJ']
#     except:
#         query = ''
#     if query != '':
#         search_fields = ['nazwa', 'opis']
#         se = search_filter(search_fields, testQuery(query))
#         if st == '0' or st == '1':
#             katalog = ElementKatalogowy.objects.filter(aktywny=zmk).filter(se)
#             sw = False
#             opis = ''
#         else:
#             katalog = ElementKatalogowy.objects.filter(firma=st, aktywny=zmk).filter(se)
#             sw = True
#             opis = ' - ' + Firma.objects.get(pk=st).nazwa + ' - ' + query
#     else:
#         if st == '0':
#             katalog = ElementKatalogowy.objects.all()
#             sw = False
#             opis = ''
#             t = 'Katalog wszystkich przechowywanych elementów.'
#         elif st == '1':
#             katalog = ElementKatalogowy.objects.filter(aktywny=zmk).order_by('firma', 'nazwa')
#             sw = False
#             opis = ''
#         else:
#             katalog = ElementKatalogowy.objects.filter(firma=st, aktywny=zmk)
#             sw = True
#             t = 'Elementy dla: '
#             opis = Firma.objects.get(pk=st).nazwa
#
#     # NOWY KOD: Dodanie informacji o paletach i historii do elementów katalogowych
#     for element in katalog:
#         # Pobierz wszystkie składy związane z tym elementem katalogowym
#         sklady = Sklad.objects.filter(element_katalogowy=element)
#         sklad_ids = [sklad.id for sklad in sklady]
#
#         # Pobierz ostatni wpis z HistoriaPalety (najnowszy) dla pola nr_palety
#         if sklad_ids:
#             ostatnia_paleta = HistoriaPalety.objects.filter(
#                 sklad__id__in=sklad_ids
#             ).order_by('-data_zmiany').first()
#
#             element.nr_palety = ostatnia_paleta.numer_palety if ostatnia_paleta else '-'
#
#             # Pobierz wszystkie unikalne numery palet z historii dla pola historia
#             wszystkie_palety = HistoriaPalety.objects.filter(
#                 sklad__id__in=sklad_ids
#             ).values_list('numer_palety', flat=True).distinct()
#
#             # Sortuj i połącz w ciąg
#             if wszystkie_palety:
#                 # Filtruj puste wartości i sortuj
#                 palety_list = [p for p in wszystkie_palety if p]
#                 try:
#                     # Próbuj sortować numerycznie
#                     palety_sorted = sorted(palety_list, key=lambda x: (int(''.join(filter(str.isdigit, x)) or '0'), x))
#                 except:
#                     # Jeśli nie da się numerycznie, sortuj alfabetycznie
#                     palety_sorted = sorted(palety_list)
#                 element.historia = ', '.join(palety_sorted)
#             else:
#                 element.historia = '-'
#         else:
#             element.nr_palety = '-'
#             element.historia = '-'
#
#     # Dodajemy paginację tylko dla st=='1'
#     if st > '0':
#         page = request.GET.get('page', 1)
#         paginator = Paginator(katalog, 100)  # 100 elementów na stronę, możesz dostosować
#         try:
#             katalog_paginated = paginator.page(page)
#         except PageNotAnInteger:
#             katalog_paginated = paginator.page(1)
#         except EmptyPage:
#             katalog_paginated = paginator.page(paginator.num_pages)
#         return render(request, 'COMP_REPO_NEW/comp_kat_lista.html', {
#             'st': st,
#             'mag': mag,
#             'katalog': katalog_paginated,
#             'name_log': name_log,
#             'about': about,
#             'title': t,
#             'firma': firma,
#             'sw': sw,
#             'opis': opis,
#             'zm': zm,
#             'zmk': zmk,
#             'is_paginated': True,
#             'paginator': paginator
#         })
#     else:
#         return render(request, 'COMP_REPO_NEW/comp_kat_lista.html', {
#             'st': st,
#             'mag': mag,
#             'katalog': katalog,
#             'name_log': name_log,
#             'about': about,
#             'title': t,
#             'firma': firma,
#             'sw': sw,
#             'opis': opis,
#             'zm': zm,
#             'zmk': zmk,
#             'is_paginated': False
#         })
#


@login_required(login_url='error')
def nkat_add(request, mag, st, zm):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    admin = False

    title = 'Dodawanie nowego elementu.'

    if request.method == "POST":
        ekf = EKForm(request.POST, request.FILES or None)
        if ekf.is_valid():
            ps = ekf.save(commit=False)

            ps.blokada_zapisu = False
            ps.save()
            pk = ps.pk

            return redirect('nkat_el', mag=mag, st=st, zm=zm)
        else:
            return render(request, 'COMP_REPO_NEW/comp_kat_add.html', {
                'mag': mag,
                'st':st,
                'form': ekf,
                'pk': 0,
                'zm': zm,
                'edycja': False,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': title
            })
    else:
        ekf = EKForm(st=st)

    return render(request, 'COMP_REPO_NEW/comp_kat_add.html', {
        'mag': mag,
        'st': st,
        'form': ekf,
        'pk': 0,
        'zm': zm,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': title
    })


@login_required(login_url='error')
def nkat_edit(request, pk, mag, st, zm):
    title = 'Edycja elementu.'
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    admin = False

    ekm = get_object_or_404(ElementKatalogowy, pk=pk)
    if request.method == "POST":
        ekf = EKForm(request.POST or None, request.FILES or None, instance=ekm)
        if ekf.is_valid():
            ps = ekf.save(commit=False)
            ps.save()

            return redirect('nkat_el', mag=mag, st=st, zm=zm)
        else:
            return render(request, 'COMP_REPO_NEW/comp_kat_add.html', {
                'mag': mag,
                'st': st,
                'form': ekf,
                'pk': pk,
                'zm': zm,
                'edycja': True,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': title
            })
    else:
        ekf = EKForm(instance=ekm)
    return render(request, 'COMP_REPO_NEW/comp_kat_add.html', {
        'mag': mag,
        'st': st,
        'form': ekf,
        'pk': pk,
        'zm': zm,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': title
    })


@login_required(login_url='error')
def nkat_delete(request, pk, mag, st, zm):
    ElementKatalogowy.objects.get(pk=pk).delete()
    return redirect('nkat_el', mag=mag, st=st, zm=zm)


@login_required(login_url='error')
def nokr_lista(request, mag, fl, zm):
    name_log, inicjaly, grupa = test_osoba(request)
    about = settings.INFO_PROGRAM
    title = 'Okresy przechowywania'

    # Zapytanie dla firmy z optymalizacją sortowania
    firma = Firma.objects.annotate(
        custom_order=Case(
            When(pk=1, then=Value(0)),  # Firma z pk=1 będzie pierwsza
            default=Value(1),  # Wszystkie inne firmy mają niższy priorytet
            output_field=IntegerField(),
        )
    ).order_by('custom_order', 'nazwa')  # Najpierw wg priorytetu, potem wg nazwy

    if zm == '0':
        zmk = False
    else:
        zmk = True

    sw = False

    if fl == '0' or fl == '1':
        # Dla pierwszego wywołania, dodatkowo wykonaj sprawdzenie dat
        from django.utils import timezone

        # Pobierz dzisiejszą datę
        today = timezone.now().date()

        # Pobierz wszystkie okresy przechowywania
        op = OkresPrzechowywania.objects.all().annotate(
            pm=Min('sklad__nr_sde__pm')
        ).filter(zamkniety=zmk).order_by('firma', 'nazwa')

        # Lista do przechowywania obiektów do zbiorczej aktualizacji
        okresy_do_aktualizacji = []

        # Aktualizacja wartości pola stan w oparciu o obliczoną różnicę dni
        for okres in op:
            if okres.data_do is None:
                okres.stan = 0  # Brak daty
            else:
                delta = (okres.data_do - today).days
                if delta > 14:
                    okres.stan = 1  # Ponad 60 dni
                elif 0 <= delta <= 14:
                    okres.stan = 2  # Między 30 a 60 dni
                else:  # delta < 30 lub ujemna
                    okres.stan = 3  # Mniej niż 30 dni lub data już minęła
            okresy_do_aktualizacji.append(okres)

        # Zbiorcza aktualizacja wszystkich obiektów - znacznie szybsza niż pojedyncze zapisywanie
        if okresy_do_aktualizacji:
            from django.db import transaction
            with transaction.atomic():
                for okres in okresy_do_aktualizacji:
                    okres.save(update_fields=['stan'])

        sw = False
        title = 'Wszystkie okresy przechowywania'
        opis = ''
    else:
        # Standardowe zapytanie dla wybranej firmy, bez aktualizacji pola 'stan'
        op = OkresPrzechowywania.objects.all().annotate(
            pm=Min('sklad__nr_sde__pm')
        ).filter(firma=fl, zamkniety=zmk).order_by('firma', 'nazwa')

        sw = True
        title = 'Okresy przechowywania dla: '
        opis = Firma.objects.get(pk=fl).nazwa

    return render(request, 'COMP_REPO_NEW/comp_okres_list.html', {
        'name_log': name_log,
        'about': about,
        'fl': fl,
        'zm': zm,
        'zmk': zmk,
        'title': title,
        'op': op,
        'mag': mag,
        'firma': firma,
        'opis': opis,
        'sw': sw
    })


def get_sklad_by_okres(request):
    """
    Widok API do pobierania elementów Składu powiązanych z danym Okresem Przechowywania.
    Zwraca dane w formacie JSON, zgrupowane wg nr_sde z sumowaniem pola suma i powierzchnia.
    """
    # Pobierz ID okresu z parametrów GET
    okres_id = request.GET.get('okres_id')

    if not okres_id:
        return JsonResponse([], safe=False)

    # Pobierz elementy Składu dla danego okresu
    wszystkie_sklady = Sklad.objects.filter(okres_id=okres_id)
    i = 0
    for ws in wszystkie_sklady:
        i += 1
        # print(">>> " + str(i) + " ", ws.stawka, ws.koszt_przech, ws.suma, ws.nr_sde, ws.okres, ws.element_katalogowy)

    # Grupowanie po nr_sde (jeśli nr_sde jest None, traktuj jako oddzielną grupę)
    sklady_by_sde = {}

    for sklad in wszystkie_sklady:
        # Użyj ID nr_sde jako klucza, lub 'none' jeśli nr_sde jest None
        key = sklad.nr_sde.id if sklad.nr_sde else 'none'

        if key not in sklady_by_sde:
            # Inicjalizacja dla nowego nr_sde
            nr_sde_nazwa = str(sklad.nr_sde) if sklad.nr_sde else '-'
            sklady_by_sde[key] = {
                'nr_sde_id': key,
                'nr_sde_nazwa': nr_sde_nazwa,
                'magazyny': set([sklad.magazyn]),  # Używamy set dla unikalnych magazynów
                'elementy': [],
                'suma_total': 0,
                'powierzchnia_total': float(sklad.przech_pow) if sklad.przech_pow else 0,
                'flaga': sklad.flaga_op
            }
        else:
            # Dodaj magazyn do zbioru unikalnych magazynów
            sklady_by_sde[key]['magazyny'].add(sklad.magazyn)
            # Dodaj powierzchnię
            if sklad.przech_pow:
                sklady_by_sde[key]['powierzchnia_total'] += float(sklad.przech_pow)

        # Dodaj pojedynczy element
        sklady_by_sde[key]['elementy'].append({
            'id': sklad.id,
            'przech_nazwa': sklad.przech_nazwa,
            'suma': str(sklad.suma)
        })

        # Dodajemy wartości do sumy
        # Konwertujemy Money do float dla obliczeń
        try:
            sklady_by_sde[key]['suma_total'] += float(sklad.koszt_przech.amount)
        except (ValueError, AttributeError):
            # Ignoruj błędy konwersji - mogą wystąpić jeśli suma to None
            pass



    # Przygotuj dane do zwrócenia w odpowiedzi JSON
    data = []
    for sde_key, sde_data in sklady_by_sde.items():
        # Formatuj sumy do wyświetlania (z symbolem waluty)
        waluta = 'EUR'  # Domyślna waluta z modelu
        if wszystkie_sklady.exists():
            pierwszy_sklad = wszystkie_sklady.first()
            waluta = pierwszy_sklad.suma.currency if hasattr(pierwszy_sklad.suma, 'currency') else 'EUR'

        # Dodaj informacje o zgrupowanych Składach do listy
        data.append({
            'nr_sde_nazwa': sde_data['nr_sde_nazwa'],
            'magazyn': ', '.join(sorted(sde_data['magazyny'])),  # Lista magazynów rozdzielonych przecinkami
            'liczba_elementow': len(sde_data['elementy']),
            'powierzchnia': f"{sde_data['powierzchnia_total']:.1f} m²",  # Formatowanie z jednym miejscem po przecinku
            'suma': f"{sde_data['suma_total']:.2f} {waluta}",
            'flaga': sde_data['flaga']
        })


    return JsonResponse(data, safe=False)


@login_required(login_url='error')
def nokr_add(request, mag, fl, zm):
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    admin = False

    title = 'Dodawanie nowego okresu.'

    if request.method == "POST":
        okf = OKForm(request.POST, request.FILES or None)
        if okf.is_valid():
            ps = okf.save(commit=False)

            ps.blokada_zapisu = False
            ps.save()
            pk = ps.pk

            return redirect('nokr_lista', mag=mag, fl=fl, zm=zm)
        else:
            return render(request, 'COMP_REPO_NEW/comp_okr_add.html', {
                'mag': mag,
                'fl':fl,
                'zm': zm,
                'form': okf,
                'pk': 0,
                'edycja': False,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': title
            })
    else:
        okf = OKForm(st=fl)

    return render(request, 'COMP_REPO_NEW/comp_okr_add.html', {
        'mag': mag,
        'fl': fl,
        'zm': zm,
        'form': okf,
        'pk': 0,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': title
    })


@login_required(login_url='error')
def nokr_edit(request, pk, mag, fl, zm):
    title = 'Edycja okresu.'
    name_log, inicjaly, grupa = test_osoba(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    admin = False

    okm = get_object_or_404(OkresPrzechowywania, pk=pk)
    if request.method == "POST":
        okf = OKForm(request.POST or None, request.FILES or None, instance=okm)
        if okf.is_valid():
            ps = okf.save(commit=False)
            ps.save()

            UpgradeDependence(ps.id)

            return redirect('nokr_lista', mag=mag, fl=fl, zm=zm)
        else:
            return render(request, 'COMP_REPO_NEW/comp_okr_add.html', {
                'mag': mag,
                'fl': fl,
                'zm': zm,
                'form': okf,
                'pk': pk,
                'edycja': True,
                'name_log': name_log,
                'about': about,
                'admin': admin,
                'title': title
            })
    else:
        okf = OKForm(instance=okm)
    return render(request, 'COMP_REPO_NEW/comp_okr_add.html', {
        'mag': mag,
        'fl': fl,
        'zm': zm,
        'form': okf,
        'pk': pk,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'admin': admin,
        'title': title
    })


@login_required(login_url='error')
def nokr_delete(request, mag, fl, pk, zm):
    OkresPrzechowywania.objects.get(pk=pk).delete()
    return redirect('nokr_lista', mag=mag, fl=fl, zm=zm)


@login_required(login_url='error')
def comp_pdf_sim(request, pk, mag):
    return sklad_pdf_sim_out(request, pk, mag)


# Okno główne - widok SDE
@login_required(login_url='error')
def sklad_pdf(request, pk, mag):
    return sklad_pdf_out(request, pk, mag)

# Okno główne - widok SDE
@login_required(login_url='error')
def sklad_pdf_bc(request, pk, mag):
    return sklad_pdf_bc_out(request, pk, mag)


@login_required(login_url='error')
def nkat_pdf(request, pk, mag):
    return nkat_pdf_out(request, pk, mag)
