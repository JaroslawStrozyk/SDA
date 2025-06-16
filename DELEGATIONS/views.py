from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from simple_search import search_filter
from CARS.models import Auto
from ORDERS.models import NrSDE
from .calculate import extractNumber, rozliczDelegacje, CalcCurrency, CalcRow, test_rok
from .models import Delegacja, Dieta, Pozycja
from .forms import DelegacjaForm, EDelegacjaForm, RDelegacjaForm, PozycjaForm, DietaForm
from django.conf import settings
from .pdf import delegacja_pdf_pw, delegacja_pdf_out
from datetime import datetime
from moneyed import Money, PLN
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db.models import F
from datetime import date


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
    return name_log, inicjaly


def test_user(request):
    gr = ''
    tst = False
    flw = False
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        gr = g.name

    if gr == 'kierownik' or gr == 'produkcja' or gr == 'magazyn':
        tst = True

    if gr == 'administrator' or gr == 'ksiegowosc' or gr == 'ksiegowosc1':
        flw = True
    return tst, flw


def deleg_to_sde():
    D = Delegacja.objects.filter(Q(kod_sde_targi1__isnull=False) | Q(kod_sde_targi2__isnull=False))

    zero = Money('00.0', PLN)

    NrSDE.objects.filter(rokk__gte=2022).update(deleg_sum=zero)

    updates = {}
    for r in D:
        if r.kod_sde_targi1:
            updates[r.kod_sde_targi1_id] = updates.get(r.kod_sde_targi1_id, 0) + r.sde_targi1_pln
        if r.kod_sde_targi2:
            updates[r.kod_sde_targi2_id] = updates.get(r.kod_sde_targi2_id, 0) + r.sde_targi2_pln

    for pk, sum in updates.items():
        NrSDE.objects.filter(pk=pk).update(deleg_sum=F('deleg_sum') + sum)


def convert_to_number_and_type(s):
    try:
        return (True, float(s)) if '.' in s else (False, int(s))
    except ValueError:
        return (False, s)

@login_required(login_url='error')
def delegacja_lista(request):

    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tst, flw = test_user(request)
    n_i, inic = test_osoba(request)


    if tst:
        #n_i, inic = test_osoba(request)
        fl_mask = False
        lista_delegacje = Delegacja.objects.filter(osoba__naz_imie=n_i) # .order_by('-numer') #('zrobione', '-data_od') naz_imie
        lista_delegacje = sorted(lista_delegacje, key=lambda x: convert_to_number_and_type(x.numer), reverse=True)

    else:
        fl_mask = True
        # lista_delegacje = Delegacja.objects.all().order_by('-numer') # 'zrobione', '-data_od')
        lista_delegacje = Delegacja.objects.all()
        lista_delegacje = sorted(lista_delegacje, key=lambda x: convert_to_number_and_type(x.numer), reverse=True)

    paginator = Paginator(lista_delegacje, 30)
    strona = request.GET.get('page')
    delegacje = paginator.get_page(strona)

    deleg_to_sde()

    return render(request, 'DELEGATIONS/delegacja.html', {
        'delegacje': delegacje,
        'name_log': name_log,
        'about': about,
        'fl_mask': fl_mask,
        'title' : 'Lista poleceń wyjazdu służbowego.',
        'flw': flw
    })

# ???
def ConwertInit(naz_imie):
    imie = ''
    nazwisko = ''

    if naz_imie != "":
        sp = naz_imie.split()
        imie = sp[0]
        nazwisko = sp[1]

    return imie, nazwisko


def delegacja_add(request, fl):
    flg = False
    if fl == 'log':
        flg = True

    if request.method == "POST":
        delf = DelegacjaForm(request.POST)

        if delf.is_valid():
            post = delf.save(commit=False)
            post.zrobione = False
            post.numer = extractNumber()
            data_od = request.POST.get("data_od")
            data_do = request.POST.get("data_do")
            post.dc_rozpo    = datetime.strptime(data_od, '%d.%m.%Y')
            post.dc_zakon    = datetime.strptime(data_do, '%d.%m.%Y')
            post.przekr_gran = datetime.strptime(data_od, '%d.%m.%Y')
            post.powrot_kraj = datetime.strptime(data_do, '%d.%m.%Y')
            post.save()
            if fl == 'log':
                return redirect('login')
            else:
                return redirect('delegacja_lista')
        else:
            pass
    else:
        delf = DelegacjaForm()
    return render(request, 'DELEGATIONS/delegacja_add.html', {
        'form':delf,
        'flg': flg,
    })


@login_required(login_url='error')
def delegacja_edit(request, pk):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    delz = get_object_or_404(Delegacja, pk=pk)
    if request.method == "POST":
        delf = EDelegacjaForm(request.POST or None, instance=delz)
        if delf.is_valid():
            post = delf.save(commit=False)
            post.save()
            return redirect('delegacja_lista')
    else:
        delf = EDelegacjaForm(instance=delz)
    return render(request, 'DELEGATIONS/delegacja_edit.html', {
        'form':delf,
        'name_log': name_log,
        'about': about,
        'pk': pk
    })

def delegacja_delete(request, pk):
    Delegacja.objects.get(pk=pk).delete()
    return redirect('delegacja_lista')

@login_required(login_url='error')
def delegacja_search(request):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tst, flw = test_user(request)
    #print(">>>>", flw)
    title = 'Lista poleceń wyjazdu służbowego. Szukana fraza: '

    if request.method == "GET":
        query = request.GET['SZUKAJ']
        title += query
        if query == '' or query == ' ':
            return redirect('delegacja_lista')
        search_fields = ['osoba__naz_imie', 'targi', 'lok_targi', 'cel_wyj', 'transport']
        f = search_filter(search_fields, query)
        fdelegacje = Delegacja.objects.filter(f)

        fdelegacje = sorted(fdelegacje, key=lambda x: convert_to_number_and_type(x.numer), reverse=True)

        if tst:
            fl_mask = False
        else:
            fl_mask = True

        paginator = Paginator(fdelegacje, 30)
        strona = request.GET.get('page')
        delegacje = paginator.get_page(strona)


        return render(request, 'DELEGATIONS/delegacja.html',{
            'delegacje': delegacje,
            'wybrany': query,
            'name_log': name_log,
            'about': about,
            'title': title,
            'fl_mask': fl_mask,
            'flw': flw
        })
    else:
        return redirect('delegacja_lista')



@login_required(login_url='error')
def delegacja_pw(request, pk):
    d = Delegacja.objects.get(id=pk)
    d.pobrane_pw = True
    d.save()
    return delegacja_pdf_pw(request, pk)


@login_required(login_url='error')
def delegacja_dieta(request):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    dieta = Dieta.objects.all().order_by('panstwo')

    return render(request, 'DELEGATIONS/delegacja_dieta.html', {
        'dieta': dieta,
        'name_log': name_log,
        'about': about,
        'title': 'Lista stawek diet i noclegów.'
    })


@login_required(login_url='error')
def delegacja_dieta_edit(request, pk):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    delz = get_object_or_404(Dieta, pk=pk)
    if request.method == "POST":
        delf = DietaForm(request.POST or None, instance=delz)
        if delf.is_valid():
            post = delf.save(commit=False)
            post.save()
            return redirect('delegacja_dieta')
    else:
        delf = DietaForm(instance=delz)
    return render(request, 'DELEGATIONS/delegacja_dieta_edit.html', {
        'form':delf,
        'name_log': name_log,
        'about': about
    })






#################################################
#
#
#################################################
@login_required(login_url='error')
def delegacja_rz(request, pk):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul = 'Rozliczenie wyjazdu służbowego.'

    rozliczDelegacje(pk)

    rozliczenie_del = Delegacja.objects.get(pk=pk)
    pozycje1 = Pozycja.objects.filter(delegacja=pk, waluta='PLN')
    pozycje2 = Pozycja.objects.filter(delegacja=pk, waluta='EUR')
    pozycje3 = Pozycja.objects.filter(delegacja=pk, waluta='GBP')
    pozycje4 = Pozycja.objects.filter(delegacja=pk, waluta='USD')
    pozycje5 = Pozycja.objects.filter(delegacja=pk, waluta='CHF')

    fkraj = False
    if rozliczenie_del.lok_targi=='Polska':
        fkraj = True

    fdata_kurs = True
    if rozliczenie_del.kurs_data==None:
        fdata_kurs = False

    fdata_kursz = True
    if rozliczenie_del.kurs_dataz==None:
        fdata_kursz = False

    fwartosc = False
    if rozliczenie_del.dieta_za_euro == Money('0.00', 'EUR'):
        fwartosc = True

    # Sprawdzanie godziny
    dc = rozliczenie_del.dc_rozpo
    flaga_rozli = not (dc.hour == 0 and dc.minute == 0 and dc.second == 0)


    return render(request, 'DELEGATIONS/delegacja_detail.html', {
        'delegacja': rozliczenie_del,
        'fwartosc': fwartosc,
        'pozycje1': pozycje1,
        'pozycje2': pozycje2,
        'pozycje3': pozycje3,
        'pozycje4': pozycje4,
        'pozycje5': pozycje5,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'fkraj': fkraj,
        'fdata_kurs': fdata_kurs,
        'fdata_kursz': fdata_kursz,
        'flaga_rozli': flaga_rozli,
        'tnull': None
    })


def delegacja_rz_out(request,pk):
    return delegacja_pdf_out(request, pk)


def delegacja_rz_out_z(request,pk):
    delegacja = Delegacja.objects.get(id=pk)
    delegacja.zrobione = True
    delegacja.save()
    #print(Delegacja.objects.get(id=pk))
    return delegacja_pdf_out(request, pk)


@login_required(login_url='error')
def rdelegacja_edit(request, pk):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    error = ""

    delz = get_object_or_404(Delegacja, pk=pk)
    # Ustawienie aktualnej daty przed przekazaniem do formularza
    delz.data_rozl = date.today()
    if request.method == "POST":
        delf = RDelegacjaForm(request.POST or None, instance=delz)

        if delf.is_valid():
            post = delf.save(commit=False)
            post.save()

            rozliczDelegacje(pk)
            return redirect('delegacja_rz', pk=pk)
        else:
            error = delf.errors
    else:
        delf = RDelegacjaForm(instance=delz)


    iin = str(delz) # delz.naz_imie
    targi = delz.targi
    ltargi = delz.lok_targi
    num_dok = delz.numer
    lt = True
    if ltargi=="Polska":
        lt = False

    return render(request, 'DELEGATIONS/delegacja_redit.html', {
        'form':delf,
        'iin': iin,
        'targi': targi,
        'ltargi': ltargi,
        'num_dok': num_dok,
        'pk': pk,
        'lt': lt,
        'name_log': name_log,
        'about': about,
        'error': error
    })


@login_required(login_url='error')
def rdelegacja_add_poz(request, pk, wal):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul = "Dodawanie nowej pozycji [" + Delegacja.objects.get(pk=pk).naz_imie + "]"

    zero = Money('00.00', str(wal))

    if request.method == "POST":
        pozf = PozycjaForm(request.POST)
        if pozf.is_valid():
            post = pozf.save(commit=False)
            post.kwota_pln, post.fwaluta = CalcCurrency(post.kwota_waluta, pk)
            post.waluta = str(wal)
            post.save()
            CalcRow(pk)

            return redirect('rdelegacja_list_poz', pk=pk, wal=wal)
    else:
        pozf = PozycjaForm(initial={'delegacja': pk, 'kwota_waluta': zero})

    return render(request, 'DELEGATIONS/delegacja_radd.html', {
        'pk': pk,
        'wal': wal,
        'form':pozf,
        'tytul': tytul,
        'name_log': name_log,
        'about': about,
        'edycja': False,
        'del_id': pk,
        'del_poz_id': 0
    })


@login_required(login_url='error')
def rdelegacja_edit_poz(request, pk, po, wal):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul = "Edycja pozycji [" + Delegacja.objects.get(pk=pk).naz_imie + "]"

    pozz = get_object_or_404(Pozycja, pk=po)
    if request.method == "POST":
        pozf = PozycjaForm(request.POST, instance=pozz)
        if pozf.is_valid():
            post = pozf.save(commit=False)
            post.kwota_pln, post.fwaluta = CalcCurrency(post.kwota_waluta, pk)
            post.save()
            CalcRow(pk)

            return redirect('rdelegacja_list_poz', pk=pk, wal=wal)
    else:
        pozf = PozycjaForm(instance=pozz)


    return render(request, 'DELEGATIONS/delegacja_radd.html', {
        'pk': pk,
        'wal': wal,
        'form':pozf,
        'tytul': tytul,
        'name_log': name_log,
        'about': about,
        'edycja': True,
        'del_id': pk,
        'del_poz_id': po
    })


def rdelegacja_delete_poz(request, pk, po, wal):
    Pozycja.objects.get(pk=po).delete()
    CalcRow(pk)
    return redirect('rdelegacja_list_poz', pk=pk, wal=wal)


def rdelegacja_list_poz(request, pk, wal):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul = "Lista pozycji: " + Delegacja.objects.get(pk=pk).naz_imie + " "

    pozycje = Pozycja.objects.filter(delegacja=pk, waluta=wal)
    # pozycje = Pozycja.objects.all()

    return render(request, 'DELEGATIONS/delegacja_rlist.html', {
        'pk': pk,
        'wal': wal,
        'tytul': tytul,
        'pozycje': pozycje,
        'name_log': name_log,
        'about': about,
    })


def CorrectName():
    w = 'Małgosia Świadek'
    c = 'Małgorzata Świadek'

    de = Delegacja.objects.filter(naz_imie=w)
    print(de)

    for r in de:
        r.naz_imie = c
        r.save()

