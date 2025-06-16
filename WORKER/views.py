from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.forms import modelformset_factory
from DELEGATIONS.models import Delegacja
from LOG.logs import LogiWORK
from ORDERS.functions import test_osoba1
from ORDERS.models import NrSDE
from .calculate import rowCalc, rowCalc_c, CompareData, calc_Del_to_Pensja, calc_PremDel_to_Pensja
from .class_calc_pracownik import CalcPracownik
from .class_user_tech import UserTech
from .functions import test_osoba, test_rok, konw_mc, DoPodsumowanie, NFileToDB
from .log_work import WorkerLog
from .models import Pracownik, Pensja, Import, Podsumowanie, Premia_det, Stoisko
from .forms import PracownikForm, PensjaForm, PensjaOForm, Premia_detForm
from moneyed import Money, PLN
from SDA.settings import WORKER_KM
from .pdf import worker_mc_pdf
from django.db.models import Q
from django.db.models import Sum
from simple_search import search_filter
from django.contrib.auth.models import Group
from datetime import datetime, timedelta


usrTech = UserTech()
calcPrac = CalcPracownik()
W_LOG = WorkerLog()


"""
!
"""
@login_required(login_url='error')
def worker_start(request):
    lata, rok, brok, bmc = usrTech.test_rok(request)
    rok_nag = konw_mc(bmc)+ " " + str(rok)

    # miesiąc poprzedni
    li = int(bmc) - 1
    if li < 10:
        pmc = '0' + str(li)
    else:
        pmc = str(li)

    if int(bmc) < 2:
        prok = str(rok - 1)
        pmc = '12'
    else:
        prok = rok

    calcPrac.oblicz_wszystkim_staz_pracy()

    return render(request, 'WORKER/main_g.html', {
        'name_log': usrTech.name_log(request),
        'about': usrTech.about(),
        'ROK': rok_nag,
        'pmc': pmc,
        'prok': prok
    })

"""
!
"""
@login_required(login_url='error')
def worker_pr(request):
    query = ''
    tytul_tabeli = 'Pracownicy.'
    lata, rok, brok, bmc = usrTech.test_rok(request)
    # prac = Pracownik.objects.filter(pracuje=True).order_by('nazwisko')

    try:
        query = request.GET['SZUKAJ']
        if query != '':
            tytul_tabeli = "Szukane: " + str(query)
    except:
        pass

    if query != '':
        search_fields = [
            'imie', 'nazwisko', 'grupa', 'dzial',
            'zatrudnienie', 'wymiar', 'staz']
        se = search_filter(search_fields, query)
        prac = Pracownik.objects.filter(pracuje=True).filter(se).order_by('nazwisko')
    else:
        prac = Pracownik.objects.filter(pracuje=True).order_by('nazwisko')


    return render(request, 'WORKER/pracownik.html', {
        'name_log': usrTech.name_log(request),
        'about': usrTech.about(),
        'tytul_tabeli': tytul_tabeli,
        'pracownik': prac,
        'p_ilosc': Pracownik.ilosc_pracownikow(),
        'mc_test': Pensja.flaga_ilosc_pensja(rok, bmc),
        'bmc': bmc
    })

"""
!
"""
@login_required(login_url='error')
def worker_pr_add(request):
    tytul = 'Nowy pracownik'

    if request.method == "POST":
        worf = PracownikForm(request.POST or None)
        if worf.is_valid():
            pz = worf.save(commit=False)
            pz.staz = calcPrac.oblicz_staz_pracy(request.POST.get("staz", 0), request.POST.get("data_zat", None))
            pz.stawka_wyj = calcPrac.oblicz_stawke_wyj(request.POST.get("pensja_ust_0", 0))
            pz.save()
            return redirect('worker_pr')
        else:
            return redirect('error')
    else:
        worf = PracownikForm()
    return render(request, 'WORKER/pracownik_new.html', {
        'name_log': usrTech.name_log(request),
        'about': usrTech.about(),
        'form': worf,
        'tytul': tytul,
        'edycja': False,
        'work_id': 0
    })

"""
!
"""
@login_required(login_url='error')
def worker_pr_edit(request, pk):
    tytul = 'Edycja pracownika'

    worm = get_object_or_404(Pracownik, pk=pk)
    if request.method == "POST":
        worf = PracownikForm(request.POST or None, instance=worm)
        if worf.is_valid():
            pz = worf.save(commit=False)
            pz.staz = calcPrac.oblicz_staz_pracy(request.POST.get("staz", 0), request.POST.get("data_zat", None))
            pz.stawka_wyj = calcPrac.oblicz_stawke_wyj(request.POST.get("pensja_ust_0", 0))
            pz.save()
            return redirect('worker_pr')
        else:
            return redirect('error')
    else:
        worf = PracownikForm(instance=worm)
    return render(request, 'WORKER/pracownik_new.html', {
        'name_log': usrTech.name_log(request),
        'about': usrTech.about(),
        'form': worf,
        'tytul': tytul,
        'edycja': True,
        'work_id': pk
    })

"""
!
"""
@login_required(login_url='error')
def worker_pr_del(request, pk):
    Pracownik.objects.get(pk=pk).delete()
    return redirect('worker_pr')

"""
!
"""
@login_required(login_url='error')
def worker_pr_update(request, mc):
    lata, rok, brok, bmc = usrTech.test_rok(request)
    bmc = mc
    calcPrac.pracownik_do_pensji(rok,bmc)
    return redirect('worker_pr')

"""
!
"""
@login_required(login_url='error')
def worker_pr_update_prev(request):
    lata, rok, brok, bmc = usrTech.test_rok(request)
    mc = int(bmc) - 1
    if mc >= 1:
        mc = str(mc)
        calcPrac.pracownik_do_pensji(rok, bmc)
        # worker_pr_update(request, mc)
    else:
        calcPrac.pracownik_do_pensji(rok - 1, 12)

    return redirect('worker_pr')


#######################################################################################################################

"""
!
"""
@login_required(login_url='error')
def worker_mc(request):
    lata, rok, brok, bmc = usrTech.test_rok(request)
    name_log, inicjaly = usrTech.tst_osoba(request)
    about = usrTech.about()

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

    pen = Pensja.objects.filter(rok = brok, miesiac = bmc).order_by('pracownik__nazwisko')
    if len(pen) != 0:

        """
        !
        """
        calcPrac.calc_Del_to_Pensja(bmc, brok)

        tytul_tabeli = "Miesiąc - " + konw_mc(bmc) + "."
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

            # Przelicza wiersze tabeli
            row.razem = row.wynagrodzenie + row.suma_pd - row.obciazenie - row.ppk

    #
    # Przepisanie sumy do tabeli podsumowań
    #
    DoPodsumowanie(brok, bmc, suma_ks)


    return render(request, 'WORKER/miesiac.html', {
        'name_log': name_log,
        'about': about,
        'tytul_tabeli': tytul_tabeli,
        'brak_danych': bd,
        'mc_rok': mc_rok,
        'brok': brok,
        'rk': rok,
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
        'suma_ks': suma_ks,
        'mc_obecny': True
    })

"""
!
"""
@login_required(login_url='error')
def worker_mc_zest(request):
    lata, rok, brok, bmc = usrTech.test_rok(request)
    name_log, inicjaly = usrTech.tst_osoba(request)
    about = usrTech.about()

    osoby = Pracownik.objects.filter(pracuje=True, lp_biuro=True).order_by('nazwisko')

    tytul_tabeli = 'Brak danych'

    bd = True
    osoba_id = ''
    pen = []

    if request.method == "GET":
        osoba_id = request.GET.get("osoba")
        if osoba_id:
            pen = Pensja.objects.filter(pracownik=osoba_id).order_by("-rok", "-miesiac")
            # Przelicza wiersze tabeli
            for row in pen:
                row.razem = row.wynagrodzenie + row.suma_pd - row.obciazenie - row.ppk
                row.save()

    if len(pen) != 0:
        pr = Pracownik.objects.get(id=osoba_id)
        tytul_tabeli = "Pracownik: " + pr.imie + " " + pr.nazwisko
        bd = False


    return render(request, 'WORKER/miesiac_z.html', {
        'osoby': osoby,
        'name_log': name_log,
        'about': about,
        'tytul_tabeli': tytul_tabeli,
        'brak_danych': bd,
        'pen': pen,
    })


'''
Funkcja na podstawie tabeli pracownik raz roku i miesiąca generuje
zestaw wpisów w tabeli Pensja
'''
def gen_mc(request, bmc, brok):
    st_km = Money(WORKER_KM, PLN)
    for pr in Pracownik.objects.filter(pracuje=True, lp_biuro=True):
        pr_id = Pracownik.objects.get(id=pr.id)
        os = pr.nazwisko + " " + pr.imie
        p = Pensja(rok=brok, miesiac=bmc, osoba=os, pracownik=pr_id, wynagrodzenie=pr.pensja_ust, stawka_wyj=pr.stawka_wyj, stawka_wyj_rob=pr.stawka_wyj_rob)
        p.save()
    return redirect('worker_mc')


'''
Pobiera date zatrudnienia z tabeli Pracownik i wylicza na podstawie aktualnej daty staż pracownika.
Wynik zapisany jest w tabeli Pracownik.
'''
def gen_staz(request):
    calcPrac.oblicz_wszystkim_staz_pracy()
    return redirect('worker_pr')

"""
!
"""
@login_required(login_url='error')
def worker_mc_edit(request, mc, rk, pk):
    lata, rok, brok, bmc = usrTech.test_rok(request)
    name_log, inicjaly = usrTech.tst_osoba(request)
    about = usrTech.about()

    test = mc == bmc

    pensjam = get_object_or_404(Pensja, pk=pk)
    if request.method == "POST":
        pensjaf = PensjaForm(request.POST or None, instance=pensjam)
        if pensjaf.is_valid():
            ps = pensjaf.save(commit=False)
            ps.save()

            if test == True:
                return redirect('worker_mc')
            else:
                return redirect('worker_mc_arch', rk=rk, mc=mc)

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
        'test': test,
        'm_c': mc,
        'r_k': rk
    })


@login_required(login_url='error')
def worker_mc_oedit(request, mc, rk):
    name_log, inicjaly = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul = "Edycja obciążenia: " + konw_mc(mc) + " " + str(rk)

    queryset = Pensja.objects.filter(miesiac=mc, rok=rk).order_by('pracownik__nazwisko')
    PFormSet = modelformset_factory(Pensja, form=PensjaOForm, extra=0)

    if request.method == 'POST':
        formset = PFormSet(request.POST, queryset=queryset)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            return redirect('worker_mc_calc', mc=mc, rk=rk, ba='b')
        else:
            print(formset.errors)
    else:
        formset = PFormSet(queryset=queryset)

    return render(request, 'WORKER/miesiac_o_edit.html', {
        'name_log': name_log,
        'about': about,
        'formset': formset,
        'tytul': tytul,

    })


def worker_flag(request, pk, col, bmc, brk):
    lata, rok, brok, b_mc = test_rok(request)
    row = Pensja.objects.get(id=pk)

    if col == '1':
        row.rozliczono = not row.rozliczono
    if col == '2':
        row.l4 = not row.l4
    row.save()

    if bmc==b_mc:
        return redirect('worker_mc')
    else:
        return redirect('worker_mc_arch', mc=bmc, rk=brk)

"""
!
"""
@login_required(login_url='error')
def worker_mc_arch(request, mc, rk):
    lata, rok, brok, bmc = usrTech.test_rok(request)
    name_log, inicjaly = usrTech.tst_osoba(request)
    about = usrTech.about()

    tytul_tabeli = 'Brak danych'
    mc_rok = str(bmc) + "-" + str(rok)
    bd = True
    bmc = mc
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

    pen = Pensja.objects.filter(rok=rk, miesiac=bmc).order_by('pracownik__nazwisko') #rok
    if len(pen) != 0:

        calcPrac.calc_Del_to_Pensja(bmc, brok)

        tytul_tabeli = "Miesiąc archiwalny - " + konw_mc(bmc) + " " + str(rk)
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
        'rk': rk,
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
        'suma_ks': suma_ks,
        'mc_obecny': False
    })

'''
! Moduł wypełniany przez kierowników
'''

# def months_list():
#     current_date = datetime.now()
#     months_list = []
#
#     # Tworzymy listę ostatnich 12 miesięcy wstecz
#     for i in range(12):
#         year = current_date.year
#         month = current_date.month
#         # Dodajemy słownik z danymi miesiąca i roku
#         months_list.append({
#             'year': year,
#             'month': month,
#             'month_name': current_date.strftime('%B')  # pełna nazwa miesiąca
#         })
#         # Przechodzimy miesiąc wstecz
#         current_date = current_date - timedelta(days=current_date.day + 1)
#     return months_list


def m_list():
    current_date = datetime.now()
    months_list = []

    # Miesiące w języku polskim
    month_names = {
        1: "Styczeń", 2: "Luty", 3: "Marzec", 4: "Kwiecień",
        5: "Maj", 6: "Czerwiec", 7: "Lipiec", 8: "Sierpień",
        9: "Wrzesień", 10: "Październik", 11: "Listopad", 12: "Grudzień"
    }

    # Tworzymy listę ostatnich 12 miesięcy wstecz
    for i in range(37): # 13
        year = current_date.year
        month = f"{current_date.month:02}" # current_date.month
        # Dodajemy słownik z danymi miesiąca, roku i nazwą miesiąca po polsku
        months_list.append({
            'year': year,
            'month': month,
            'month_name': month_names[current_date.month]  # pełna nazwa miesiąca po polsku
        })
        # Przechodzimy miesiąc wstecz
        current_date = current_date - timedelta(days=current_date.day + 1)
    return months_list



@login_required(login_url='error')
def red_worker_mc(request, b_mc, b_rk, fl):
    inicjaly = usrTech.inicjaly(request)
    bmc = usrTech.biezacy_miesiac()
    zero = Money('00.00', PLN)

    """
    Przeliczanie delegacji w pensjach
    """
    calcPrac.calc_Del_to_Pensja(b_mc, b_rk)
    # print(">>>", b_mc, b_rk)

    admin = False
    blokada = False

    if inicjaly == 'M.M.':
        dzial = 'PROJEKTANT'
        tytul_tabeli = "Miesiąc - " + konw_mc(b_mc) + " " + str(b_rk) + " [ " + dzial + " ]"
        pen = Pensja.objects.filter(rok=b_rk, miesiac=b_mc, pracownik__dzial=dzial, pracownik__maska=False).order_by('pracownik__nazwisko')
    elif inicjaly == 'A.B.':
        dzial = 'TM'
        tytul_tabeli = "Miesiąc - " + konw_mc(b_mc) + " " + str(b_rk) + " [ " + dzial + " ]"
        pen = Pensja.objects.filter(rok=b_rk, miesiac=b_mc, pracownik__dzial=dzial).order_by('pracownik__nazwisko')
    elif inicjaly == 'J.K.':
        dzial = ['MARKETING', 'PM']
        tytul_tabeli = "Miesiąc - " + konw_mc(b_mc) + " " + str(b_rk) + " [ " + dzial[0] + "/" + dzial[1] + " ]"
        pen = Pensja.objects.filter(rok=b_rk, miesiac=b_mc).filter(Q(pracownik__dzial=dzial[0]) | Q(pracownik__dzial=dzial[1])).order_by('pracownik__nazwisko')
    elif inicjaly == 'A.S.':
        dzial = 'PM'
        tytul_tabeli = "Miesiąc - " + konw_mc(b_mc) + " " + str(b_rk) + " [ " + dzial + " ]"
        pen = Pensja.objects.filter(rok=b_rk, miesiac=b_mc, pracownik__dzial=dzial, pracownik__maska=False).order_by('pracownik__nazwisko')
    else:
        dzial = ''
        tytul_tabeli = "Miesiąc - " + konw_mc(b_mc) + " " + str(b_rk)
        pen = Pensja.objects.filter(rok=b_rk, miesiac=b_mc).order_by('pracownik__nazwisko')
        blokada = Pensja.objects.filter(rok=b_rk, miesiac=b_mc).values_list('blokada', flat=True).first()
        admin = True

    info = 'Okno główne - przeglądanie. Zdalny host: [' + str(request.META.get('REMOTE_ADDR')) + '], ' + tytul_tabeli
    W_LOG.start(request, info)

    brak_danych = len(pen) == 0
    f_l = fl == 't'
    sw = b_mc == bmc
    admin_mo_js = inicjaly in ('M.O.', 'J.S.', 'J.M.')

    if sw:
        admin_mo_js = False

    months_list = m_list()

    #print(">>>", months_list)


    return render(request, 'WORKER/r_miesiac.html', {
        'name_log': usrTech.name_log(request),
        'about': usrTech.about(),
        'tytul_tabeli': tytul_tabeli,
        'pen': pen,
        'brak_danych': brak_danych,
        'f_l': f_l,
        'fl': fl,
        'sw': sw,
        'b_mc': b_mc,
        'b_rk': b_rk,
        'admin': admin,
        'admin_mo_js': admin_mo_js,
        'blokada': blokada,
        'zero': zero,
        'izero': 0,
        'months_list': months_list
    })

"""
!
"""
def red_worker_mc_pdf(request, b_mc, b_rk, pk, fl):
    zero = Money('00.00', PLN)
    tst = len(Premia_det.objects.filter(pensja=pk))

    pen = Pensja.objects.get(pk=pk)
    rd = pen.del_rozli

    if rd > zero:
        ts = True
    else:
        ts = False

    if tst != 0 or ts:
        out = worker_mc_pdf(request, pk)
    else:
        out = redirect('red_worker_mc', b_mc=b_mc, b_rk=b_rk, fl=fl)
    return out

"""
!
"""
def to_money(value):
    return value if isinstance(value, Money) else Money(value or 0, 'PLN')

"""
!
"""
@login_required(login_url='error')
def red_worker_mc_detail(request, pk, fl):
    name_log, inicjaly = test_osoba(request)
    about = usrTech.about()

    pensja  = Pensja.objects.get(pk=pk)
    stawka  = pensja.stawka_wyj
    stawkar = pensja.stawka_wyj_rob
    rok     = pensja.rok
    mc = pensja.miesiac
    miesiac = konw_mc(pensja.miesiac)
    blokada = pensja.blokada

    tytul = str(pensja.pracownik.imie) + " " + str(pensja.pracownik.nazwisko)

    zero = Money('00.00', PLN)
    suma_pemia = zero
    premia = Premia_det.objects.filter(pensja=pensja.pk)

    # Agregacja sum dla różnych pól
    aggregated_sums = Premia_det.objects.filter(pensja=pensja.pk).aggregate(
        suma_wartosc=Sum('pr_wartosc'),
        suma_wyjazd=Sum('del_ilosc_razem'),
        suma_sprzedaz=Sum('kw_sprzedazy'),
        suma_premia=Sum('premia_proj'),
        suma_indywid=Sum('ind_pr_kwota')
    )

    # Przypisanie sum z agregacji lub wartości zero, jeśli wynik jest None
    suma_wartosc = to_money(aggregated_sums['suma_wartosc'])
    suma_wyjazd = to_money(aggregated_sums['suma_wyjazd'])
    suma_sprzedaz = to_money(aggregated_sums['suma_sprzedaz'])
    suma_premia = to_money(aggregated_sums['suma_premia'])
    suma_indywid = to_money(aggregated_sums['suma_indywid'])

    suma_all = suma_wartosc + suma_wyjazd + suma_pemia + suma_indywid

    flb = fl == 'p'                                                    # Jesli fl == 'p' to True else False

    if inicjaly in ['M.O.', 'J.S.', 'J.M.']:
        flb=True

    info = 'Okno personalne: ' + tytul + ', ' + str(rok) + '/' + str(mc) + ', [ ' + str(stawka) + '/' + str(stawkar) + ' ], Suma całość: ' + str(suma_all)
    W_LOG.start_det(request, info)

    return render(request, 'WORKER/red_mc_detail.html', {
        'name_log': name_log,
        'about': about,
        'form': pensja,
        'premia': premia,
        'tytul': tytul,
        'stawka': stawka,
        'stawkar': stawkar,
        'rok': rok,
        'mc': mc,
        'miesiac': miesiac,
        'pk': pk,
        'fl': fl,
        'flb': flb,
        'suma_wartosc': suma_wartosc,
        'suma_wyjazd': suma_wyjazd,
        'suma_sprzedaz': suma_sprzedaz,
        'suma_pemia': suma_pemia,
        'suma_indywid': suma_indywid,
        'suma_all': suma_all,
        'blokada': blokada
    })

"""
Funkcja do blokowania lub odblokowywania pensji pracowników za dany miesiąc i rok.

:param fn: Flag, określający czy blokować (1) czy odblokować (inne wartości).
"""
@login_required(login_url='error')
def red_worker_mc_blok(request, fl, mc, rk, fn):

    klucz = fn == '1'

    try:
        Pensja.objects.filter(miesiac=mc, rok=rk).update(blokada=klucz)
    except Exception as e:
        print("Wystąpił błąd podczas aktualizacji pensji:", e)

    return redirect('red_worker_mc', b_mc=mc, b_rk=rk, fl=fl)

"""
!
"""
@login_required(login_url='error')
def red_worker_mc_add(request,wo, fl):
    name_log, inicjaly = usrTech.tst_osoba(request)
    about = usrTech.about()
    zero = Money('00.00', PLN)

    pensja_id = Pensja.objects.get(pk=wo)

    tytul = "Nowa pozycja premii/delegacji. [ " + str(pensja_id.pracownik) + " ]"

    if request.method == "POST":
        pref = Premia_detForm(request.POST or None)

        if pref.is_valid():
            pz = pref.save(commit=False)

            pri = request.POST.get("ind_pr_kwota_0", "")
            if pri == "":
                pri = Money('00.00', PLN)
            else:
                pri = Money(str(pri), PLN)

            prw = request.POST.get("pr_wielkosc", "")
            if prw != "":
                pz.pr_wartosc = Stoisko.objects.get(pk=prw).w_premii
            else:
                pz.pr_wartosc = zero

            pz.pensja = pensja_id # Pensja.objects.get(pk=wo)
            del_ilosc_razem, premia_proj = calcPrac.calc_DelegPremia(pz, wo)
            pz.del_ilosc_razem = del_ilosc_razem
            pz.premia_proj = premia_proj
            pz.save()

            info = "NOWA POZYCJA: " + str(pensja_id.pracownik) + ", Delegacja: " + str(del_ilosc_razem) + ", Premia - projekt: " + str(premia_proj) + ", Premia indywidualna: " + str(pri)
            W_LOG.add_edit(request, info)

            return redirect('red_worker_mc_detail', pk=wo, fl=fl)
        else:
            return redirect('error')
    else:
        pref = Premia_detForm()

        flb = fl == 'p' # If 'p' that True else False

    return render(request, 'WORKER/red_mc_add.html', {
        'name_log': name_log,
        'about': about,
        'form': pref,
        'tytul': tytul,
        'pk': wo,
        'del_id': 0,
        'edycja': False,
        'fl': fl,
        'flb': flb
    })

"""
!
"""
@login_required(login_url='error')
def red_worker_mc_edit(request, wo, pk, fl):
    name_log, inicjaly = usrTech.tst_osoba(request)
    about = usrTech.about()
    zero = Money('00.00', PLN)

    pensja_id = Pensja.objects.get(pk=wo)

    tytul = "Edycja pozycji premii/delegacji. [ " + str(pensja_id.pracownik) + " ]"

    premiam = get_object_or_404(Premia_det, pk=pk)
    if request.method == "POST":
        pref = Premia_detForm(request.POST or None, instance=premiam)

        if pref.is_valid():
            pz = pref.save(commit=False)

            pri = request.POST.get("ind_pr_kwota_0", "")
            if pri == "":
                pri = Money('00.00', PLN)
            else:
                pri = Money(str(pri), PLN)

            prw = request.POST.get("pr_wielkosc", "")
            if prw != "":
                pz.pr_wartosc = Stoisko.objects.get(pk=prw).w_premii
            else:
                pz.pr_wartosc = zero

            pz.pensja = Pensja.objects.get(pk=wo)
            del_ilosc_razem, premia_proj = calcPrac.calc_DelegPremia(pz, wo)
            pz.del_ilosc_razem = del_ilosc_razem
            pz.premia_proj = premia_proj
            pz.save()

            info = "EDYCJA POZYCJI: " + str(pensja_id.pracownik) + ", Delegacja: " + str(del_ilosc_razem) + ", Premia - projekt: " + str(premia_proj) + ", Premia indywidualna: " + str(pri)
            W_LOG.add_edit(request, info)

            return redirect('red_worker_mc_detail', pk=wo, fl=fl)
        else:
            return redirect('error')
    else:
        pref = Premia_detForm(instance=premiam)


        if usrTech.tst_admin(request):
            flb = True
        else:
            flb = fl == 'p'                                                 # if 'p' that True else False

    return render(request, 'WORKER/red_mc_add.html', {
        'name_log': name_log,
        'about': about,
        'form': pref,
        'tytul': tytul,
        'pk': wo,
        'del_id': pk,
        'edycja': True,
        'fl': fl,
        'flb': flb
    })

"""
!
"""
@login_required(login_url='error')
def red_worker_mc_delete(request,wo,pk, fl):
    Premia_det.objects.get(pk=pk).delete()
    return redirect('red_worker_mc_detail', pk=wo, fl=fl)

"""
!
"""
def red_worker_mc_redirect(request,wo, fl):

    rok, m_c = calc_PremDel_to_Pensja(wo)

    if m_c < 10:
        mc = '0'+str(m_c)
    else:
        mc= str(m_c)

    return redirect('red_worker_mc', b_mc=mc, b_rk=rok, fl=fl)

"""
! Wysyłka do Googla - sprawdzić!
"""
def CalcDelPremie(rok):

    pr_del = Premia_det.objects.all()
    zero = Money('00.00', PLN)

    # Likwidacja poprzednich wartości, ustawienie zer.
    NrSDE.objects.filter(rokk=rok).update(sum_premie=zero, sum_deleg=zero)

    do_zaktualizowania = []

    for premia_det in pr_del:
        prw = premia_det.pr_wartosc + premia_det.premia_proj + premia_det.ind_pr_kwota
        de  = premia_det.del_ilosc_razem

        if hasattr(premia_det.projekt, 'id'):
            id_projektu = premia_det.projekt.id
            nsde, created = NrSDE.objects.update_or_create(
                id=id_projektu,
                defaults={'sum_premie': prw, 'sum_deleg': de, 'sum_pre_del': prw + de}
            )
            do_zaktualizowania.append(nsde)

    NrSDE.objects.bulk_update(do_zaktualizowania, ['sum_premie', 'sum_deleg', 'sum_pre_del'])


    # pr_del = Premia_det.objects.filter(pensja__rok=rok)
    # print("^^^", pr_del.count())
    # pr_del = Premia_det.objects.all()
    # print("^^^", pr_del.count())
    # zero = Money('00.00', PLN)
    #
    #
    # # Likwidacja poprzednich wartości, ustawienie zer.
    #
    # for ns in NrSDE.objects.filter(rokk=rok):
    #     ns.sum_premie = zero
    #     ns.sum_deleg  = zero
    #     ns.save()
    #
    #
    # for pd in pr_del:
    #     prw = pd.pr_wartosc + pd.premia_proj + pd.ind_pr_kwota
    #     de  = pd.del_ilosc_razem
    #     fl = 0
    #     try:
    #         idr = pd.projekt.id #Błąd oznacza że to MPK
    #         fl = 1
    #     except:
    #         pass
    #
    #     if fl == 1:
    #         nsde = NrSDE.objects.get(id=idr)
    #         nsde.sum_premie = prw
    #         nsde.sum_deleg  = de
    #         nsde.sum_pre_del = prw + de
    #         nsde.save()
    # #



"""
Tylko do użytku technicznego
"""
def upgrade_pensja(request):
    zero = Money('00.00', PLN)

    for p in Pensja.objects.all():
        os = p.pracownik.nazwisko + " " + p.pracownik.imie
        p.osoba = os
        p.save()

    rok = 2022

    for mc in range(1,4):
        suma = zero
        for r in Pensja.objects.filter(rok=rok, miesiac=mc):
            suma += r.sum_kosztow

        try:
            pod = Podsumowanie.objects.get(miesiac=mc, rok=rok)
            pod.suma_biuro = suma
            pod.save()
        except:
            po = Podsumowanie(miesiac=mc, rok=rok, suma_biuro=suma)
            po.save()

    return redirect('worker_mc')

