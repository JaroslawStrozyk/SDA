from moneyed import Money, PLN
from DELEGATIONS.models import Delegacja
from INVOICES.models import Osoba
from .models import Pensja, Pracownik, Premia_det
from .functions import testQuery
from django.contrib.auth.models import User
from django.db.models import F, Sum
from datetime import datetime, timedelta

'''
Obliczanie wynagrodzenia dla jednej pozycji. Wskaźnik do wiersza przekazywany jest jako parametr (r)
To jest odwzorowanie tabeli z Googla 
'''
def rowCalc(r):

    gotowka = r.wynagrodzenie - r.przelew
    km_wartosc = (r.km_ilosc * r.km_dystans) / 8 * r.km_stawka
    nadgodz = r.nadgodz_ilosc * r.stawka_nadgodz
    del_ilosc_razem = (r.del_ilosc_st * r.stawka_wyj) + (r.del_ilosc_we * (r.stawka_wyj * 2)) # Uwaga! to samo w linii 668 views.py
    razem = r.wynagrodzenie + r.dodatek - r.obciazenie + km_wartosc + nadgodz + del_ilosc_razem + r.premia - r.ppk
    wyplata = razem - r.przelew - r.zaliczka - r.komornik


    r.gotowka = gotowka
    r.km_wartosc = km_wartosc
    r.nadgodz = nadgodz
    r.del_ilosc_razem = del_ilosc_razem
    r.razem = razem
    r.wyplata = wyplata
    r.save()


def rowCalc_c(r):

    gotowka = r.wynagrodzenie - r.przelew
    km_wartosc = (r.km_ilosc * r.km_dystans) / 8 * r.km_stawka
    nadgodz = r.nadgodz_ilosc * r.stawka_nadgodz
    del_ilosc_razem = (r.del_ilosc_st * r.stawka_wyj_rob) + (r.del_ilosc_so * (r.stawka_wyj / 2)) + (r.del_ilosc_we * (r.stawka_wyj * 2))
    del_ilosc_razem = del_ilosc_razem # + r.del_rozli
    razem = (r.wynagrodzenie + r.dodatek - r.obciazenie + km_wartosc + nadgodz + del_ilosc_razem + r.premia - r.ppk) + r.del_rozli
    wyplata = razem - r.przelew - r.zaliczka - r.komornik


    r.gotowka = gotowka
    r.km_wartosc = km_wartosc
    r.nadgodz = nadgodz
    r.del_ilosc_razem = del_ilosc_razem
    r.razem = razem
    r.wyplata = wyplata
    r.save()


'''
Dodatek do modulu importu pliku
'''
def CompareData(tab_data):

    err = ''
    count_ok = 0
    count_er = 0

    for r in tab_data:
        rs = Pensja.objects.filter(rok=r[0], miesiac=r[1], osoba__icontains=r[2].split("-")[0])


        if rs.exists():
            count_ok += 1

            rs = rs.values_list('id')[0][0]  # UWAGA nie zmieniać !!!
            przelew = Money(testQuery(r[3]), PLN)
            suma = Money(testQuery(r[4]), PLN)

            rsw = Pensja.objects.get(pk=rs)
            rsw.przelew = przelew
            rsw.sum_kosztow = suma

            rowCalc(rsw)

        else:
            count_er += 1
            err += "(" + r[2] + ") "

    return count_ok, count_er, err


'''
Filtruje pensje i delegacje wg roku i miesiąca. Listuje Delegacje i dodaje wartości do Pensji. 
Sumuje wszystkie wiersze w miesiącu.
'''

"""
   Wywołania procedury:
       1. => red_worker_mc()
"""
def calc_Del_to_Pensja(mc, rk):
    zero = Money('0.00', 'PLN')

    # Zerowanie kolumny 'del_rozli' w jednym zapytaniu
    Pensja.objects.filter(miesiac=mc, rok=rk).update(del_rozli=zero)

    # Pobranie delegacji i pensji razem
    delegacje = Delegacja.objects.filter(data_rozl__month=mc, data_rozl__year=rk)
    pensje = Pensja.objects.filter(miesiac=mc, rok=rk)

    # Mapowanie nazwisk z delegacji do obiektów Pensja
    pensje_dict = {f"{p.osoba.split(' ')[1]} {p.osoba.split(' ')[0]}": p for p in pensje}

    # Słownik do przechowywania sum delegacji dla każdego pracownika
    suma_delegacji = {}

    for delegacja in delegacje:
        delegacja_tst = str(delegacja.osoba.naz_imie)
        if delegacja_tst in suma_delegacji:
            suma_delegacji[delegacja_tst] += delegacja.roznica_diet_pl
        else:
            suma_delegacji[delegacja_tst] = delegacja.roznica_diet_pl

    # Aktualizacja wartości del_rozli dla każdego pracownika
    for nazwisko, suma in suma_delegacji.items():
        pensja = pensje_dict.get(nazwisko)
        if pensja:
            pensja.del_rozli += suma

    # Batch update
    Pensja.objects.bulk_update(pensje, ['del_rozli'])


    pensje_do_zaktualizowania = []
    pensje = Pensja.objects.filter(miesiac=mc, rok=rk)
    for r in pensje:
        calc_PremDel_to_Pensja(r.id)
        pensje_do_zaktualizowania.append(r)

    # Bulk update dla optymalizacji
    Pensja.objects.bulk_update(pensje_do_zaktualizowania,
                               ['premia', 'del_ilosc_st', 'del_ilosc_so', 'del_ilosc_we', 'del_ilosc_razem', 'suma_pd'])




"""
Wywołania procedury:
    1. => red_worker_mc()
    2. red_worker_mc_redirect() =>
"""
def calc_PremDel_to_Pensja(wo):
    zero = Money('00.00', PLN)

    aggregations = Premia_det.objects.filter(pensja=wo).aggregate(
        prw=Sum('pr_wartosc') + Sum('premia_proj') + Sum('ind_pr_kwota'),
        iws=Sum('del_ilosc_st'),
        iwo=Sum('del_ilosc_so'),
        iww=Sum('del_ilosc_we'),
        ww=Sum('del_ilosc_razem'),
    )
    #
    # # Aktualizacja obiektu Pensja
    # Pensja.objects.filter(pk=wo).update(
    #     premia=F('prw'),
    #     del_ilosc_st=F('iws'),
    #     del_ilosc_so=F('iwo'),
    #     del_ilosc_we=F('iww'),
    #     del_ilosc_razem=F('ww'),
    #     suma_pd=F('ww') + F('prw')
    # )

    prw = aggregations['prw']
    iws = aggregations['iws']
    iwo = aggregations['iwo']
    iww = aggregations['iww']
    ww = aggregations['ww']

    pen = Pensja.objects.get(pk=wo)
    try:
        pen.premia = prw
        pen.del_ilosc_st = iws
        pen.del_ilosc_so = iwo
        pen.del_ilosc_we = iww
        pen.del_ilosc_razem = ww
        sum = ww + prw
        pen.suma_pd = Money(str(sum), PLN)
    except:
        pen.premia = zero
        pen.del_ilosc_st = 0
        pen.del_ilosc_so = 0
        pen.del_ilosc_we = 0
        pen.del_ilosc_razem = zero
        pen.suma_pd = zero
    pen.save()


    pen = Pensja.objects.get(pk=wo)
    rok = str(pen.rok)
    m_c  = pen.miesiac

    return rok, m_c


"""
Konwerter przedziału dat na dni robocze, soboty i niedziele
"""
def licz_dni(d1, d2):
    try:
        # Konwersja stringów na obiekty datetime
        data_start = datetime.strptime(d1, '%Y-%m-%d')
        data_koniec = datetime.strptime(d2, '%Y-%m-%d')

        # Sprawdzenie, czy zakres dat jest prawidłowy
        if data_start > data_koniec:
            return 0, 0, 0

        dni_robocze = 0
        soboty = 0
        niedziele = 0

        # Iteracja przez każdy dzień w zakresie
        while data_start <= data_koniec:
            if data_start.weekday() == 5:  # Sobota
                soboty += 1
            elif data_start.weekday() == 6:  # Niedziela
                niedziele += 1
            else:  # Dni robocze
                dni_robocze += 1

            data_start += timedelta(days=1)

        return dni_robocze, soboty, niedziele

    except:
        # W przypadku błędu, zwróć zera
        return 0, 0, 0



def dni_do_PremDel(d1, d2):
    dni_robocze, soboty, niedziele = licz_dni(d1, d2)
    print("Dni robocze:", dni_robocze, "Soboty:", soboty, "Niedziele:", niedziele)