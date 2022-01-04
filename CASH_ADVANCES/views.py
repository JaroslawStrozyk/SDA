from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group

from TaskAPI.models import Rok, URok, Waluta
from .models import Rozliczenie, Pozycja
from ORDERS.models import NrSDE, NrMPK
from .forms import PozycjaForm, RozliczenieForm
from moneyed import Money, PLN, USD, GBP, EUR, CHF
from simple_search import search_filter
import datetime
from .pdf import cash_out_pdf_roz
from django.core.paginator import Paginator
from LOG.logs import Logi, Logi_r


def test_admin(request):
    admini = False
    gr = str(Group.objects.filter(user=request.user).first())
    if gr == 'administrator':
        admini = True
    return admini


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'

    if inicjaly == 'P.Z.' or inicjaly == 'J.S.' or inicjaly == 'M.O.':
        rozliczenie = 1
    else:
        rozliczenie = 0
    return name_log, inicjaly, rozliczenie


def test_rok(request):
    tst = Rok.objects.all().order_by('rok')
    lata = []
    for t in tst:
        lata.append(t.rok)
    name_log, inicjaly, rozliczenie = test_osoba(request)
    rok = URok.objects.get(nazwa=inicjaly).rok
    brok = datetime.datetime.now().strftime("%Y")
    return lata, rok, brok


@login_required(login_url='error')
def cash_start_p(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba(request)
    about = settings.INFO_PROGRAM
    pp = settings.PAGIN_PAGE
    sv = settings.SIMPLE_VIEW

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False


    tytul = 'Zaliczki - Pozycje'

    if sv == True:
        if test_admin(request):
            pozycje = Pozycja.objects.filter(rok=rok, nr_roz__kontrola=False).order_by('-pk')
        else:
            pozycje = Pozycja.objects.filter(rok=rok, nr_roz__kontrola=False, inicjaly=inicjaly).order_by('-pk')
    else:
        if test_admin(request):
            pozycje = Pozycja.objects.filter(rok=rok).order_by('-pk')
        else:
            pozycje = Pozycja.objects.filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

    tzero = 0  # Money('00.00', PLN)

    nrsde = NrSDE.objects.filter().order_by('pk')
    nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')

    paginator = Paginator(pozycje, pp)
    strona = request.GET.get('page')
    ppozycje = paginator.get_page(strona)

    return render(request, 'CASH_ADVANCES/cash_main_p.html', {
        'pozycje': ppozycje,
        'name_log': name_log,
        'tytul_tabeli': tytul,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'tzero': tzero,
        'nrsde': nrsde,
        'nrmpk': nrmpk,
        'sv': sv,
        'szukanie': False,
        'b_rok': b_rok
    })


@login_required(login_url='error')
def cash_start_pw(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba(request)
    about = settings.INFO_PROGRAM
    pp = settings.PAGIN_PAGE

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    tytul = 'Zaliczki - Pozycje'

    if test_admin(request):
        pozycje = Pozycja.objects.filter(rok=rok, ).order_by('-pk')
    else:
        pozycje = Pozycja.objects.filter(rok=rok, inicjaly=inicjaly).order_by('-pk')

    tzero = 0  # Money('00.00', PLN)

    nrsde = NrSDE.objects.filter().order_by('pk')
    nrmpk = NrMPK.objects.filter(rok=rok).order_by('pk')

    paginator = Paginator(pozycje, pp)
    strona = request.GET.get('page')
    ppozycje = paginator.get_page(strona)

    return render(request, 'CASH_ADVANCES/cash_main_p.html', {
        'pozycje': ppozycje,
        'name_log': name_log,
        'tytul_tabeli': tytul,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'tzero': tzero,
        'nrsde': nrsde,
        'nrmpk': nrmpk,
        'sv': True,
        'szukanie': False,
        'b_rok': b_rok
    })


def CheckCorrect(ps):
    i = 0
    if ps.nr_roz.data_zal == None:
        tst1 = False  # ps.kontrola = 0
    else:
        tst1 = True  # ps.kontrola = 10
    if ps.nr_sde == None:
        tst2 = False
    else:
        tst2 = True
    if ps.nr_mpk == None:
        tst3 = False
    else:
        tst3 = True
    if ps.data_zak == None:
        tst4 = False
    else:
        tst4 = True
    if tst1 and tst4 and (tst2 or tst3):
        i = 10
    return i


def CalcCurrency(kwota, dataf):
    wartosc = Money('00.00', PLN)
    kurs = Money('00.00', PLN)
    data = ''

    if str(kwota.currency) != 'PLN' and str(dataf) != "":
        try:
            ind = Waluta.objects.filter(kod=kwota.currency,
                                        data=datetime.datetime.strptime(str(dataf), "%d.%m.%Y").strftime(
                                            "%Y-%m-%d")).values('id')[0]['id']
            poz = Waluta.objects.get(id=(ind - 1))

        except:
            ind = Waluta.objects.filter(kod=kwota.currency).order_by('-id').values('id')[0]['id']
            poz = Waluta.objects.get(id=(ind))

        wartosc = Money(str(kwota.amount * poz.kurs.amount), PLN)
        kurs = poz.kurs
        data = poz.data

    # print('kwota: '+str(kwota)+' wartość:'+str(wartosc)+' kurs:'+str(kurs))
    return data, wartosc, kurs


def ChangeFlag(pk_r, cc):
    if pk_r != '' and cc==10:
        r = Rozliczenie.objects.get(pk=pk_r)
        r.flaga_zmian = True
        r.save()


@login_required(login_url='error')
def cash_new_p(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba(request)
    about = settings.INFO_PROGRAM
    tytul = "Zaliczki - Nowa pozycja [" + name_log + "]"
    if request.method == "POST":
        pozf = PozycjaForm(request.POST or None)
        if pozf.is_valid():
            ps = pozf.save(commit=False)

            trig = request.POST.get("kwota_netto_1", "")
            dataf = request.POST.get("data_zak", "")
            ps.kwota_netto = Money(str(ps.kwota_netto.amount), trig)
            ps.kwota_brutto = Money(str(ps.kwota_brutto.amount), trig)

            tzero = Money('00.00', PLN)
            if trig != tzero.currency and str(ps.kwota_netto.currency) != 'PLN':
                data, wartosc, kurs = CalcCurrency(ps.kwota_netto, dataf)
                ps.kwota_netto_pl = wartosc
                ps.kurs_walut = kurs

            ps.kontrola = CheckCorrect(ps)

            ChangeFlag(request.POST.get("nr_roz", ""), ps.kontrola)

            ps.rok = rok
            ps.inicjaly = inicjaly

            # LOGI
            o_ik = ''
            tsde = request.POST.get("nr_sde", "")
            tmpk = request.POST.get("nr_mpk", "")
            if tsde !='':
                o_ik = "SDE: " + NrSDE.objects.get(id=tsde).nazwa
            if tmpk != '':
                o_ik = o_ik + "MPK: " + NrMPK.objects.get(id=tmpk).nazwa
            s = " Zaliczka: "+str(ps.nr_roz.data_zal) + ", " + o_ik + ", Kontrahent: " + str(ps.kontrahent)\
                + ", Kwota Netto: " + str(ps.kwota_netto) + ", Faktura: " + str(ps.nr_fv)
            Logi(0, s, inicjaly)



            ps.save()
            return redirect('cash_start_p')
        else:
            return redirect('error')
    else:
        if test_admin(request):
            pozf = PozycjaForm()
        else:
            nr_roz = Rozliczenie.objects.filter(inicjaly=inicjaly).last().id
            pozf = PozycjaForm(user=inicjaly, initial={'nr_roz': nr_roz})
    return render(request, 'CASH_ADVANCES/cash_new_p.html', {
        'form': pozf,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'edycja': False,
        'cash_id': 0
    })


@login_required(login_url='error')
def cash_edit_p(request, pk):
    name_log, inicjaly, rozliczenie = test_osoba(request)
    about = settings.INFO_PROGRAM

    tytul = "Zaliczki - Edycja pozycja [" + name_log + "]"
    pozm = get_object_or_404(Pozycja, pk=pk)
    if request.method == "POST":
        pozf = PozycjaForm(request.POST or None, instance=pozm)
        if pozf.is_valid():
            ps = pozf.save(commit=False)

            trig = request.POST.get("kwota_netto_1", "")
            dataf = request.POST.get("data_zak", "")
            ps.kwota_netto = Money(str(ps.kwota_netto.amount), trig)
            ps.kwota_brutto = Money(str(ps.kwota_brutto.amount), trig)

            tzero = Money('00.00', PLN)
            if trig != tzero.currency and str(ps.kwota_netto.currency) != 'PLN':
                data, wartosc, kurs = CalcCurrency(ps.kwota_netto, dataf)
                ps.kwota_netto_pl = wartosc
                ps.kurs_walut = kurs

            ps.kontrola = CheckCorrect(ps)

            ChangeFlag(request.POST.get("nr_roz", ""), ps.kontrola)

            # LOGI
            o_ik = ''
            tsde = request.POST.get("nr_sde", "")
            tmpk = request.POST.get("nr_mpk", "")
            if tsde !='':
                o_ik = "SDE: " + NrSDE.objects.get(id=tsde).nazwa
            if tmpk != '':
                o_ik = o_ik + "MPK: " + NrMPK.objects.get(id=tmpk).nazwa
            s = " Zaliczka: "+str(ps.nr_roz.data_zal) + ", " + o_ik + ", Kontrahent: " + str(ps.kontrahent)\
                + ", Kwota Netto: " + str(ps.kwota_netto) + ", Faktura: " + str(ps.nr_fv)
            Logi(1, s, inicjaly)


            ps.save()
            return redirect('cash_start_p')
        else:
            return redirect('error')
    else:
        pozf = PozycjaForm(instance=pozm)
    return render(request, 'CASH_ADVANCES/cash_new_p.html', {
        'form': pozf,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'edycja': True,
        'cash_id': pk
    })


def suma_wartosci(pozycje):
    DICT = {}
    tab = settings.CURRENCIES
    for t in tab:
        DICT[t] = Money('00.00', t)

    for poz in pozycje:
        if poz.data_zak != '':
            c = poz.kwota_netto.currency
            d = poz.kwota_netto.amount
            DICT[str(c)] = Money(d, c) + DICT[str(c)]

    suma = ''
    for i in DICT.items():
        tst = Money('00.00', i[1].currency)
        if i[1] != tst:
            suma += str(i[1].currency) + ': ' + str(i[1].amount) + ' / '
    suma = suma[:-3]
    DICT.clear()
    return suma


@login_required(login_url='error')
def cash_search_p(request):
    if request.method == "GET":
        lata, rok, brok = test_rok(request)
        name_log, inicjaly, rozliczenie = test_osoba(request)
        query = request.GET['SZUKAJ']
        if query == '' or query == ' ':
            return redirect('cash_start_p')
        else:
            search_fields = [
                'kontrahent', 'nr_fv', 'kwota_netto', 'kwota_brutto', 'data_zak', 'data_zam', 'opis', 'inicjaly',
                'nr_mpk__nazwa', 'nr_sde__nazwa', 'nr_roz__data_zal'
            ]
            f = search_filter(search_fields, query)
            if test_admin(request):
                pozycje = Pozycja.objects.filter(f).filter(rok=rok)
            else:
                pozycje = Pozycja.objects.filter(f).filter(rok=rok, inicjaly=inicjaly)

        if int(rok) == int(brok):
            b_rok = True
        else:
            b_rok = False

        tytul = 'Lista pozycji, Szukasz: ' + query
        about = settings.INFO_PROGRAM

        tzero = 0  # Money('00.00', PLN)

        nrsde = NrSDE.objects.filter(rok=rok)
        nrmpk = NrMPK.objects.filter(rok=rok)

        suma = suma_wartosci(pozycje)

        return render(request, 'CASH_ADVANCES/cash_main_p.html', {
            'pozycje': pozycje,
            'name_log': name_log,
            'tytul_tabeli': tytul,
            'admini': test_admin(request),
            'about': about,
            'lata': lata,
            'rok': rok,
            'tzero': tzero,
            'nrsde': nrsde,
            'nrmpk': nrmpk,
            'suma': suma,
            'szukanie': True,
            'b_rok': b_rok
        })
    else:
        return redirect('cash_start_p')


@login_required(login_url='error')
def cash_delete_p(request, pk):
    name_log, inicjaly, rozliczenie = test_osoba(request)

    # Logi
    o_ik = ''
    ps = Pozycja.objects.get(id=pk)
    tsde = ps.nr_sde_id
    tmpk = ps.nr_mpk_id
    if tsde != None:
        o_ik = "SDE: " + NrSDE.objects.get(id=tsde).nazwa
    if tmpk != None:
        o_ik = o_ik + "MPK: " + NrMPK.objects.get(id=tmpk).nazwa
    s = " Zaliczka: " + str(ps.nr_roz.data_zal) + ", " + o_ik + ", Kontrahent: " + str(ps.kontrahent) \
        + ", Kwota Netto: " + str(ps.kwota_netto) + ", Faktura: " + str(ps.nr_fv)
    Logi(2, s, inicjaly)


    Pozycja.objects.get(pk=pk).delete()

    return redirect('cash_start_p')


'''
Sekcja rozliczenia
'''


def CheckCurrency(kwota):  # z wartości zaliczki pobieram symbol waluty
    w = str(kwota)
    ps = Money('00.00', PLN)
    if w.find('Fr.') > -1:
        ps = Money('00.00', CHF)
    elif w.find('€') > -1:
        ps = Money('00.00', EUR)
    elif w.find('GB£') > -1:
        ps = Money('00.00', GBP)
    elif w.find('US$') > -1:
        ps = Money('00.00', USD)
    return ps


def CalcCurrents(rok):
    roz = Rozliczenie.objects.filter(rok=rok, flaga_zmian=True)

    for rz in roz:
        poz = Pozycja.objects.filter(nr_roz=rz.pk, data_zak__isnull=False)
        wydatki = 0
        for pz in poz:
            if isinstance(wydatki, int):
                wydatki = CheckCurrency(rz.zal_kwota)
            wydatki = wydatki + pz.kwota_brutto
        rz.zal_suma = wydatki
        rz.saldo = rz.zal_kwota - wydatki
        rz.save()


def PozycjeUpdate(pk, zal_kwota, przek):
    zal_suma = CheckCurrency(zal_kwota)
    poz = Pozycja.objects.filter(nr_roz=pk, data_zak__isnull=False)

    for pz in poz:
        if pz.kontrola==10 and przek==True:
            pz.kontrola = 11
        if pz.kontrola==11 and przek==False:
            pz.kontrola = 10
        zal_suma = zal_suma + pz.kwota_brutto
        pz.save()

    saldo = zal_kwota - zal_suma
    return zal_suma, saldo


@login_required(login_url='error')
def cash_start_r(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba(request)
    about = settings.INFO_PROGRAM
    pp = settings.PAGIN_PAGE
    sv = settings.SIMPLE_VIEW

    CalcCurrents(rok)

    if int(rok) == int(brok):
        b_rok = True
    else:
        b_rok = False

    tytul = 'Zaliczki - Rozliczenia'

    if sv == True:
        if test_admin(request):
            rozliczenia = Rozliczenie.objects.filter(rok=rok, kontrola=False).order_by('-id')
        else:
            rozliczenia = Rozliczenie.objects.filter(rok=rok, kontrola=False, inicjaly=inicjaly).order_by('-id')
    else:
        if test_admin(request):
            rozliczenia = Rozliczenie.objects.filter(rok=rok).order_by('-id')
        else:
            rozliczenia = Rozliczenie.objects.filter(rok=rok, inicjaly=inicjaly).order_by('-id')

    tzero = 0  # Money('00.00', PLN)

    nrsde = NrSDE.objects.filter().order_by('nazwa')
    nrmpk = NrMPK.objects.filter(rok=rok).order_by('nazwa')

    wpisy = Pozycja.objects.filter(rok=rok).order_by('data_zak')

    return render(request, 'CASH_ADVANCES/cash_main_r.html', {
        'rozliczenia': rozliczenia,
        'name_log': name_log,
        'tytul_tabeli': tytul,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'tzero': tzero,
        'nrsde': nrsde,
        'nrmpk': nrmpk,
        'wpisy': wpisy,
        'sv': sv,
        'b_rok': b_rok

    })


@login_required(login_url='error')
def cash_start_rw(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba(request)
    about = settings.INFO_PROGRAM

    CalcCurrents(rok)

    tytul = 'Zaliczki - Rozliczenia'

    if test_admin(request):
        rozliczenia = Rozliczenie.objects.filter(rok=rok).order_by('-id')
    else:
        rozliczenia = Rozliczenie.objects.filter(rok=rok, inicjaly=inicjaly).order_by('-id')

    tzero = 0  # Money('00.00', PLN)

    nrsde = NrSDE.objects.filter().order_by('nazwa')
    nrmpk = NrMPK.objects.filter(rok=rok).order_by('nazwa')

    wpisy = Pozycja.objects.filter(rok=rok).order_by('data_zak')

    return render(request, 'CASH_ADVANCES/cash_main_r.html', {
        'rozliczenia': rozliczenia,
        'name_log': name_log,
        'tytul_tabeli': tytul,
        'admini': test_admin(request),
        'about': about,
        'lata': lata,
        'rok': rok,
        'tzero': tzero,
        'nrsde': nrsde,
        'nrmpk': nrmpk,
        'wpisy': wpisy,
        'sv': True
    })


@login_required(login_url='error')
def cash_new_r(request):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba(request)
    about = settings.INFO_PROGRAM

    tytul = "Nowe rozliczenie"
    if request.method == "POST":
        rozf = RozliczenieForm(request.POST or None)
        if rozf.is_valid():
            ps = rozf.save(commit=False)
            ps.rok = datetime.date.today().year

            ps.zal_suma = CheckCurrency(ps.zal_kwota)
            ps.saldo = CheckCurrency(ps.zal_kwota)

            if ps.roz == True:
                ps.kontrola = 10
            else:
                ps.kontrola = 0

            ps.rok = rok
            ps.inicjaly = inicjaly

            # LOGI
            s = " Rozliczenie: "+str(ps.data_zal) + ", Kto: " + str(ps.nazwisko) + ", KW: "+ str(ps.kw) + ", Kwota: "\
                + str(ps.zal_kwota)
            Logi_r(0, s, inicjaly)

            ps.save()
            return redirect('cash_start_r')
        else:
            return redirect('error')
    else:
        rozf = RozliczenieForm()
    return render(request, 'CASH_ADVANCES/cash_new_r.html', {
        'form': rozf,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'potwierdzenie': rozliczenie,
        'edycja': False,
        'cash_id': 0
    })


@login_required(login_url='error')
def cash_edit_r(request, pk):
    lata, rok, brok = test_rok(request)
    name_log, inicjaly, rozliczenie = test_osoba(request)
    about = settings.INFO_PROGRAM

    tytul = "Edycja rozliczenia"

    rozm = get_object_or_404(Rozliczenie, pk=pk)
    if request.method == "POST":
        rozf = RozliczenieForm(request.POST or None, request.FILES or None, instance=rozm)
        if rozf.is_valid():
            ps = rozf.save(commit=False)
            ps.rok = datetime.date.today().year

            ps.zal_suma, ps.saldo = PozycjeUpdate(pk, ps.zal_kwota, ps.przek)

            if ps.roz == True:
                ps.kontrola = 10
            else:
                ps.kontrola = 0

            # ps.rok = rok

            # LOGI
            if ps.roz == True:
                troz = 'Tak'
            else:
                troz = 'Nie'
            if ps.przek == True:
                tprzek = 'Tak'
            else:
                tprzek = 'Nie'
            s = " Rozliczenie: "+str(ps.data_zal) + ", Kto: " + str(ps.nazwisko) + ", KW: "+ str(ps.kw) + ", Kwota: "\
                + str(ps.zal_kwota) + ", Wydatki: " + str(ps.zal_suma) + ", Saldo: " + str(ps.saldo) \
                + ", Przek. do rozliczenia: " + tprzek + ", Rozliczono: " + troz
            Logi_r(1, s, inicjaly)

            ps.save()
            return redirect('cash_start_r')
        else:
            return redirect('error')
    else:
        rozf = RozliczenieForm(instance=rozm)
    return render(request, 'CASH_ADVANCES/cash_new_r.html', {
        'form': rozf,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'potwierdzenie': rozliczenie,
        'edycja': True,
        'cash_id': pk
    })


@login_required(login_url='error')
def cash_search_r(request):
    if request.method == "GET":
        lata, rok, brok = test_rok(request)
        name_log, inicjaly, rozliczenie = test_osoba(request)
        query = request.GET['SZUKAJ']
        if query == '' or query == ' ':
            return redirect('cash_start_r')
        else:
            search_fields = [
                'data_roz', 'kw', 'nazwisko', 'zal_kwota', 'zal_suma', 'saldo',
                'uwagi', 'inicjaly'
            ]
            f = search_filter(search_fields, query)
            rozliczenia = Rozliczenie.objects.filter(f).filter(rok=rok)

        if int(rok) == int(brok):
            b_rok = True
        else:
            b_rok = False

        tytul = 'Lista rozliczeń, Szukasz: ' + query
        about = settings.INFO_PROGRAM

        tzero = Money('00.00', PLN)

        nrsde = NrSDE.objects.filter(rok=rok)
        nrmpk = NrMPK.objects.filter(rok=rok)

        return render(request, 'CASH_ADVANCES/cash_main_r.html', {
            'rozliczenia': rozliczenia,
            'name_log': name_log,
            'tytul_tabeli': tytul,
            'admini': test_admin(request),
            'about': about,
            'lata': lata,
            'rok': rok,
            # 'tdate': tdate,
            'tzero': tzero,
            'nrsde': nrsde,
            'nrmpk': nrmpk,
            'b_rok': b_rok
        })
    else:
        return redirect('cash_start_r')


@login_required(login_url='error')
def cash_delete_r(request, pk):
    name_log, inicjaly, rozliczenie = test_osoba(request)

    # LOGI
    ps = Rozliczenie.objects.get(pk=pk)
    if ps.roz == True:
        troz = 'Tak'
    else:
        troz = 'Nie'
    if ps.przek == True:
        tprzek = 'Tak'
    else:
        tprzek = 'Nie'
    s = " Rozliczenie: " + str(ps.data_zal) + ", Kto: " + str(ps.nazwisko) + ", KW: " + str(ps.kw) + ", Kwota: " \
        + str(ps.zal_kwota) + ", Wydatki: " + str(ps.zal_suma) + ", Saldo: " + str(ps.saldo) \
        + ", Przek. do rozliczenia: " + tprzek + ", Rozliczono: " + troz
    Logi_r(2, s, inicjaly)

    Rozliczenie.objects.get(pk=pk).delete()
    return redirect('cash_start_r')


@login_required(login_url='error')
def cash_pdf_roz(request, pk):
    return cash_out_pdf_roz(request, pk)


def cash_rok_akt1(request, pk):
    name_log, inicjaly, rozliczenie = test_osoba(request)
    ur = URok.objects.all()
    for u in ur:
        if u.nazwa == inicjaly:
            u.rok = pk
            u.save()
    return redirect('cash_start_p')


def cash_rok_akt2(request, pk):
    name_log, inicjaly, rozliczenie = test_osoba(request)
    ur = URok.objects.all()
    for u in ur:
        if u.nazwa == inicjaly:
            u.rok = pk
            u.save()
    return redirect('cash_start_r')
