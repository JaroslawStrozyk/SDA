from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from simple_search import search_filter

from COMP_REPO.functions import format_european_currency
from ORDERS.models import NrSDE
from TIMBER_WH.forms import PlytaForm, PrzychodForm, RozchodForm, ZwrotForm, PrzychodPzForm
from TIMBER_WH.models import Plyta, Rozchod, Przychod, Zestawienie, Zwrot, Statystyka, RozchodSzczegoly
from ORDERS.functions import test_rok
from .functions import Cal_States_r, check_gr, check_group, testQuery, test_osoba, format_european_currency_pln
from .gen_tables import gen_main_inwent, gen_main_stat, gen_main_inwent_pdf, gen_main_inwent_pdf_data
from .pdf import wz_pdf, pz_pdf, pzw_pdf, ze_pdf, inw_pdf, inw_pdf_data
from django.conf import settings
from moneyed import Money, PLN
from datetime import datetime

from django.db.models import Sum, F, DecimalField


from .xls import ExportAll, ExportByDateRange, ExportByDateRangeAndElement, inw_xls


def timber_exp(request, rok, mag, fl):
    try:
        # Wywołanie funkcji ExportAll
        response = ExportAll(request, rok, fl)
    except ValueError as e:
        # Obsługa błędu przy niepoprawnym roku
        return HttpResponse(f"Błąd: {str(e)}", status=400)

    # Zwrócenie odpowiedzi z plikiem
    return response


def timber_exp_t(request, mag, fl, start_d, stop_d):
    try:

        #print(">>>", start_d, stop_d, type(start_d), type(stop_d))
        # Wywołanie funkcji ExportAll
        response = ExportByDateRange(request, start_d, stop_d, 0)
    except ValueError as e:
        # Obsługa błędu przy niepoprawnym roku
        return HttpResponse(f"Błąd: {str(e)}", status=400)

    # Zwrócenie odpowiedzi z plikiem
    return response

def dok_ze_xls(request, pk, mag, fl, sel):
    print(">>>", pk, mag, fl, sel)
    start_d = "2023-01-01"
    stop_d = "2024-12-29"
    response = ExportByDateRangeAndElement(request, start_d, stop_d, pk, mag, fl, sel)
    return response


# !!!
@login_required(login_url='error')
def timber_list(request, mag, fl):

    name_log, inicjaly, grupa, rw, fls = test_osoba(request, mag, fl)
    about = settings.INFO_PROGRAM
    timber = ''
    idata = datetime.now().strftime("%Y-%m-%d")


    mag1 = False
    mag2 = False
    mag3 = False
    mag4 = False
    mag5 = False
    f = ''

    zero = 0.0
    limit = 10.0
    query = ''
    sw = False

    if mag == 'mag1':
        mag1 = True
        f = 'MAGAZYN1'
    elif mag == 'mag2':
        mag2 = True
        f = 'MAGAZYN2'
    elif mag == 'mag3':
        mag3 = True
        f = 'MAGAZYN3'
    elif mag == 'mag4':
        mag4 = True
        f = 'MAGAZYN4'
    elif mag == 'mag5':
        mag5 = True
        f = 'MAGAZYN5'


    if fl == 'dre':
        t = 'Magazyn płyt drewnianych.'
        m_wew = False
    else:
        t = 'Magazyn wewnętrzny.'
        m_wew = True


    try:
        query = request.GET['SZUKAJ']
        opis = "Szukane: " + str(query)
    except:
        opis = ''

    if query != '':
        sw = True
        search_fields = [
            'nazwa', 'stan', 'opis', 'cena'
        ]
        se = search_filter(search_fields, testQuery(query))
        timber = Plyta.objects.filter(magazyn=f, rodzaj=fl).filter(se).order_by('id')
    else:
        timber = Plyta.objects.filter(magazyn=f, rodzaj=fl).order_by('nazwa')

    return render(request, 'TIMBER_WH/timber_main.html', {
        'fmag': check_gr(request, mag1, mag2, mag3, mag4, mag5),
        'fl': fl,
        'fls': fls,
        'mag': mag,
        'mag1': mag1,
        'mag2': mag2,
        'mag3': mag3,
        'mag4': mag4,
        'mag5': mag5,
        'timber': timber,
        'name_log': name_log,
        'about': about,
        'title': t,
        'zero': zero,
        'limit': limit,
        'opis': opis,
        'sw': sw,
        'rw': rw,
        'm_wew': m_wew,
        'idata': idata
    })


@login_required(login_url='error')
def timber_sda(request, mag, fl, rk):
    name_log = request.user.first_name + " " + request.user.last_name
    lata, rok, brok = test_rok(request)
    about = settings.INFO_PROGRAM
    nrsde = NrSDE.objects.filter(rok=rk).order_by('pk')
    kod_sde = ''
    zero = Money('0.00', PLN)
    suma_d = zero
    suma_w = zero
    wz1 = "MAGAZYN1"
    wz2 = "MAGAZYN2"
    wz3 = "MAGAZYN3"
    opis_sde = ''


    try:
        query = request.GET['NRSDE']
    except:
        query = ''


    if query != '':
        sw = True
        md1 = Rozchod.objects.filter(nr_sde__nazwa=query, plyta__rodzaj='dre').order_by('-pk')
        md2 = Rozchod.objects.filter(nr_sde__nazwa=query, plyta__rodzaj='wew').order_by('-pk')
        for m in md1:
            suma_d += m.kwota
        for m in md2:
            suma_w += m.kwota

        o_sde = NrSDE.objects.get(nazwa=query)

        opis_sde = o_sde.nazwa + " [Klient: " + o_sde.klient + ", Targi: " + o_sde.targi + ", Stoisko: " + o_sde.stoisko + "]"
    else:
        sw = False
        md1 = ''
        md2 = ''


    return render(request, 'TIMBER_WH/timber_sde.html', {
        'name_log': name_log,
        'about': about,
        'title1': 'Magazyn Drewna - Lista pozycji dla SDE ' + kod_sde,
        'title2': 'Magazyn wewnętrzny - Lista pozycji dla SDE ' + kod_sde,
        'zero': zero,
        'fl': fl,
        'mag': mag,
        'rk': rk,
        'nrsde': nrsde,
        'suma_d': suma_d,
        'suma_w': suma_w,
        'sw': sw,
        'md1': md1,
        'md2': md2,
        'wz1': wz1,
        'wz2': wz2,
        'wz3': wz3,
        'opis_sde': opis_sde
    })


@login_required(login_url='error')
def timber_search(request):
    pass


@login_required(login_url='error')
def timber_add(request, mag, fl):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    licz = Plyta.objects.all().last().prod_id

    if request.method == "POST":
        plytaf = PlytaForm(request.POST or None, mag=mag)
        if plytaf.is_valid():
            ps = plytaf.save(commit=False)
            ps.prod_id = licz + 1
            ps.rodzaj = fl
            ps.save()
            return redirect('timber_list', mag=mag, fl=fl)
        else:
            return redirect('error')
    else:

        if fl == 'dre':

            if mag == 'mag1':
                tmag = "Magazynu Szparagowa"

            if mag == 'mag2':
                tmag = "Magazynu Podolany"

            if mag == 'mag3':
                tmag = 'Magazynu u dostawcy'
        else:

            if mag == 'mag1':
                tmag = "Magazynu Szparagowa"

            if mag == 'mag2':
                tmag = "Magazynu Profili"

            if mag == 'mag3':
                tmag = 'Magazynu chemii'

            if mag == 'mag4':
                tmag = 'Magazynu szkła'

            if mag == 'mag5':
                tmag = 'Magazynu stali'


        plytaf = PlytaForm(mag=mag) #initial={'magazyn': tmag},

    return render(request, 'TIMBER_WH/timber_add.html', {
        'fl': fl,
        'mag': mag,
        'form': plytaf,
        'pk': 0,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'title' : 'Dodawanie nowego towaru do '+ tmag
    })


@login_required(login_url='error')
def timber_edit(request, pk, mag, fl):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    plytam = get_object_or_404(Plyta, pk=pk)
    if request.method == "POST":
        plytaf = PlytaForm(request.POST or None, instance=plytam, mag=mag)
        if plytaf.is_valid():
            ps = plytaf.save(commit=False)
            ps.rodzaj = fl
            ps.save()
            return redirect('timber_list', mag=mag, fl=fl)
        else:
            return redirect('error')
    else:

        if mag == 'mag1':
            tmag = "Magazynu Szparagowa"

        if mag == 'mag2':
            tmag = "Magazynu Podolany"

        if mag == 'mag3':
            tmag = 'Magazyn Chemii'

        if mag == 'mag4':
            tmag = 'Magazyn Szkła'

        if mag == 'mag5':
            tmag = 'Magazynu stali'

        plytaf = PlytaForm(instance=plytam, mag=mag)

    return render(request, 'TIMBER_WH/timber_add.html', {
        'fl': fl,
        'mag': mag,
        'form': plytaf,
        'pk': pk,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'title' : 'Edytowanie towaru z ' + tmag
    })


@login_required(login_url='error')
def timber_delete(request, pk, mag, fl):
    Plyta.objects.get(pk=pk).delete()
    return redirect('timber_list', mag=mag, fl=fl)

# !!!
@login_required(login_url='error')
def przychod_list(request, pk, mag, fl):
    name_log, inicjaly, grupa, rw, fls = test_osoba(request, mag, fl)
    about = settings.INFO_PROGRAM
    pl = Plyta.objects.get(pk=pk)
    nazwa = pl.nazwa
    stan  = pl.stan
    opis  = pl.opis
    cena  = pl.cena

    przychod = Przychod.objects.filter(plyta=pk).order_by('-data')

    if fl == 'dre':
        t = 'Przychód płyt drewnianych'
    else:
        t = 'Przychód w magazynie wewnętrznym'

    return render(request, 'TIMBER_WH/przychod_main.html', {
        'fmag': check_group(request,mag),
        'fl': fl,
        'mag': mag,
        'nazwa': nazwa,
        'stan': stan,
        'opis': opis,
        'cena': cena,
        'pk': pk,
        'przychod': przychod,
        'name_log': name_log,
        'about': about,
        'title' : t,
        'rw': rw
    })

# !!!
@login_required(login_url='error')
def przychod_add(request,pk, mag, fl):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    plyta_nazwa = Plyta.objects.get(pk=pk)

    try:
        l = int(Przychod.objects.all().last().doc_id.split(".")[2]) + 1
        lid = "P."+str(plyta_nazwa.prod_id)+"."+str(l)
    except:
        lid = "P."+str(plyta_nazwa.prod_id)+".1"

    if request.method == "POST":
        przychodf = PrzychodForm(request.POST or None)
        if przychodf.is_valid():
            ps = przychodf.save(commit=False)
            ps.doc_id = lid
            ps.plyta = plyta_nazwa
            ps.save()

            pr = Przychod.objects.get(pk=ps.id)
            pr.cena = pr.ilosc * pr.cena_j
            pr.save()

            Cal_States_r(pk, '')

            return redirect('przychod_list', pk=pk, mag=mag, fl=fl)
        else:
            return redirect('error')
    else:
        przychodf = PrzychodForm()

    return render(request, 'TIMBER_WH/przychod_add.html', {
        'fl': fl,
        'mag': mag,
        'form': przychodf,
        'plyta_nazwa': plyta_nazwa,
        'pk': pk,
        'po': 0,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'title' : 'Dodawanie nowej pozycji.'
    })


@login_required(login_url='error')
def timber_pz_add(request, mag, fl):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    # plyta_nazwa = Plyta.objects.get(pk=pk)
    #
    # try:
    #     l = int(Przychod.objects.all().last().doc_id.split(".")[2]) + 1
    #     lid = "P."+str(plyta_nazwa.prod_id)+"."+str(l)
    # except:
    #     lid = "P."+str(plyta_nazwa.prod_id)+".1"

    if request.method == "POST":
        przychodf = PrzychodPzForm(request.POST or None, mag=mag ,rod=fl)
        if przychodf.is_valid():
            ps = przychodf.save(commit=False)
            # ps.doc_id = lid
            # ps.plyta = plyta_nazwa
            ps.save1()

            #Cal_States_r(pk, '')

            return redirect('timber_list', mag=mag, fl=fl)
        # else:
        #     return redirect('error')
    else:
        przychodf = PrzychodPzForm(mag=mag, rod=fl)

    return render(request, 'TIMBER_WH/przychod_pz_add.html', {
        'fl': fl,
        'mag': mag,
        'form': przychodf,
        # 'plyta_nazwa': plyta_nazwa,
        # 'pk': pk,
        # 'po': 0,
        # 'edycja': False,
        'name_log': name_log,
        'about': about,
        'title' : 'Nowa PZ.'
    })

# !!!
@login_required(login_url='error')
def przychod_edit(request, pk, po, mag, fl):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    plyta_nazwa = Plyta.objects.get(pk=pk)

    przychodm = get_object_or_404(Przychod, pk=po)
    if request.method == "POST":
        przychodf = PrzychodForm(request.POST or None, instance=przychodm)
        if przychodf.is_valid():
            ps = przychodf.save(commit=False)
            ps.plyta = plyta_nazwa
            ps.save()

            pr = Przychod.objects.get(pk=ps.id)
            pr.cena = pr.ilosc * pr.cena_j
            pr.save()

            Cal_States_r(pk, '')

            return redirect('przychod_list', pk=pk, mag=mag, fl=fl)
        else:
            return redirect('error')
    else:
        przychodf = PrzychodForm(instance=przychodm)

    return render(request, 'TIMBER_WH/przychod_add.html', {
        'fl': fl,
        'mag': mag,
        'form': przychodf,
        'plyta_nazwa': plyta_nazwa,
        'pk': pk,
        'po': po,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'title' : 'Edytowanie pozycji.'
    })

# !!!
@login_required(login_url='error')
def przychod_delete(request, pk, po, mag, fl):
    Przychod.objects.get(pk=po).delete()

    Cal_States_r(pk, '')

    return redirect('przychod_list', pk=pk, mag=mag, fl=fl)

# !!!
@login_required(login_url='error')
def rozchod_list(request, pk, mag, fl):

    name_log, inicjaly, grupa, rw, fls = test_osoba(request, mag, fl)
    about = settings.INFO_PROGRAM
    pl = Plyta.objects.get(pk=pk)
    nazwa = pl.nazwa
    stan  = pl.stan
    opis  = pl.opis
    cena  = pl.cena

    rozchod = Rozchod.objects.filter(plyta=pk).order_by('-data')

    SDE_None = None

    if fl=='dre':
        t = 'Rozchod płyt drewnianych.'
    else:
        t = 'Rozchód w magazynie wewnętrznym'

    return render(request, 'TIMBER_WH/rozchod_main.html', {
        'fmag': check_group(request, mag),
        'fl': fl,
        'mag': mag,
        'nazwa': nazwa,
        'stan': stan,
        'opis': opis,
        'cena': cena,
        'pk': pk,
        'rozchod': rozchod,
        'name_log': name_log,
        'about': about,
        'title' : t,
        'SDE_None': SDE_None,
        'rw': rw
    })

# !!!
@login_required(login_url='error')
def rozchod_add(request, pk, mag, fl, stan):
    lata, rok, brok = test_rok(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    pl = Plyta.objects.get(pk=pk)
    plyta_nazwa = pl.nazwa
    j_m = pl.jm

    try:
        l = int(Rozchod.objects.all().last().doc_id.split(".")[2]) + 1
        lid = "R."+str(pl.prod_id)+"."+str(l)
    except:
        lid = "R."+str(pl.prod_id)+".1"

    if request.method == "POST":
        rozchodf = RozchodForm(request.POST or None, rok=rok, stan=stan)
        if rozchodf.is_valid():
            nr_sde = request.POST.get("nr_sde", "")
            ps = rozchodf.save(commit=False)
            ps.doc_id = lid
            ps.plyta = pl
            ps.save()

            Cal_States_r(pk, nr_sde)

            return redirect('rozchod_list', pk=pk, mag=mag, fl=fl)
        # else:
        #     return redirect('error')
    else:

        rozchodf = RozchodForm(rok=rok, stan=stan, initial={'jm': j_m}) #rok=brok

    return render(request, 'TIMBER_WH/rozchod_add.html', {
        'fl': fl,
        'mag': mag,
        'form': rozchodf,
        'plyta_nazwa': plyta_nazwa,
        'pk': pk,
        'po': 0,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'title' : 'Rozchód - nowa pozycja.'
    })

# !!!
@login_required(login_url='error')
def rozchod_edit(request, pk, po, mag, fl, stan):
    lata, rok, brok = test_rok(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    pl = Plyta.objects.get(pk=pk)
    plyta_nazwa = pl.nazwa
    j_m = pl.jm

    rozchodm = get_object_or_404(Rozchod, pk=po)
    if request.method == "POST":
        rozchodf = RozchodForm(request.POST or None, instance=rozchodm, rok=rok, stan=stan)
        if rozchodf.is_valid():
            nr_sde = request.POST.get("nr_sde", "")
            ps = rozchodf.save(commit=False)
            ps.plyta = pl
            ps.save()

            # print("KP:", pk, type(pk), nr_sde, type(nr_sde))

            Cal_States_r(pk, nr_sde)

            return redirect('rozchod_list', pk=pk, mag=mag, fl=fl)
        # else:
        #     return redirect('error')
    else:
        rozchodf = RozchodForm(instance=rozchodm, rok=rok, stan=stan, initial={'jm': j_m})

    return render(request, 'TIMBER_WH/rozchod_add.html', {
        'fl':fl,
        'mag': mag,
        'form': rozchodf,
        'plyta_nazwa': plyta_nazwa,
        'pk': pk,
        'po': po,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'title' : 'Rozchód - edycja pozycji.'
    })

# !!!
@login_required(login_url='error')
def rozchod_delete(request, pk, po, mag, fl):
    try:
        nr_sde = Rozchod.objects.get(pk=po).nr_sde.id
    except:
        nr_sde = ''
    Rozchod.objects.get(pk=po).delete()

    Cal_States_r(pk, nr_sde)

    return redirect('rozchod_list', pk=pk, mag=mag, fl=fl)


@login_required(login_url='error')
def zwrot_list(request, pk, mag, fl):

    name_log, inicjaly, grupa, rw, fls = test_osoba(request, mag, fl)
    about = settings.INFO_PROGRAM
    pl = Plyta.objects.get(pk=pk)
    nazwa = pl.nazwa
    stan  = pl.stan
    opis  = pl.opis
    cena  = pl.cena

    zwrot = Zwrot.objects.filter(plyta=pk).order_by('-data')

    SDE_None = None

    if fl=='dre':
        t = 'Zwroty płyt drewnianych.'
    else:
        t = 'Zwrot w magazynie wewnętrznym'

    return render(request, 'TIMBER_WH/zwrot_main.html', {
        'fmag': check_group(request, mag),
        'fl': fl,
        'mag': mag,
        'nazwa': nazwa,
        'stan': stan,
        'opis': opis,
        'cena': cena,
        'pk': pk,
        'zwrot': zwrot,
        'name_log': name_log,
        'about': about,
        'title' : t,
        'SDE_None': SDE_None,
        'rw': rw
    })


@login_required(login_url='error')
def zwrot_add(request, pk, mag, fl):
    lata, rok, brok = test_rok(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    plyta_nazwa = Plyta.objects.get(pk=pk)

    try:
        l = int(Zwrot.objects.all().last().doc_id.split(".")[2]) + 1
        lid = "Z."+str(plyta_nazwa.prod_id)+"."+str(l)
    except:
        lid = "Z."+str(plyta_nazwa.prod_id)+".1"

    if request.method == "POST":
        zwrotf = ZwrotForm(request.POST or None, rok=rok)
        if zwrotf.is_valid():
            nr_sde = request.POST.get("nr_sde", "")
            ps = zwrotf.save(commit=False)
            ps.doc_id = lid
            ps.plyta = plyta_nazwa
            ps.save()

            Cal_States_r(pk, nr_sde)

            return redirect('zwrot_list', pk=pk, mag=mag, fl=fl)
        else:
            return redirect('error')
    else:
        zwrotf = ZwrotForm(rok=rok) #rok=brok

    return render(request, 'TIMBER_WH/zwrot_add.html', {
        'fl': fl,
        'mag': mag,
        'form': zwrotf,
        'plyta_nazwa': plyta_nazwa,
        'pk': pk,
        'po': 0,
        'edycja': False,
        'name_log': name_log,
        'about': about,
        'title' : 'Zwroty - nowa pozycja.'
    })


@login_required(login_url='error')
def zwrot_edit(request, pk, po, mag, fl):
    lata, rok, brok = test_rok(request)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    plyta_nazwa = Plyta.objects.get(pk=pk)

    zwrotm = get_object_or_404(Zwrot, pk=po)
    if request.method == "POST":
        zwrotf = ZwrotForm(request.POST or None, instance=zwrotm, rok=rok)
        if zwrotf.is_valid():
            nr_sde = request.POST.get("nr_sde", "")
            ps = zwrotf.save(commit=False)
            ps.plyta = plyta_nazwa
            ps.save()

            Cal_States_r(pk, nr_sde)

            return redirect('zwrot_list', pk=pk, mag=mag, fl=fl)
        else:
            return redirect('error')
    else:
        zwrotf = RozchodForm(instance=zwrotm, rok=rok) #, rok=brok

    return render(request, 'TIMBER_WH/zwrot_add.html', {
        'fl': fl,
        'mag': mag,
        'form': zwrotf,
        'plyta_nazwa': plyta_nazwa,
        'pk': pk,
        'po': po,
        'edycja': True,
        'name_log': name_log,
        'about': about,
        'title' : 'Zwroty - edyja pozycji'
    })


@login_required(login_url='error')
def zwrot_delete(request, pk, po, mag, fl):
    try:
        nr_sde = Zwrot.objects.get(pk=po).nr_sde.id
    except:
        nr_sde = ''
    Zwrot.objects.get(pk=po).delete()

    Cal_States_r(pk, nr_sde)

    return redirect('zwrot_list', pk=pk, mag=mag, fl=fl)

# !!!
@login_required(login_url='error')
def zestawienie(request, pk, mag, fl, sel):
    name_log = request.user.first_name + " " + request.user.last_name
    lata, rok, brok = test_rok(request)
    about = settings.INFO_PROGRAM
    pl = Plyta.objects.get(pk=pk)
    nazwa = pl.nazwa
    stan  = pl.stan
    opis  = pl.opis
    cena  = pl.cena
    rok_k = brok
    SDE_None = None
    nav1 = False
    nav2 = False
    nav3 = False
    nav4 = False
    out = ''
    wartosc = SDE_None
    zero = Money('00.00', PLN)


    if sel == 'ze':
        out, wartosc, kw, kp, kr = gen_main_view(pk, rok_k)
        nav1 = True
    elif sel == 'pr':
        out, kw, kp, kr = gen_sel_view(sel, pk)
        nav2 = True
    elif sel == 'ro':
        out, kw, kp, kr = gen_sel_view(sel, pk)
        nav3 = True
    elif sel == 'zw':
        out, kw, kp, kr = gen_sel_view(sel, pk)
        nav4 = True

    nrsde = NrSDE.objects.all().order_by('-pk')

    # print("KW", kw, type(kw))
    # print("KP", kp, type(kp))
    # print("KR", kr, type(kr))

    # kw = format_european_currency_pln(kw)
    # kp = format_european_currency_pln(kp)
    # kr = format_european_currency_pln(kr)

    return render(request, 'TIMBER_WH/zestawienie.html', {
        'fl': fl,
        'mag': mag,
        'nazwa': nazwa,
        'stan': stan,
        'opis': opis,
        'cena': cena,
        'pk': pk,
        'out': out,
        'name_log': name_log,
        'about': about,
        'title' : 'Zestawienie operacji dla: ' + pl.nazwa,
        'SDE_None': SDE_None,
        'wartosc': wartosc,
        'nav1': nav1,
        'nav2': nav2,
        'nav3': nav3,
        'nav4': nav4,
        'sel': sel,
        'nrsde': nrsde,
        'viewm': True,
        'kw': kw,
        'kr': kr,
        'kp': kp
    })


@login_required(login_url='error')
def zest_search(request, pk, mag, fl, sel):
    name_log = request.user.first_name + " " + request.user.last_name
    lata, rok, brok = test_rok(request)
    about = settings.INFO_PROGRAM
    pl = Plyta.objects.get(pk=pk)
    nazwa = pl.nazwa
    stan  = pl.stan
    opis  = pl.opis
    cena  = pl.cena
    rok_k = brok
    SDE_None = None
    nav1 = False
    nav2 = False
    nav3 = False
    nav4 = False
    viewm = True
    out = ''
    wartosc = SDE_None


    if request.method == "GET":
        try:
            query = request.GET['NRSDE']
            sel = query
        except:
            sel = 'ze'



    if sel == 'ze':
        out, wartosc, kw, kp, kr = gen_main_view(pk, rok_k)
        nav1 = True
    elif sel == 'pr':
        out, kw, kp, kr = gen_sel_view(sel, pk)
        nav2 = True
    elif sel == 'ro':
        out, kw, kp, kr = gen_sel_view(sel, pk)
        nav3 = True
    elif sel == 'zw':
        out, kw, kp, kr = gen_sel_view(sel, pk)
        nav4 = True
    else:
        out, kw, kp, kr = gen_sel_view(sel, pk)
        viewm = False

    nrsde = NrSDE.objects.all().order_by('-pk')

    return render(request, 'TIMBER_WH/zestawienie.html', {
        'fl': fl,
        'mag': mag,
        'nazwa': nazwa,
        'stan': stan,
        'opis': opis,
        'cena': cena,
        'pk': pk,
        'out': out,
        'name_log': name_log,
        'about': about,
        'title' : 'Zestawienie opreacji dla: ' + pl.nazwa,
        'SDE_None': SDE_None,
        'wartosc': wartosc,
        'nav1': nav1,
        'nav2': nav2,
        'nav3': nav3,
        'nav4': nav4,
        'sel': sel,
        'nrsde': nrsde,
        'viewm': viewm,
        'kw': kw,
        'kr': kr,
        'kp': kp
    })


@login_required(login_url='error')
def timber_stat(request, rk, mag, fl):
    name_log = request.user.first_name + " " + request.user.last_name
    lata, rok, brok = test_rok(request)
    about = settings.INFO_PROGRAM

    out,  m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12 = gen_main_stat(brok) # nie_przypisana,

    return render(request, 'TIMBER_WH/timber_stat.html', {
        'fl': fl,
        'mag': mag,
        'name_log': name_log,
        'about': about,
        'title': 'Statystyka rozłożenia kosztów SDE z podziałem na miesiące za rok ' + str(rk),
        'out': out,
        # 'out_np': Money(str(nie_przypisana),PLN),
        'zero': Money('0.00', PLN),
        'SDE_None': None,
        'm1': m1,
        'm2': m2,
        'm3': m3,
        'm4': m4,
        'm5': m5,
        'm6': m6,
        'm7': m7,
        'm8': m8,
        'm9': m9,
        'm10': m10,
        'm11': m11,
        'm12': m12,
    })


@login_required(login_url='error')
def timber_inwentura(request, rk, mag, fl):
    name_log = request.user.first_name + " " + request.user.last_name
    lata, rok, brok = test_rok(request)
    about = settings.INFO_PROGRAM
    zero = Money('0.00', PLN)
    mag1_suma = zero
    mag2_suma = zero
    mag3_suma = zero
    brok = rk

    out1, out2, out3 = gen_main_inwent(brok) # gen_main_inwent_pdf(brok) # gen_main_inwent(brok)
    # for o in out1:
    #     print(o)

    for o in out1:
        mag1_suma += o['suma_wart']

    for o in out2:
        mag2_suma += o['suma_wart']

    for o in out3:
        mag3_suma += o['suma_wart']

    # print(">>> mag1_suma: ", mag1_suma, " mag2_suma: ", mag2_suma, " mag3_suma: ", mag3_suma)

    return render(request, 'TIMBER_WH/timber_inw.html', {
        'fl': fl,
        'mag': mag,
        'rk': rk,
        'name_log': name_log,
        'about': about,
        'zero': Money('0.00', PLN),
        'title1': 'Zestawienie magazynu Szparagowa.',
        'title2': 'Zestawienie magazynu Podolany.',
        'title3': 'Zestawienie magazynu u Dostawcy.',
        'out1': out1,
        'out2': out2,
        'out3': out3,
        'mag1_suma': mag1_suma,
        'mag2_suma': mag2_suma,
        'mag3_suma': mag3_suma
    })


def dok_wz_pdf(request, pk, po):
    return wz_pdf(request, pk, po)


def dok_pz_pdf(request, pk, po):
    return pz_pdf(request, pk, po)


def dok_pzw_pdf(request, pk, po):
    return pzw_pdf(request, pk, po)


def dok_inw_pdf(request, rk, mag, fl):
    out1, out2, out3 = gen_main_inwent_pdf(rk)
    if mag == 'mag1':
        out = out1
    elif mag == 'mag2':
        out = out2
    else:
        out = out3
    return inw_pdf(request,mag, out)


def dok_inw_xls(request, rk, mag, fl):
    out1, out2, out3 = gen_main_inwent(rk) # gen_main_inwent_pdf(rk)
    if mag == 'mag1':
        out = out1
    elif mag == 'mag2':
        out = out2
    else:
        out = out3
    return inw_xls(request,mag, out)





def dok_inw_pdf_data(request, rk, mag, fl, dt):

    gdt = datetime.strptime(dt, "%Y-%m-%d").date()

    out1, out2, out3 = gen_main_inwent_pdf_data(rk,gdt)
    if mag == 'mag1':
        out = out1
    elif mag == 'mag2':
        out = out2
    else:
        out = out3
    return inw_pdf_data(request,mag, out, dt)

# !!!
def dok_ze_pdf(request, pk, mag, fl, sel):
    return ze_pdf(request, pk, mag, fl, sel)

# !!!
def gen_main_view(pk, rok_k):

    zero = Money('00.00', PLN)
    Zestawienie.objects.all().delete()
    kw, kp, kr = zero, zero, zero

    przychod = Przychod.objects.filter(plyta=pk)
    rozchod = Rozchod.objects.filter(plyta=pk) #, rokk=rok_k)

    for p in przychod:
        kp += p.cena

    for r in rozchod:
        kr += r.kwota

    kw = kp - kr

    for p in przychod:
        o = Zestawienie(dok_id=p.doc_id, rokk=rok_k, plyta=p.plyta, data=p.data, operacja='Przychód', opis=p.zrodlo, ilosc=p.ilosc, jm=p.jm, kwota=p.cena)
        o.save()

    for r in rozchod:
        o = Zestawienie(dok_id=r.doc_id, rokk=rok_k, plyta=r.plyta, data=r.data, operacja='Rozchód', opis=r.cel, ilosc=r.ilosc, jm=r.jm, kwota=r.kwota, nr_sde=r.nr_sde)
        o.save()

    out = Zestawienie.objects.all().order_by('-data')
    wartosc = Zestawienie.objects.filter(operacja='Rozchód', nr_sde=None).aggregate(Sum('kwota'))
    wartosc = wartosc['kwota__sum']


    return out, wartosc, kw, kp, kr

# !!!
def gen_sel_view(sel, pk):
    zero = Money('00.00', PLN)
    kw, kp, kr = zero, zero, zero
    przychod = Przychod.objects.filter(plyta=pk)
    rozchod = Rozchod.objects.filter(plyta=pk) #, rokk=rok_k)

    for p in przychod:
        kp += p.cena

    for r in rozchod:
        kr += r.kwota

    kw = kp - kr

    if sel == 'pr':
        out = Zestawienie.objects.filter(operacja='Przychód').order_by('-data')
    elif sel == 'ro':
        out = Zestawienie.objects.filter(operacja='Rozchód').order_by('-data')
    elif sel == 'zw':
        out = Zestawienie.objects.filter(operacja='Zwrot').order_by('-data')
    else:
        out = Zestawienie.objects.filter(nr_sde__nazwa=sel).order_by('-data')
    return out, kw, kp, kr


################################################################################

def generuj_raport_konsola():
    plyty = Plyta.objects.filter(magazyn='MAGAZYN1') # .all()
    for plyta in plyty:
        # Obliczanie sumy ilości i wartości przychodów
        przychody = plyta.przychod_set.annotate(
            wartosc=F('ilosc') * F('cena_j')
        ).aggregate(
            ilosc_sum=Sum('ilosc'),
            wartosc_sum=Sum('wartosc', output_field=DecimalField())
        )

        # Obliczanie sumy ilości i wartości rozchodów
        rozchody = RozchodSzczegoly.objects.filter(rozchod__plyta=plyta).aggregate(
            ilosc_sum=Sum('ilosc'),
            wartosc_sum=Sum('kwota', output_field=DecimalField())
        )

        # Obliczanie stanu magazynowego
        stan_obecny = (przychody['ilosc_sum'] or 0) - (rozchody['ilosc_sum'] or 0)
        wartosc_obecna = (przychody['wartosc_sum'] or 0) - (rozchody['wartosc_sum'] or 0)

        print(f"Płyta: {plyta.nazwa}")
        print(f"  Stan obecny: {stan_obecny}")
        print(f"  Wartość obecna: {wartosc_obecna}")
        print(f"  Łączne przychody: {przychody['ilosc_sum'] or 0}")
        print(f"  Łączne rozchody: {rozchody['ilosc_sum'] or 0}")
        print("-" * 40)



