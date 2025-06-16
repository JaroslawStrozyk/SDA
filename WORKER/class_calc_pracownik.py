from datetime import datetime, timedelta
from moneyed import Money, PLN
from django.shortcuts import redirect
from django.db.models import Sum
from DELEGATIONS.models import Delegacja
from .calculate import licz_dni
from .models import Pracownik, Pensja, Premia_det
from django.db.models import F


class CalcPracownik:

    """
    Wywołania procedury:
        1. => worker_pr_add()
        2. => worker_pr_edit()
    """
    def oblicz_staz_pracy(self ,staz_p, data_zatrudnienia):
        roz = 0
        staz = int(staz_p)
        if staz == 0:
            if data_zatrudnienia != "":
                d_zat = datetime.strptime(data_zatrudnienia, '%d.%m.%Y')
                t = datetime.today()
                if d_zat != None:
                    roz = round((t - d_zat) / timedelta(days=365))
        else:
            roz = staz
        return roz

    """
    Wywołania procedury:
        1. => worker_start()
        2. urls => gen_staz()
    """

    def oblicz_wszystkim_staz_pracy(self):
        t = datetime.today().date()
        for prac in Pracownik.objects.filter(pracuje=True):
            d_zat = prac.data_zat
            if d_zat != None:
                roz = round((t - d_zat) / timedelta(days=365))
            else:
                roz = 0
            prac.staz = roz
            prac.save()

    """
    Wywołania procedury:
        1. => worker_pr_add()
        2. => worker_pr_edit()
    """
    def oblicz_stawke_wyj(self, pensja):
        pens = Money(str(pensja), PLN)
        pens = (pens / 168) * 8
        return pens

    """
    Wywołania procedury:
        1. => worker_pr_update()
        2. => worker_pr_update_prev()
    """
    def pracownik_do_pensji(self, rok, bmc):
        pracownicy_qs = Pracownik.objects.filter(pracuje=True, lp_biuro=True)
        pensje_qs = Pensja.objects.filter(rok=rok, miesiac=bmc)

        pracownik_ids = set(pracownicy_qs.values_list('id', flat=True))
        pensja_pracownik_ids = set(pensje_qs.values_list('pracownik', flat=True))

        # Nowi pracownicy do dodania do Pensja
        nowi_pracownicy_ids = pracownik_ids - pensja_pracownik_ids
        nowi_pracownicy = Pracownik.objects.filter(id__in=nowi_pracownicy_ids)
        nowe_pensje = [Pensja(
            pracownik=pracownik,
            osoba=f"{pracownik.nazwisko} {pracownik.imie}",
            wynagrodzenie=pracownik.pensja_ust,
            ppk=pracownik.ppk,
            stawka_wyj=pracownik.stawka_wyj,
            stawka_wyj_rob=pracownik.stawka_wyj_rob,
            rok=rok,
            miesiac=bmc
        ) for pracownik in nowi_pracownicy]

        # Usunięci pracownicy do usunięcia z Pensja
        usunieci_pracownicy_ids = pensja_pracownik_ids - pracownik_ids
        Pensja.objects.filter(pracownik_id__in=usunieci_pracownicy_ids).delete()

        # Aktualizacja istniejących rekordów Pensja
        do_aktualizacji = []
        for pensja in pensje_qs:
            if pensja.pracownik_id in pracownik_ids:
                pracownik = pracownicy_qs.get(id=pensja.pracownik_id)
                pensja.wynagrodzenie = pracownik.pensja_ust
                pensja.ppk = pracownik.ppk
                pensja.stawka_wyj = pracownik.stawka_wyj
                pensja.stawka_wyj_rob = pracownik.stawka_wyj_rob
                do_aktualizacji.append(pensja)

        Pensja.objects.bulk_update(do_aktualizacji,['wynagrodzenie', 'ppk', 'stawka_wyj', 'stawka_wyj_rob'])
        Pensja.objects.bulk_create(nowe_pensje)

    """
    Wywołania procedury:
        1. => red_worker_mc()
        2. => worker_mc()
        3. => worker_mc_arch()
    """
    def calc_Del_to_Pensja(self, mc, rk):
        # print("class calc_pracownik => calc_Del_to_Pensja() ", datetime.now())
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

        # Pobranie obiektów Pensja
        pensje_do_zaktualizowania = []
        pensje = Pensja.objects.filter(miesiac=mc, rok=rk)
        for r in pensje:
            self.calc_PremDel_to_Pensja(r.id)
            pensje_do_zaktualizowania.append(r)

        # Bulk update dla optymalizacji
        Pensja.objects.bulk_update(pensje_do_zaktualizowania,['premia', 'del_ilosc_st', 'del_ilosc_so', 'del_ilosc_we', 'del_ilosc_razem','suma_pd'])

        # Suma del_rozli, del_ilosc_razem i premii
        for p in Pensja.objects.filter(miesiac=mc, rok=rk):
            p.suma_pd = p.del_rozli + p.del_ilosc_razem + p.premia
            p.save()

       # Do sprawdzenia ten kod wywala błedy
       #  Pensja.objects.filter(miesiac=mc, rok=rk).update(suma_pd=F('del_rozli') + F('del_ilosc_razem') + F('premia'))


    """
    Wywołania procedury:
        1. => red_worker_mc()
        2. red_worker_mc_redirect() =>
    """
    def calc_PremDel_to_Pensja(self, wo):
        # print("class calc_pracownik => calc_PremDel_to_Pensja() ", datetime.now())
        zero = Money('00.00', PLN)

        aggregations = Premia_det.objects.filter(pensja=wo).aggregate(
            prw=Sum('pr_wartosc') + Sum('premia_proj') + Sum('ind_pr_kwota'),
            iws=Sum('del_ilosc_st'),
            iwo=Sum('del_ilosc_so'),
            iww=Sum('del_ilosc_we'),
            ww=Sum('del_ilosc_razem'),
        )

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
        m_c = pen.miesiac

        return rok, m_c

    """
     Wywołania procedury:
        1. red_worker_mc_add() => 
        2. red_worker_mc_edit() => 
    """
    def calc_DelegPremia(self, pz, wo):
        stawka_wyj = Pensja.objects.get(pk=wo).stawka_wyj
        stawka_wyj_rob = Pensja.objects.get(pk=wo).stawka_wyj_rob
        # suma delegacji = dni robocze * stawka stała + niedziele * (2 * stawka wyliczona) + soboty * (1,5  * stawka wyliczona)
        deleg = (pz.del_ilosc_st * stawka_wyj_rob) + (pz.del_ilosc_we * (stawka_wyj * 2)) + (pz.del_ilosc_so * (stawka_wyj + (stawka_wyj / 2)))
        # 1% z kwoty sprzedaży
        premia = Money(str(float(pz.kw_sprzedazy.amount) * 0.01), PLN)
        return deleg, premia




