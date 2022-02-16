from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from LOG.logs import LogiWORK
from ORDERS.functions import test_osoba1
from .functions import test_osoba, test_rok
from .models import Pracownik, Pensja, Import
from .forms import PracownikForm, PensjaForm
from datetime import datetime, timedelta
from .functions import prac_staz, konw_mc
from moneyed import Money, PLN
from SDA.settings import WORKER_KM
import tabula



@login_required(login_url='error')
def worker_start(request):
    lata, rok, brok, bmc = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    rok_nag = konw_mc(bmc)+ " " + str(rok)

    return render(request, 'WORKER/main_g.html', {
        'name_log': name_log,
        'about': about,
        'ROK': rok_nag,
    })


@login_required(login_url='error')
def worker_pr(request):
    lata, rok, brok, bmc = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul_tabeli = 'Pracownicy'

    prac = Pracownik.objects.filter(pracuje=True).order_by('nazwisko')
    p_ilosc = prac.count()


    return render(request, 'WORKER/pracownik.html', {
        'name_log': name_log,
        'about': about,
        'tytul_tabeli': tytul_tabeli,
        'pracownik': prac,
        'p_ilosc': p_ilosc
    })


@login_required(login_url='error')
def worker_pr_add(request):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul = 'Nowy pracownik'

    if request.method == "POST":
        worf = PracownikForm(request.POST or None)
        if worf.is_valid():
            pz = worf.save(commit=False)
            pz.save()
            return redirect('worker_pr')
        else:
            return redirect('error')
    else:
        worf = PracownikForm()
    return render(request, 'WORKER/pracownik_new.html', {
        'name_log': name_log,
        'about': about,
        'form': worf,
        'tytul': tytul,
        'edycja': False,
        'work_id': 0
    })


@login_required(login_url='error')
def worker_pr_edit(request, pk):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul = 'Edycja pracownika'

    worm = get_object_or_404(Pracownik, pk=pk)
    if request.method == "POST":
        worf = PracownikForm(request.POST or None, instance=worm)
        if worf.is_valid():
            pz = worf.save(commit=False)

            dat = request.POST.get("data_zat", None)
            st  = int(request.POST.get("staz", 0))
            pz.staz = prac_staz(st, dat)

            pz.save()
            return redirect('worker_pr')
        else:
            return redirect('error')
    else:
        worf = PracownikForm(instance=worm)
    return render(request, 'WORKER/pracownik_new.html', {
        'name_log': name_log,
        'about': about,
        'form': worf,
        'tytul': tytul,
        'edycja': True,
        'work_id': pk
    })


@login_required(login_url='error')
def worker_pr_del(request, pk):
    Pracownik.objects.get(pk=pk).delete()
    return redirect('worker_pr')


@login_required(login_url='error')
def worker_mc(request):
    lata, rok, brok, bmc = test_rok(request)
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul_tabeli = 'Brak danych'
    mc_rok = str(bmc) + "-" + str(rok)
    bd = True
    zero = Money('00.00', PLN)

    suma_p = zero
    suma_pr = zero
    suma_go = zero
    suma_nd = zero
    suma_no = zero
    suma_km = zero
    suma_na = zero
    suma_dl = zero
    suma_pm = zero
    suma_ra = zero
    suma_za = zero
    suma_ko = zero
    suma_wy = zero
    suma_ks = zero

    pen = Pensja.objects.filter(rok = rok, miesiac = bmc).order_by('pracownik__nazwisko')
    if len(pen) != 0:
        tytul_tabeli = "Miesiąc - " + konw_mc(bmc)
        bd = False
        for row in pen:
            suma_p  += row.wynagrodzenie
            suma_pr += row.przelew
            suma_go += row.gotowka
            suma_nd += row.dodatek
            suma_no += row.obciazenie
            suma_km += row.km_wartosc
            suma_na += row.nadgodz
            suma_dl += row.del_ilosc_razem
            suma_pm += row.premia
            suma_ra += row.razem
            suma_za += row.zaliczka
            suma_ko += row.komornik
            suma_wy += row.wyplata
            suma_ks += row.sum_kosztow

    return render(request, 'WORKER/miesiac.html', {
        'name_log': name_log,
        'about': about,
        'tytul_tabeli': tytul_tabeli,
        'brak_danych': bd,
        'mc_rok': mc_rok,
        'brok': brok,
        'bmc': bmc,
        'pen': pen,
        'suma_p': suma_p,
        'suma_pr': suma_pr,
        'suma_go': suma_go,
        'suma_nd': suma_nd,
        'suma_no': suma_no,
        'suma_km': suma_km,
        'suma_na': suma_na,
        'suma_dl': suma_dl,
        'suma_pm': suma_pm,
        'suma_ra': suma_ra,
        'suma_za': suma_za,
        'suma_ko': suma_ko,
        'suma_wy': suma_wy,
        'suma_ks': suma_ks
    })


def gen_mc(request, bmc, brok):
    st_km = Money(WORKER_KM, PLN)

    for pr in Pracownik.objects.filter(pracuje=True):
        pr_id = Pracownik.objects.get(id=pr.id)
        p = Pensja(rok=brok, miesiac=bmc, pracownik=pr_id, wynagrodzenie=pr.pensja_ust, ppk=pr.ppk, km_dystans=pr.dystans, stawka_nadgodz=pr.stawka_nadgodz, stawka_wyj=pr.stawka_wyj, km_stawka=st_km)
        p.save()

    return redirect('worker_mc')


def gen_staz(request):

    t = datetime.today().date()

    for prac in Pracownik.objects.all():
        d_zat = prac.data_zat
        if d_zat != None:
            roz = round((t - d_zat)/timedelta(days=365))
        else:
            roz = 0
        prac.staz = roz
        prac.save()

    return redirect('worker_pr')


def rowCalc(r):

    gotowka = r.wynagrodzenie - r.przelew
    km_wartosc = (r.km_ilosc * r.km_dystans) / 8 * r.km_stawka
    nadgodz = r.nadgodz_ilosc * r.stawka_nadgodz
    del_ilosc_razem = (r.del_ilosc_100 * r.stawka_wyj) + (r.del_ilosc_50 * (r.stawka_wyj / 2))
    razem = r.wynagrodzenie + r.dodatek - r.obciazenie + km_wartosc + nadgodz + del_ilosc_razem + r.premia - r.ppk
    brutto_brutto = r.przelew * 1.68
    wyplata = razem - r.przelew - r.zaliczka - r.komornik
    sum_kosztow = brutto_brutto + wyplata + r.zaliczka

    if r.l4 == True:
        sum_kosztow = sum_kosztow - r.przelew

    r.gotowka = gotowka
    r.km_wartosc = km_wartosc
    r.nadgodz = nadgodz
    r.del_ilosc_razem = del_ilosc_razem
    r.razem = razem
    r.brutto_brutto = brutto_brutto
    r.wyplata = wyplata
    r.sum_kosztow = sum_kosztow
    # r.save()



def worker_mc_calc(request, mc, rk, ba):

    for r in Pensja.objects.filter(miesiac=mc, rok=rk):
        rowCalc(r)
        r.save()

        # gotowka         = r.wynagrodzenie - r.przelew
        # km_wartosc      = (r.km_ilosc * r.km_dystans)/8 * r.km_stawka
        # nadgodz         = r.nadgodz_ilosc * r.stawka_nadgodz
        # del_ilosc_razem = (r.del_ilosc_100 * r.stawka_wyj)+(r.del_ilosc_50 * (r.stawka_wyj/2))
        # razem           = r.wynagrodzenie + r.dodatek - r.obciazenie + km_wartosc + nadgodz + del_ilosc_razem + r.premia - r.ppk
        # brutto_brutto   = r.przelew * 1.68
        # wyplata         = razem - r.przelew - r.zaliczka - r.komornik
        # sum_kosztow     = brutto_brutto + wyplata + r.zaliczka
        #
        # if r.l4 == True:
        #     sum_kosztow = sum_kosztow - r.przelew
        #
        # r.gotowka         = gotowka
        # r.km_wartosc      = km_wartosc
        # r.nadgodz         = nadgodz
        # r.del_ilosc_razem = del_ilosc_razem
        # r.razem           = razem
        # r.brutto_brutto   = brutto_brutto
        # r.wyplata         = wyplata
        # r.sum_kosztow     = sum_kosztow
        # r.save()

    if ba=='b':
        return redirect('worker_mc')
    else:
        return redirect('worker_mc_arch')


def worker_mc_edit(request, pk):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM

    pensjam = get_object_or_404(Pensja, pk=pk)
    if request.method == "POST":
        pensjaf = PensjaForm(request.POST or None, instance=pensjam)
        if pensjaf.is_valid():
            ps = pensjaf.save(commit=False)
            rowCalc(ps)
            ps.save()
            return redirect('worker_mc')
        else:
            return redirect('error')
    else:
        pensjaf = PensjaForm(instance=pensjam)
        tytul = str(pensjam.pracownik.imie) + " " + str(pensjam.pracownik.nazwisko)


    return render(request, 'WORKER/miesiac_edit.html', {
        'name_log': name_log,
        'about': about,
        'form': pensjaf,
        'tytul': tytul,

    })


def worker_amc_edit(request, pk):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM

    pensjam = get_object_or_404(Pensja, pk=pk)
    if request.method == "POST":
        pensjaf = PensjaForm(request.POST or None, instance=pensjam)
        if pensjaf.is_valid():
            ps = pensjaf.save(commit=False)
            ps.save()
            return redirect('worker_mc_arch')
        else:
            return redirect('error')
    else:
        pensjaf = PensjaForm(instance=pensjam)
        tytul = str(pensjam.pracownik.imie) + " " + str(pensjam.pracownik.nazwisko)


    return render(request, 'WORKER/miesiac_a_edit.html', {
        'name_log': name_log,
        'about': about,
        'form': pensjaf,
        'tytul': tytul,

    })



def worker_flag(request, pk, col):

    row = Pensja.objects.get(id=pk)
    if col == '1':
        row.rozliczono = not row.rozliczono
    if col == '2':
        row.l4 = not row.l4
    row.save()

    return redirect('worker_mc')


@login_required(login_url='error')
def worker_mc_arch(request):
    lata, rok, brok, bmc = test_rok(request)

    # Wyświetl miesiąc poprzedni
    li = int(bmc) - 1
    if li < 10:
        bmc = '0' + str(li)
    else:
        bmc = str(li)

    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul_tabeli = 'Brak danych'
    mc_rok = str(bmc) + "-" + str(rok)
    bd = True
    zero = Money('00.00', PLN)

    suma_p = zero
    suma_pr = zero
    suma_go = zero
    suma_nd = zero
    suma_no = zero
    suma_km = zero
    suma_na = zero
    suma_dl = zero
    suma_pm = zero
    suma_ra = zero
    suma_za = zero
    suma_ko = zero
    suma_wy = zero
    suma_ks = zero

    pen = Pensja.objects.filter(rok = rok, miesiac = bmc).order_by('pracownik__nazwisko')
    if len(pen) != 0:
        tytul_tabeli = "Miesiąc - " + konw_mc(bmc)
        bd = False
        for row in pen:
            suma_p  += row.wynagrodzenie
            suma_pr += row.przelew
            suma_go += row.gotowka
            suma_nd += row.dodatek
            suma_no += row.obciazenie
            suma_km += row.km_wartosc
            suma_na += row.nadgodz
            suma_dl += row.del_ilosc_razem
            suma_pm += row.premia
            suma_ra += row.razem
            suma_za += row.zaliczka
            suma_ko += row.komornik
            suma_wy += row.wyplata
            suma_ks += row.sum_kosztow

    return render(request, 'WORKER/miesiac_a.html', {
        'name_log': name_log,
        'about': about,
        'tytul_tabeli': tytul_tabeli,
        'brak_danych': bd,
        'mc_rok': mc_rok,
        'brok': brok,
        'bmc': bmc,
        'pen': pen,
        'suma_p': suma_p,
        'suma_pr': suma_pr,
        'suma_go': suma_go,
        'suma_nd': suma_nd,
        'suma_no': suma_no,
        'suma_km': suma_km,
        'suma_na': suma_na,
        'suma_dl': suma_dl,
        'suma_pm': suma_pm,
        'suma_ra': suma_ra,
        'suma_za': suma_za,
        'suma_ko': suma_ko,
        'suma_wy': suma_wy,
        'suma_ks': suma_ks
    })


def worker_flag_arch(request, pk, col):

    row = Pensja.objects.get(id=pk)
    if col == '1':
        row.rozliczono = not row.rozliczono
    if col == '2':
        row.l4 = not row.l4
    row.save()

    return redirect('worker_mc_arch')


def FileToDB(file_n, file_r):

    tab_data = []
    data = ''
    err = ''

    table = tabula.read_pdf(file_n, pages=1, guess=False)
    tab = table[0].values.tolist()
    for r in tab:
        st = str(r[2])
        if st.find("Lista płac skrócona") != -1:
           data = r[2].split(" ")[-1]
    if data != '':
        tdata = data.split(".")
        mc  = tdata[1]
        rok = tdata[2]

        table = tabula.read_pdf(file_r, pages=1)
        tab = table[0].values.tolist()

        for t in tab:
            if t[0] > 0:
               d = [rok, mc, t[1].split(" ")[0], t[1].split(" ")[1], t[8]]
               tab_data.append(d)
    else:
        err = 'Problem z konwersją.'

    return err, tab_data



def file_upload_view(request):

    if request.method == 'POST':
        name_log, inicjaly, rozliczenie = test_osoba1(request)

        my_file = request.FILES.get('file')
        Import.objects.create(up_load = my_file)
        pid = Import.objects.all().values().last()['id']
        file_n = Import.objects.get(pk=pid).up_load
        file_r = Import.objects.get(pk=pid).up_load

        try:
            err1, tab_data = FileToDB(file_n, file_r)
            if err1 != '':
                LogiWORK(1, err1, inicjaly)
            count_ok, count_er, err2 = CompareData(tab_data)
            s = "Importy poprawne: " + str(count_ok) + ", Błędne: " + str(count_er) + "  " + err2
            LogiWORK(0, s, inicjaly)
        except:
            err3 = "Problem z importem pliku " + str(file_n).split("/")[1] + ". Pradopodobnie zła zawartość."
            LogiWORK(1, err3, inicjaly)



        Import.objects.all().delete()

        return HttpResponse('')


def testQuery(query):
    query = str(query)
    if query.find(",") > -1:
        try:
            q = query.replace(",", ".")
            t = q.split(" ")
            if len(t) > 1:
                q = t[0] + t[1]
            else:
                q = t[0]
            query = q
        except:
            pass
    return query



def CompareData(tab_data):

    err = ''
    count_ok = 0
    count_er = 0


    for r in tab_data:
        rs = Pensja.objects.filter(rok=r[0],miesiac=r[1],pracownik__nazwisko__icontains=r[2].split("-")[0],pracownik__imie__icontains=r[3])

        if rs.exists():
            count_ok += 1

            rs = rs.values_list('id')[0][0]  # UWAGA nie zmieniać !!!
            przelew = Money(testQuery(r[4]), PLN)
            rsw = Pensja.objects.get(pk=rs)
            rsw.przelew = przelew
            rsw.save()

        else:
            count_er += 1
            err += "(" + r[2] + " " + r[3] + ") "

    return count_ok, count_er, err



