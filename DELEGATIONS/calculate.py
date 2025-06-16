from moneyed import Money, PLN
from .models import Delegacja, Dieta, Pozycja
from TaskAPI.models import Waluta, Rok, URok
import datetime
import requests
from currency_converter import CurrencyConverter




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
    brok = datetime.datetime.now().strftime("%Y")
    return lata, rok, brok


#
# Funkcja dla oblicznia następnej delegacji (przy ADD)
#
def extractNumber():
    rok = int(datetime.datetime.now().strftime("%Y"))
    num = ''
    if rok > 2023:
        num = Delegacja.objects.all().last().numer
        try:
            num = num.split('.')
            m_c = int(num[0])
            r_k = num[1]       # Ta linia jest tylko dla sprawdzenia formatu numeru
            m_c += 1
            num = str(m_c) + '.' + str(rok)
        except:
            num = '1.' + str(rok)
    return num


def szukajDietyNoclegi(s):
    stawka =  Money('00.00', 'PLN')
    nocleg = Money('00.00', 'PLN')

    # print("SZUKANA ZMIENNA :", s)

    for D in Dieta.objects.all():
        if D.panstwo == s:
            stawka = D.dieta
            nocleg = D.nocleg
            # print(">>>", D.dieta, D.nocleg, D.panstwo,type(D.panstwo))
    return stawka, nocleg


def delgacja_mv_data():
    dele = Delegacja.objects.all()

    for d in dele:
        d.dc_rozpo = d.data_od
        d.dc_zakon = d.data_do
        d.przekr_gran = d.data_od
        d.powrot_kraj = d.data_do
        d.save()


def convertDataPL(R):
    out = R.dc_zakon - R.dc_rozpo
    dni = out.days
    godz, remainder = divmod(out.seconds, 3600)
    minuty, seconds = divmod(remainder, 60)
    return dni, godz, minuty


def convertDataSW(R):
    out = R.powrot_kraj - R.przekr_gran
    dni = out.days
    godz, remainder = divmod(out.seconds, 3600)
    minuty, seconds = divmod(remainder, 60)
    return dni, godz, minuty


def convertDataPLSW(R):
    out1 = R.przekr_gran - R.dc_rozpo
    out2 = R.dc_zakon - R.powrot_kraj
    #out = out1 + out2
    dni1 = out1.days
    godz1, remainder = divmod(out1.seconds, 3600)
    minuty1, seconds1 = divmod(remainder, 60)

    dni2 = out2.days
    godz2, remainder = divmod(out2.seconds, 3600)
    minuty2, seconds2 = divmod(remainder, 60)

    return dni1, godz1, minuty1, dni2, godz2, minuty2


def calc_DietaPosilkiKraj(dni, godz, stawka, sniadanie, obiad, kolacja):
    # Dieta krajowa:  <8h - wal się; 8<>12 - 50%; >12h - 100%
    # Dieta
    out = Money('00.00', 'PLN')
    if dni > 0:
        out = dni * stawka

    if godz >= 8 and godz <= 12:
        out = out + stawka / 2

    if godz > 12:
        out = out + stawka

    # Posiłki
    out = out - sniadanie * (stawka * 0.25)
    out = out - obiad * (stawka * 0.5)
    out = out - kolacja * (stawka * 0.25)

    #
    # DIETY DO PEŁNYCH DNI
    #
    # print("><><", dni, godz )

    out1 = Money('00.00', 'PLN')
    if dni > 0:
        out1 = out1 + dni * stawka

    if godz > 0:
        out1 += stawka

    r = out1 - out

    return out, out1, r


def calc_DietaPosilkiKraj1(dni, dni1, godz, godz1, stawka, sniadanie, obiad, kolacja):
    # Dieta krajowa:  <8h - wal się; 8<>12 - 50%; >12h - 100%

    # Dieta na wyjazd
    out = Money('00.00', 'PLN')
    if dni > 0:
        out = dni * stawka

    if godz >= 8 and godz <= 12:
        out = out + stawka / 2

    if godz > 12:
        out = out + stawka

    # Dieta na powrót
    out1 = Money('00.00', 'PLN')
    if dni1 > 0:
        out1 = dni1 * stawka

    if godz1 >= 8 and godz1 <= 12:
        out1 = out1 + stawka / 2

    if godz1 > 12:
        out1 = out1 + stawka

    out = out + out1

    # Posiłki
    out = out - sniadanie * (stawka * 0.25)
    out = out - obiad * (stawka * 0.5)
    out = out - kolacja * (stawka * 0.25)

    return out


def calc_DietaPosilkiSwiat(dni, godz, stawka, sniadanie, obiad, kolacja):
    # Dieta świat:  <8h - 33%; 8<>12 - 50%; >12h - 100%
    # Diety
    sout = Money('00.00', str(stawka.currency))
    if dni > 0:
        sout = sout + dni * stawka

    # Posiłki
    # sniadanie = 4.31
    if sniadanie > dni:
        test1 = True
    else:
        test1 = False

    if obiad > dni:
        test2 = True
    else:
        test2 = False

    if kolacja > dni:
        test3 = True
    else:
        test3 = False

    if test1:
        sout = sout - ((sniadanie - 1) * (stawka * 0.15))
    else:
        sout = sout - ((sniadanie) * (stawka * 0.15))

    if test2:
        sout = sout - ((obiad - 1) * (stawka * 0.3))
    else:
        sout = sout - obiad * (stawka * 0.3)

    if test3:
        sout = sout - ((kolacja - 1) * (stawka * 0.3))
    else:
        sout = sout - kolacja * (stawka * 0.3)


    # Godziny
    if  godz > 0 and godz < 8:
        if test1:
            sout = sout + ((stawka * 0.33) - ((stawka * 0.33) * 0.15))
        else:
            sout = sout + (stawka * 0.33)


    if godz >= 8 and godz <= 12:

        if (not test1) and (not test2) and (not test3):
            sout = sout + (stawka / 2)

        if test1:
            sout = sout + ((stawka / 2)) - ((stawka / 2) * 0.15)

        if test2:
            sout = sout + ((stawka / 2)) - ((stawka / 2) * 0.3)

        if test3:
            sout = sout + ((stawka / 2)) - ((stawka / 2) * 0.3)


    if godz > 12:

        if (not test1) and (not test2) and (not test3):
            sout = sout + stawka

        if test1:
            sout = sout + (stawka - (stawka * 0.15))

        if test2:
            sout = sout + (stawka - (stawka * 0.3))

        if test3:
            sout = sout + (stawka - (stawka * 0.3))

    #
    # DIETY DO PEŁNYCH DNI
    #
    # print("><><", dni, godz )

    sout1 = Money('00.00', str(stawka.currency))
    if dni > 0:
        sout1 = sout1 + dni * stawka

    if godz > 0:
        sout1 += stawka

    r = sout1 - sout

    return sout, sout1, r


def calc_NoclegKraj(ilosc, nocleg):
    out = ilosc * nocleg
    return out


def calc_NoclegSwiat(ilosc, nocleg):
    out = ilosc * nocleg
    return out


def calc_AutoPrvKraj(poj_siln, ilosc_km):
    out = Money('00.00', 'PLN')
    st1 = Money('00.8358', 'PLN')
    st2 = Money('00.5214', 'PLN')
    if poj_siln:
        out = ilosc_km * st1
    else:
        out = ilosc_km * st2
    return out


def AddCurr(pk, war):
    #D = Delegacja.objects.get(pk=pk)
    wal  = war.amount
    curr = war.currency
    c = CurrencyConverter()
    out = c.convert(wal, str(curr), 'PLN')

    print("TEST: ", war.currency, 'PLN', out)




def rozliczDelegacje(pk):
    # Pobieranie instancje delegacji
    R = Delegacja.objects.get(pk=pk)
    data_z = R.data_pobr_zal
    data_r = R.data_rozl
    #
    # print("Data zgłoszenia  :", data_z)
    # print("Data rozliczenia :", data_r)
    # print("Lokalizacja      :", R.lok_targi)

    # Pobieranie wartości diet i noclegów według Panstwa
    stawka_kraj, nocleg_kraj = szukajDietyNoclegi('Polska')
    stawka, nocleg = szukajDietyNoclegi(R.lok_targi)

    # print("Stawka, Noclegi  :", stawka, nocleg)


    suma_pl = Money('00.00', 'PLN')
    suma_wal = Money('00.00', str(stawka.currency))

    # Konwersja czasu z dat i celu podróży
    if R.lok_targi == 'Polska':
        PL = True
        dni, godz, minuty = convertDataPL(R)
        sdni, sgodz, sminuty = [0, 0, 0]
    else:
        PL = False
        dni, godz, minuty, dni1, godz1, minuty1 = convertDataPLSW(R)
        sdni, sgodz, sminuty = convertDataSW(R)

    # Opis
    if PL:
        out = "Długość delegacji - dni[" + str(dni) + "], godz.["+str(godz)+"]"
    else:
        out = "Długość delegacji => Kraj - dni[ " + str(dni) + " - " + str(dni) + " ], godz.[ "+str(godz)+" - "+str(godz1)+" ]; Poza granicami - dni[ " + str(sdni) + " ], godz.[ "+str(sgodz)+" ]"
    R.czas_opis = out

    if PL:
        # Dieta i Psilki
        out, out1, r = calc_DietaPosilkiKraj(dni, godz, stawka_kraj, R.sniadanie, R.obiad, R.kolacja)
        #
        R.czysta_dieta = out1
        R.roznica_diet = r
        R.roznica_diet_pl = r
        #
        R.dieta_kr = out
        suma_pl = suma_pl + out
        R.dieta_razem = out
        out = calc_NoclegKraj(R.nocleg_ilosc_kr, nocleg_kraj)
        R.nocleg_kr = out
        suma_pl = suma_pl + out
        R.prv_paliwo_kr = calc_AutoPrvKraj(R.silnik_poj, R.km_ilosc)
        suma_pl = suma_pl + out
        suma_pl += R.koszt_paliwo_kr

        sum_wal, sum_pl = CalcWydatki(pk, stawka)

        R.wydatki_sum = sum_pl
        R.wydatki_sum_pl = sum_pl

        zal_pln = Money(str(R.kasa_pln), 'PLN')
        R.pobr_zal_pln = zal_pln

        suma_pl = suma_pl + sum_pl
        R.lacznie_koszty_pln = suma_pl
        R.suma_koniec_pl = zal_pln - suma_pl

    else:
        # Kraj
        out             = calc_DietaPosilkiKraj1(dni, dni1, godz, godz1, stawka_kraj, 0, 0, 0)
        R.dieta_kr      = out
        suma_pl = suma_pl + out
        out     = calc_NoclegKraj(R.nocleg_ilosc_kr, nocleg_kraj)
        R.nocleg_kr = out
        suma_pl = suma_pl + out
        out = calc_AutoPrvKraj(R.silnik_poj, R.km_ilosc)
        R.prv_paliwo_kr = out
        suma_pl = suma_pl + out

        # Świat
        sout, sout1, r = calc_DietaPosilkiSwiat(sdni, sgodz, stawka, R.sniadanie, R.obiad, R.kolacja)

        R.czysta_dieta = sout1
        R.roznica_diet = r
        wartosc, kurs, kurs_data = CalcCurrencyDS(r, data_r)
        R.roznica_diet_pl = wartosc

        R.dieta_za = sout
        suma_wal = suma_wal + sout
        wartosc, kurs, kurs_data = CalcCurrencyDS(sout, data_r)

        if (sout.amount>0) and (wartosc.amount==0):
            ex = str(sout.currency)
            wal, efd = GetRate(ex)                                         # Pobieranie kursu walut online !
            wartosc = sout.amount * wal                                    # wyliczenie na złotówki
            wartosc_kon = Money(str(wartosc.amount/R.kurs2.amount), 'EUR') # konwersja na EUR
            R.dieta_za_euro = wartosc_kon
            R.dieta_za_not  = wal
            R.dieta_za_efd  = efd
        else:
            R.dieta_za_euro = Money('0.00', 'EUR')
            R.dieta_za_not  = Money('0.00', 'PLN')
            R.dieta_za_efd  = ''


        R.dieta_za_zl = wartosc
        suma_pl = suma_pl + out + wartosc
        R.dieta_razem = wartosc + out
        sout = calc_NoclegSwiat(R.nocleg_ilosc_za, nocleg)
        R.nocleg_za = sout
        suma_wal = suma_wal + sout
        wartosc, kurs, kurs_data = CalcCurrencyDS(sout, data_r)
        R.nocleg_za_zl = wartosc
        suma_pl = suma_pl + wartosc

        cw = CorrectAuto(R.koszt_paliwo_za, stawka)
        R.koszt_paliwo_za = cw
        suma_wal = suma_wal + cw
        wartosc, kurs, kurs_data = CalcCurrencyDS(cw, data_r)
        R.koszt_paliwo_za_pl = wartosc
        suma_pl = suma_pl + wartosc

        zal_wal = SelectCurrent(R.kasa_euro, R.kasa_funt, R.kasa_dolar, stawka)
        R.pobr_zal_wal = zal_wal
        zal_pln, kursz, kurs_dataz = CalcCurrencyDS(zal_wal, data_z)
        R.pobr_zal_pln = zal_pln

        R.kursz = kursz
        R.kurs_dataz = kurs_dataz

        R.kurs = kurs
        R.kurs_data = kurs_data

        sum_wal, sum_pl = CalcWydatki(pk, stawka)

        R.wydatki_sum = sum_wal
        R.wydatki_sum_pl = sum_pl

        suma_wal = suma_wal + sum_wal
        suma_pl = suma_pl + sum_pl

        R.lacznie_koszty_wal = suma_wal
        R.lacznie_koszty_pln = suma_pl # !?

        v = CorrectValue(zal_wal, suma_wal)

        R.suma_koniec    = v # zal_wal - suma_wal
        R.suma_koniec_pl = zal_pln - suma_pl
    R.save()

    # Dopisanie diety do właściwego pola
    R = Delegacja.objects.get(pk=pk)
    war = R.dieta_za
    curr = war.currency
    R.dieta_za_2 = Money('0.00', 'EUR')
    R.dieta_za_3 = Money('0.00', 'GBP')
    R.dieta_za_4 = Money('0.00', 'USD')
    R.dieta_za_5 = Money('0.00','CHF')
    if str(curr)=='EUR':
        R.dieta_za_2 = war
    elif str(curr)=='GBP':
        R.dieta_za_3 = war
    elif str(curr)=='USD':
        R.dieta_za_4 = war
    elif str(curr)=='CHF':
        R.dieta_za_5 = war
    elif str(curr) == 'DKK':
        AddCurr(pk, war)
    elif str(curr) == 'JPY':
        AddCurr(pk, war)
    else:
        R.dieta_za_2 = R.dieta_za_euro
    R.save()

    # Liczenie Zestawienia
    R = Delegacja.objects.get(pk=pk)

    kw1 = Money(str(R.kasa_pln),'PLN')
    kw2 = Money(str(R.kasa_euro),'EUR')
    kw3 = Money(str(R.kasa_funt),'GBP')
    kw4 = Money(str(R.kasa_dolar),'USD')
    kw5 = Money(str(R.kasa_inna),'CHF')
    #kw5 = Money('0.00','CHF')
    wd1 = R.dieta_kr + R.sum_wydatki1
    wd2 = R.dieta_za_2 + R.sum_wydatki2
    wd3 = R.dieta_za_3 + R.sum_wydatki3
    wd4 = R.dieta_za_4 + R.sum_wydatki4
    wd5 = R.dieta_za_5 + R.sum_wydatki5
    R.podsumowanie1 = kw1 - wd1
    R.podsumowanie2 = kw2 - wd2
    R.podsumowanie3 = kw3 - wd3
    R.podsumowanie4 = kw4 - wd4
    R.podsumowanie5 = kw5 - wd5

    R.zaliczka1 = kw1
    R.wd1 = wd1
    R.suma1 = kw1 - wd1

    wartosc1, kurs, kurs_data = CalcCurrencyDS(kw2, data_z)
    R.kursz2 = kurs
    R.zaliczka2 = wartosc1
    wartosc2, kurs, kurs_data = CalcCurrencyDS(wd2, data_r)
    R.kurs2 = kurs
    R.wd2 = wartosc2
    R.suma2 = wartosc1 - wartosc2

    wartosc1, kurs, kurs_data = CalcCurrencyDS(kw3, data_z)
    R.kursz3 = kurs
    R.zaliczka3 = wartosc1
    wartosc2, kurs, kurs_data = CalcCurrencyDS(wd3, data_r)
    R.kurs3 = kurs
    R.wd3 = wartosc2
    R.suma3 = wartosc1 - wartosc2

    wartosc1, kurs, kurs_data = CalcCurrencyDS(kw4, data_z)
    R.kursz4 = kurs
    R.zaliczka4 = wartosc1
    wartosc2, kurs, kurs_data = CalcCurrencyDS(wd4, data_r)
    R.kurs4 = kurs
    R.wd4 = wartosc2
    R.suma4 = wartosc1 - wartosc2

    wartosc1, kurs, kurs_data = CalcCurrencyDS(kw5, data_z)
    R.kursz5 = kurs
    R.zaliczka5 = wartosc1
    wartosc2, kurs, kurs_data = CalcCurrencyDS(wd5, data_r)
    R.kurs5 = kurs
    R.wd5 = wartosc2
    R.suma5 = wartosc1 - wartosc2

    R.save()

    # Ostateczna suma
    R = Delegacja.objects.get(pk=pk)
    R.suma0 = R.suma1 + R.suma2 + R.suma3 + R.suma4 + R.suma5
    R.save()

    #SDE
    R = Delegacja.objects.get(pk=pk)
    kst1 = R.kod_sde_targi1
    kst2 = R.kod_sde_targi2
    swd = R.wd1 + R.wd2 + R.wd3 + R.wd4 + R.wd5
    zero = Money('0.00','PLN')

    f = 0
    if kst1 != None:
        f += 1
    if kst2 != None:
        f += 2

    if f == 1:
        R.sde_targi1_pln = swd
        R.sde_targi2_pln = zero

    if f == 2:
        R.sde_targi1_pln = zero
        R.sde_targi2_pln = swd

    if f == 3:
        swd = swd/2
        R.sde_targi1_pln = swd
        R.sde_targi2_pln = swd

    R.save()





def CorrectValue(zal_wal, suma_wal):

    if zal_wal.amount == 0.00:
        zal_wal = Money(str(zal_wal.amount), str(suma_wal.currency))

    out = zal_wal - suma_wal
    return out


def SelectCurrent(kasa_euro, kasa_funt, kasa_dolar, stawka): # !!!
    tst = str(stawka.currency)
    if tst == 'EUR':
        out = Money(str(kasa_euro), 'EUR')
    elif tst == 'GBP':
        out = Money(str(kasa_funt), 'GBP')
    elif tst == 'USD':
        out = Money(str(kasa_dolar), 'USD')
    elif tst == 'JPY':
        out = stawka
    elif tst == 'DKK':
        out = stawka
    else:
        out = Money('00.00', 'PLN')
    return out


def CalcCurrencyD(kwota):
    kurs = Money('00.00', 'PLN')
    kurs_data = datetime.datetime.strptime("01.01.2000", '%d.%m.%Y')

    if str(kwota.currency) != 'PLN':

        tab = Waluta.objects.filter(kod=kwota.currency).order_by('-data')
        dataf = datetime.date.today()
        tst = dataf.strftime("%Y-%m-%d")

        poz = ''

        f = False
        ex = False
        for pt in tab:
            if f == True:
                poz = pt
                f = False
                ex = True

            if pt.data == tst:
                f = True

        if ex == False:
            try:
                ind = Waluta.objects.filter(kod=kwota.currency).order_by('-id').values('id')[0]['id']
                poz = Waluta.objects.get(id=(ind))
                am  = poz.kurs.amount
                ku  = poz.kurs
                da  = poz.data
            except:
                zero = Money('00.00', 'PLN')
                am = zero.amount
                ku = zero
                da = datetime.datetime.strptime("01.01.2000", '%d.%m.%Y')

        wartosc = Money(str(kwota.amount * am), PLN)


        kurs = ku
        kurs_data = da

    else:
        wartosc = kwota

    return wartosc, kurs, kurs_data


def CalcCurrencyDS(kwota, data):
    kurs = Money('00.00', 'PLN')
    kurs_data = datetime.datetime.strptime("01.01.2000", '%d.%m.%Y') # data domyślna gdy nie znaleziono
    am = kurs.amount
    ku = kurs


    if str(kwota.currency) != 'PLN':

        tab = Waluta.objects.filter(kod=kwota.currency).order_by('-data')
        tst = data.strftime("%Y-%m-%d")

        f = False
        for r in tab:
            if f == True:
                am = r.kurs.amount
                ku = r.kurs
                kurs_data = r.data
                break

            if r.data == tst:
                f = True

        if f == False:

            try:
                tab = Waluta.objects.filter(kod=kwota.currency).last()
                am = tab.kurs.amount
                ku = tab.kurs
                kurs_data = tab.data
            except:
                wal, efd = SimpleGetRate(kwota.currency)
                am = wal.amount
                ku = wal
                kurs_data = efd

        wartosc = Money(str(kwota.amount * am), PLN)
        kurs = ku

    else:
        wartosc = kwota

    return wartosc, kurs, kurs_data


def CorrectAuto(kwota, stawka):
    if str(kwota.currency) == 'PLN':
        out = Money(str(kwota.amount), str(stawka.currency))
    else:
        out = kwota
    return out


def CalcCurrency(kwota, pk):

    flaga = True

    if str(kwota.currency) != 'PLN':

        tab = Waluta.objects.filter(kod=kwota.currency).order_by('-data')
        dataf = datetime.date.today()
        tst = dataf.strftime("%Y-%m-%d")

        poz = ''

        f = False
        ex = False
        for pt in tab:
            if f == True:
                poz = pt
                f = False
                ex = True

            if pt.data == tst:
                f = True

        if ex == False:
            ind = Waluta.objects.filter(kod=kwota.currency).order_by('-id').values('id')[0]['id']
            poz = Waluta.objects.get(id=(ind))

        wartosc = Money(str(kwota.amount * poz.kurs.amount), PLN)

        d = Delegacja.objects.get(pk=pk)
        d.kurs = poz.kurs
        d.kurs_data = poz.data
        d.save()

        flaga = False

    else:
        wartosc = kwota

    return wartosc, flaga


def CalcWydatki(pk, stawka):
    sum_val = Money('00.00', str(stawka.currency))
    sum_pl = Money('00.00', 'PLN')

    poz = Pozycja.objects.filter(delegacja=pk)
    for p in poz:
        sum_pl += p.kwota_pln
        x = p.kwota_waluta
        if str(x.currency) == str(stawka.currency):
            sum_val += p.kwota_waluta
        else:
            sum_val += Money(str(x.amount), str(stawka.currency))
    return sum_val, sum_pl


def CalcRow(pk):
    out1 = Money('00.00', 'PLN')
    out2 = Money('00.00', 'EUR')
    out3 = Money('00.00', 'GBP')
    out4 = Money('00.00', 'USD')
    out5 = Money('00.00', 'CHF')

    poz = Pozycja.objects.filter(delegacja=pk)
    for p in poz:
        if p.waluta=='PLN':
            out1 += p.kwota_pln

        if p.waluta=='EUR':
            out2 += p.kwota_waluta

        if p.waluta=='GBP':
            out3 += p.kwota_waluta

        if p.waluta=='USD':
            out4 += p.kwota_waluta

        if p.waluta=='CHF':
            out5 += p.kwota_waluta

    d = Delegacja.objects.get(pk=pk)
    d.sum_wydatki1 = out1
    d.sum_wydatki2 = out2
    d.sum_wydatki3 = out3
    d.sum_wydatki4 = out4
    d.sum_wydatki5 = out5
    d.save()


def GetRate(ex):
    url = 'https://api.nbp.pl/api/exchangerates/rates/a/'+ex+'/last/1/?format=json'
    waluta = requests.get(url).json()

    # print("***", waluta)

    for w in waluta['rates']:
        wal = Money(w['mid'], PLN)
        efd = w['effectiveDate']
    return wal, efd


def SimpleGetRate(ex):
    url = 'https://api.nbp.pl/api/exchangerates/rates/a/' + str(ex) + '/last/1/?format=json'
    waluta = requests.get(url).json()

    for w in waluta['rates']:
        wal = Money(w['mid'], PLN)
        efd = w['effectiveDate']

    print("POBRANE NOTOWANIE: ", wal, efd)

    return wal, efd



