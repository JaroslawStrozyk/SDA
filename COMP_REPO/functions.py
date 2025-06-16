from moneyed import Money, EUR
import datetime
import re
from INVOICES.models import Osoba
from TaskAPI.models import Asp
from .models import Sklad
from django.contrib.auth.models import Group
from django.conf import settings

from decimal import Decimal
from django.db import transaction
from datetime import timedelta
from django.db.models import F, Min

def TEST_InfoSend():
    komunikat = "Edycja zakończona."
    nmg = "Jarocin TEST"
    nnazwa = "072_2024"
    ntargi = "Farnborough Air Show 2024"
    nklient = "2Heads Global Design"
    nstoisko = "Rolls Royce chalet"
    sum = "0,00 €"
    sum_zw = "1 616,00 €"
    sum_np = "60,00 €"
    npm = ''
    SendInformation(nmg, nnazwa, ntargi, nklient, nstoisko, sum, sum_zw, sum_np, komunikat, npm)


def SendInformation(nmg, nnazwa, ntargi, nklient, nstoisko, sum, sum_zw, sum_np, komunikat, npm):
    adres = settings.CR_SKYPE_DO_USERS
    cel = settings.CR_TO_TARGET

    cel = 1
    # adres = ['jaroslaw_strozyk']

    try:
        os = Osoba.objects.get(naz_imie=npm)
        pm = os.skype
    except:
        pm = ''

    data = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if pm != '':
        info = ("⮕ " + komunikat + '\n\r\n' \
                + "⮊ MAGAZYN:\n" \
                + "⮡ \u2003" + nmg + "\n\n" \
                + "⮊ SDE:\n" \
                + "⮡ \u2003" + nnazwa + "\n" \
                + "⮊ TARGI:\n" \
                + "⮡ \u2003" + ntargi + "\n" \
                + "⮊ KLIENT:\n" \
                + "⮡ \u2003" + nklient + "\n" \
                + "⮊ STOISKO:\n" \
                + "⮡ \u2003" + nstoisko + "\n" \
                + "⮊ KOSZT/SUMA ZW./SUMA NP.:\u2003\u2003\n" \
                + "⮡ \u2003" + str(sum) + "/" + str(sum_zw) + "/" + str(sum_np) + "\n\n" \
                + "⇨ DATA: " + data + "\n")
        # info = komunikat + '\n\r\n' \
        #        + "MAGAZYN:\u2003\u2007" + nmg + "\n\n" \
        #        + "\u2007\u2007\u2007\u2007SDE:\u2003\u2007" + nnazwa + "\n" \
        #        + "\u2007\u2007TARGI:\u2003\u2007" + ntargi + "\n" \
        #        + "\u2007KLIENT:\u2003\u2007" + nklient + "\n" \
        #        + "STOISKO:\u2003\u2007" + nstoisko + "\n" \
        #        + "\u2007\u2007\u2007SUMA:\u2003\u2007" + str(sum) + "\n\n" \
        #        + "\u2007\u2007\u2007DATA:\u2003\u2007" + data + "\n"
    else:
        info = ("⮕ " + komunikat + '\n\r\n' \
                + "⮊ MAGAZYN:\n" \
                + "⮡ \u2003" + nmg + "\n\n" \
                + "⮊ SDE:\n" \
                + "⮡ \u2003" + nnazwa + "\n" \
                + "⮊ TARGI:\n" \
                + "⮡ \u2003" + ntargi + "\n" \
                + "⮊ KLIENT:\n" \
                + "⮡ \u2003" + nklient + "\n" \
                + "⮊ STOISKO:\n" \
                + "⮡ \u2003" + nstoisko + "\n" \
                + "⮊ KOSZT/SUMA ZW./SUMA NP.:\u2003\u2003\n" \
                + "⮡ \u2003" + str(sum) + "/" + str(sum_zw) + "/" + str(sum_np) + "\n\n" \
                + "⇨ DATA: " + data + "\n")
        # info = komunikat + '\n\r\n' \
        #        + "MAGAZYN:\u2003\u2007" + nmg + "\n\n" \
        #        + "\u2007\u2007\u2007\u2007SDE:\u2003\u2007" + nnazwa + "\n" \
        #        + "\u2007\u2007TARGI:\u2003\u2007" + ntargi + "\n" \
        #        + "\u2007KLIENT:\u2003\u2007" + nklient + "\n" \
        #        + "STOISKO:\u2003\u2007" + nstoisko + "\n" \
        #        + "\u2007\u2007\u2007SUMA:\u2003\u2007" + str(sum) + "\n\n" \
        #        + "\u2007\u2007\u2007DATA:\u2003\u2007" + data + "\n"

    #            + "⮕ ⇨  ⥤ ↳ ➜ ➟ ➠ 🠊 ⮡ ⮊ ● ⬤\n"\
    # info = ("⮕ " + komunikat + '\n\r\n'\
    #        + "⮊ MAGAZYN:\n"\
    #        + "⮡ \u2003" + nmg + "\n\n"\
    #        + "⮊ SDE:\n"\
    #        + "⮡ \u2003" + nnazwa + "\n"\
    #        + "⮊ TARGI:\n"\
    #        + "⮡ \u2003" + ntargi + "\n"\
    #        + "⮊ KLIENT:\n"\
    #        + "⮡ \u2003" + nklient + "\n"\
    #        + "⮊ STOISKO:\n"\
    #        + "⮡ \u2003" + nstoisko + "\n"\
    #        + "⮊ KOSZT/SUMA ZW./SUMA NP.:\u2003\n"\
    #        + "⮡ \u2003" + str(sum) + "/" + str(sum_zw) + "/" + str(sum_np) + "\n\n"\
    #        + "⇨ DATA: " + data + "\n")

    tytul = ''

    if info != '':
        for adr in adres:
            asp = Asp.objects.create(cel=cel, adres=adr, tytul=tytul, info=info, data=data)
            asp.save()
        if pm != '':
            asp = Asp.objects.create(cel=cel, adres=pm, tytul=tytul, info=info, data=data)
            asp.save()






def CalAllCost():
    f = 'Podolany'
    sklad = Sklad.objects.filter(magazyn=f).distinct('nr_sde')

    for sk in sklad:
        CalCost(sk.nr_sde)

    f = 'Szparagowa'
    sklad = Sklad.objects.filter(magazyn=f).distinct('nr_sde')

    for sk in sklad:
        CalCost(sk.nr_sde)


def ChangeStatus(nr_sde):
    cs = Sklad.objects.filter(nr_sde=nr_sde)
    #print("OBJ:", cs)
    for c in cs:
        c.status_pracy = True
        c.save()


def UpdateDokUwagi(pk, nr_sde):
    sk = Sklad.objects.get(pk=pk)
    pdf1 = sk.dok_pdf1
    pdf2 = sk.dok_pdf2
    pdf3 = sk.dok_pdf3
    pdf4 = sk.dok_pdf4
    fv   = sk.fv_pdf1
    uwagi = sk.uwagi
    cs = Sklad.objects.filter(nr_sde=nr_sde)
    for c in cs:
        c.dok_pdf1 = pdf1
        c.dok_pdf2 = pdf2
        c.dok_pdf3 = pdf3
        c.dok_pdf4 = pdf4
        c.fv_pdf1 = fv
        c.uwagi = uwagi
        c.save()


def CalcAdd(pk):
    zero = Money('0.00', EUR)
    sk = Sklad.objects.get(pk=pk)
    pow = sk.przech_sze * sk.przech_gl
    stawka_m = sk.stawka

    stawka_d = zero
    if stawka_m > zero:
        stawka_d = (stawka_m / 30)

    d_start = sk.czas_od
    d_stop = sk.czas_do
    try:
        d_delta = d_stop - d_start
        d_delta = d_delta.days
    except:
        d_delta = 0

    sum = (pow * stawka_d) * d_delta
    sk.przech_pow = pow
    sk.koszt_przech = sum
    sk.save()


def CalSelSde(nr_sde, wst):
    zero = Money('0.00', EUR)
    try:
        sklad = Sklad.objects.filter(nr_sde=nr_sde)
        c_sum = zero
        c_sum_zw = zero
        c_sum_np = zero
        p_sum = 0
        for s in sklad:
            pow = s.przech_sze * s.przech_gl
            p_sum += pow
            stawka_m = wst #s.stawka

            stawka_d = zero
            if stawka_m > zero:
                stawka_d = (stawka_m / 30)

            d_start = s.czas_od
            d_stop = s.czas_do
            try:
                d_delta = d_stop - d_start
                d_delta = d_delta.days
            except:
                d_delta = 0

            sum = (pow * stawka_d) * d_delta
            s.przech_pow = pow

            if (s.zwolnione == True): # or (s.multi_uzycie == True):
                s.koszt_przech = zero
            else:
                s.koszt_przech = sum
            s.stawka = wst
            s.save()
            if (s.faktura != '') and (s.zwolnione == False): # and (s.multi_uzycie == False):
                c_sum += sum
            if (s.faktura == '') and (s.zwolnione == False): # and (s.multi_uzycie == False):
                c_sum_np += sum
            if (s.faktura == '') and (s.zwolnione == True): # and (s.multi_uzycie == False):
                c_sum_zw += sum

        for s in sklad:
            s.suma = c_sum
            s.suma_zw = c_sum_zw
            s.suma_np = c_sum_np
            s.suma_pow = p_sum
            s.save()
    except:
        pass


# Funkcja bez obsługi serwisowej i z optymalizacją operacji na bazie danych
def CalCost(nr_sde):
    zero = Decimal('0.00')
    zero = Money('0.00', EUR)
    sklad = Sklad.objects.filter(nr_sde=nr_sde)

    cal_sum = zero
    cal_sum_zw = zero
    cal_sum_np = zero
    pow_sum = 0

    batch_updates = []
    for s in sklad:
        # Obliczenie powierzchni
        pow = s.przech_sze * s.przech_gl
        pow_sum += pow

        # Obliczenie stawki dziennej
        stawka_d = s.stawka / 30 if s.stawka > zero else zero

        # Obliczenie różnicy dni między d_start a d_stop
        d_delta = (s.czas_do - s.czas_od).days if s.czas_od and s.czas_do else 0

        # Obliczenie kosztu przechowywania
        sum_value = (pow * stawka_d) * d_delta
        s.przech_pow = pow

        # Ustawienie kosztu przechowania z uwzględnieniem zwolnienia
        # s.koszt_przech = zero if s.zwolnione else sum_value
        s.koszt_przech = sum_value # Koszty przechowywania liczone zawsze

        # EWU poprawka liczenia dla elementów powtórnie użytych
        if not s.liczyc and s.multi_uzycie:
            sum_value = zero

        # Określenie warunków dla sum
        if s.faktura and not s.zwolnione:
            cal_sum += sum_value
        elif not s.faktura and not s.zwolnione:
            cal_sum_np += sum_value
        elif not s.faktura and s.zwolnione:
            cal_sum_zw += sum_value
        elif s.faktura and s.zwolnione:
            cal_sum_zw += sum_value


        # Zapisz obiekt do późniejszej aktualizacji
        batch_updates.append(s)

    # Zbiorcze aktualizowanie obiektów
    with transaction.atomic():
        Sklad.objects.bulk_update(batch_updates, ['przech_pow', 'koszt_przech'])

    # Aktualizacja pól sumarycznych
    with transaction.atomic():
        Sklad.objects.filter(nr_sde=nr_sde).update(
            suma=cal_sum,
            suma_zw=cal_sum_zw,
            suma_np=cal_sum_np,
            suma_pow=pow_sum
        )


def CalCostGen(r_sde, test):
    [CalCost(rs.nr_sde, test) for rs in r_sde]


def testQuery(query):
    query = str(query)
    if query.find(",") > -1:
        try:
            q = query.replace(",", ".")
            float(q)
            query = q
        except:
            pass
    return query


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
    gr = ''
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        gr = g.name
    return name_log, inicjaly, gr


def rename_timbers():
    f = 'MAGAZYN1'
    sklad = Sklad.objects.filter(magazyn=f)
    for s in sklad:
        #print(">>>", s.magazyn)
        s.magazyn = 'Szparagowa'
        s.save()

    f = 'MAGAZYN2'
    sklad = Sklad.objects.filter(magazyn=f)
    for s in sklad:
        #print(">>>", s.magazyn)
        s.magazyn = 'Podolany'
        s.save()




def set_multi_calc():
    # Krok 1: Pobierz rekordy z multi_uzycie=True
    sklad_records = Sklad.objects.filter(multi_uzycie=True)

    # Krok 2: Pogrupuj po multi_uzycie_id i znajdź minimalny pk w każdej grupie
    groups = (
        sklad_records.values('multi_uzycie_id')
        .annotate(min_pk=Min('pk'))
    )

    # Krok 3: Resetuj pole liczyc dla wszystkich rekordów
    Sklad.objects.filter(multi_uzycie=True).update(liczyc=False)

    # Krok 4: Ustaw liczyc=True dla rekordów o minimalnym pk w każdej grupie
    for group in groups:
        Sklad.objects.filter(pk=group['min_pk']).update(liczyc=True)


    for s in Sklad.objects.all():
        # Obliczenie różnicy dni między d_start a d_stop
        d_delta = (s.czas_do - s.czas_od).days if s.czas_od and s.czas_do else 0
        s.ilosc_dni = d_delta
        s.save()

def CalcDay(ipk):
    s = Sklad.objects.get(pk=ipk)
    d_delta = (s.czas_do - s.czas_od).days if s.czas_od and s.czas_do else 0
    s.ilosc_dni = d_delta
    s.save()


def format_european_currency(value):
    # Konwersja na string, jeśli wartość jest typu Money
    if not isinstance(value, str):
        value = str(value)

    # Usuwanie znaku waluty, zakładając, że jest na końcu
    match = re.match(r"([\d,\.]+)\s*€", value)
    if not match:
        raise ValueError("Nieprawidłowy format wartości walutowej.")

    numeric_part = match.group(1)

    # Zamiana separatorów: najpierw zamiana przecinków na tymczasowy znak, aby nie stracić danych
    numeric_part = numeric_part.replace(',', 'TEMP').replace('.', ',').replace('TEMP', ' ')

    # Dodanie znaku waluty
    formatted_value = numeric_part + " €"
    return formatted_value
