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
from .models import Firma
import json
from django.db import transaction
from decimal import Decimal
from django.db.models import Min, Sum, Count, Q, Case, When, BooleanField, Value, Exists, OuterRef, Subquery, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def UpgradeSum(pk):
    # Główne wywołanie danych
    sklad = Sklad.objects.filter(nr_sde=pk).order_by('przech_nrpalet')

    # Jeśli brak rekordów, zakończ funkcję
    if not sklad.exists():
        return

    # Obliczamy sumy obu pól
    sumy = sklad.aggregate(
        suma_kosztow=Sum('koszt_przech'),
        suma_powierzchni=Sum('przech_pow')
    )

    # Pobieramy wartości (z obsługą wartości null)
    suma_kosztow = sumy['suma_kosztow'] or Decimal('0.00')
    suma_powierzchni = sumy['suma_powierzchni'] or Decimal('0.00')

    # Obliczenie suma_1m (suma_powierzchni * stawka)
    # Pobieramy stawkę z pierwszego rekordu, zakładając że jest taka sama dla wszystkich w ramach nr_sde
    if sklad.exists():
        pierwszy_rekord = sklad.first()
        stawka = pierwszy_rekord.stawka
        # Obliczamy suma_1m (powierzchnia * stawka)
        suma_1m = stawka.amount * suma_powierzchni
        # Tworzymy obiekt Money z obliczoną wartością i walutą z stawki
        suma_1m_money = Money(suma_1m, stawka.currency)
    else:
        # Domyślna wartość jeśli nie ma rekordów (choć ten przypadek jest już obsługiwany wcześniej)
        suma_1m_money = Money(0, 'EUR')

    # Sprawdzanie pól czas_od, czas_do i faktura dla określenia flaga_op
    flaga_op_value = 2  # Domyślnie zakładamy, że wszystko jest kompletne (poziom 2)

    # Sprawdzamy czy istnieje jakikolwiek rekord, gdzie brakuje czas_od, czas_do
    missing_date_records = sklad.filter(Q(czas_od__isnull=True) | Q(czas_do__isnull=True))

    if missing_date_records.exists():
        # Jeśli brakuje jakichkolwiek dat, ustawiamy flagę na 0
        flaga_op_value = 0
    else:
        # Sprawdzamy czy wszystkie rekordy mają fakturę
        for record in sklad:
            if record.okres is None or record.okres.faktura is None or record.okres.faktura == '':
                # Znaleziono rekord bez faktury, ale z datami
                flaga_op_value = 1
                break

    # Aktualizujemy wszystkie rekordy jednym zapytaniem, dodając suma_1m
    sklad.update(
        suma=suma_kosztow,
        suma_pow=suma_powierzchni,
        suma_1m=suma_1m_money,
        flaga_op=flaga_op_value
    )

# Tylko dla całej tabeli
def AllSkladRecalculate():
    for s in Sklad.objects.all():
        force_recalculation(s.pk)



def CalKosztPrzechowywania(przech_pow, stawka, ilosc_dni):
    stala = (stawka / 30) * ilosc_dni
    out = stala * przech_pow
    #print(">>> ", stala, out)
    return out




def force_recalculation(sklad_id):
    """
    Wymusza przeliczenie kosztów dla rekordu Sklad.

    Args:
        sklad_id: ID rekordu Sklad
    """
    try:
        rekord = Sklad.objects.get(pk=sklad_id)
    except Sklad.DoesNotExist:
        return False

    # Jeśli rekord nie ma okresu, nie ma co przeliczać
    if not rekord.okres:
        return False

    # Sprawdź, czy wszystkie niezbędne dane są dostępne
    if not rekord.okres or not rekord.czas_od or not rekord.czas_do or not rekord.stawka.amount:
        return False

    # Synchronizuj daty z okresem
    rekord.czas_od = rekord.okres.data_od
    rekord.czas_do = rekord.okres.data_do

    # Oblicz liczbę dni
    delta = rekord.czas_do - rekord.czas_od
    rekord.ilosc_dni = delta.days + 1

    # Ustaw stawkę z okresu
    rekord.stawka = rekord.okres.stawka

    # Oblicz koszt przechowywania
    if rekord.przech_pow and rekord.ilosc_dni:
        if not rekord.element_katalogowy:
            # SCENARIUSZ 1: Ręczne dodanie elementu
            rekord.koszt_przech = CalKosztPrzechowywania(rekord.przech_pow, rekord.stawka.amount, rekord.ilosc_dni) # (rekord.przech_pow * (rekord.stawka.amount / 30) * rekord.ilosc_dni)
            rekord.liczyc = True
        elif rekord.element_katalogowy:
            # SCENARIUSZ 2: Wybór z elementu katalogowego
            existing_elements = Sklad.objects.filter(
                element_katalogowy=rekord.element_katalogowy,
                okres=rekord.okres
            ).exclude(pk=rekord.pk).exists()

            # Jeśli to pierwszy element katalogowy w okresie, ustaw liczyc=True
            if not existing_elements:
                rekord.liczyc = True

            if rekord.liczyc:
                rekord.koszt_przech = CalKosztPrzechowywania(rekord.przech_pow, rekord.stawka.amount, rekord.ilosc_dni) #(rekord.przech_pow * (rekord.stawka.amount / 30) * rekord.ilosc_dni)

    # Zapisz rekord bez wywoływania standardowej metody save
    # aby uniknąć rekursji i nadpisania wartości
    Sklad.objects.filter(pk=rekord.pk).update(
        czas_od=rekord.czas_od,
        czas_do=rekord.czas_do,
        ilosc_dni=rekord.ilosc_dni,
        stawka=rekord.stawka,
        koszt_przech=rekord.koszt_przech,
        liczyc=rekord.liczyc
    )

    return True


def update_element_katalogowy_status():
    """
    Zoptymalizowana funkcja aktualizująca pola 'wydany' i 'licznik' w tabeli ElementKatalogowy
    na podstawie powiązanych wpisów w tabeli Sklad.
    """
    from django.db.models import Count, Q, Case, When, BooleanField, Value

    # Oblicz licznik dla każdego elementu (ilość powiązanych wpisów w Sklad)
    licznik_query = Sklad.objects.filter(
        element_katalogowy__isnull=False
    ).values(
        'element_katalogowy'
    ).annotate(
        count=Count('id')
    )

    # Przygotuj słownik liczników {id_elementu: liczba_wpisów}
    licznik_dict = {item['element_katalogowy']: item['count'] for item in licznik_query}

    # Znajdź elementy, które są aktualnie wydane (mają wpis w Sklad z wydano_data, ale bez zwroco_data)
    wydane_elementy = set(Sklad.objects.filter(
        element_katalogowy__isnull=False,
        wydano_data__isnull=False,
        zwroco_data__isnull=True
    ).values_list('element_katalogowy', flat=True).distinct())

    # Pobierz wszystkie aktywne elementy katalogowe
    elementy = ElementKatalogowy.objects.filter(aktywny=True)

    # Przygotuj listę obiektów do aktualizacji
    obiekty_do_aktualizacji = []

    for element in elementy:
        zmiana = False

        # Aktualizuj licznik
        nowy_licznik = licznik_dict.get(element.id, 0)
        if element.licznik != nowy_licznik:
            element.licznik = nowy_licznik
            zmiana = True

        # Aktualizuj status wydany
        nowy_wydany = element.id in wydane_elementy
        if element.wydany != nowy_wydany:
            element.wydany = nowy_wydany
            zmiana = True

        # Jeśli coś się zmieniło, dodaj do listy do aktualizacji
        if zmiana:
            obiekty_do_aktualizacji.append(element)

    # Aktualizuj tylko te obiekty, które rzeczywiście się zmieniły
    if obiekty_do_aktualizacji:
        # Używamy bulk_update, aby zminimalizować liczbę zapytań do bazy danych
        ElementKatalogowy.objects.bulk_update(obiekty_do_aktualizacji, ['licznik', 'wydany'])


# def UpgradeDependence(id):
#     """
#     Aktualizuje wszystkie powiązane rekordy Sklad po zmianie wartości w OkresPrzechowywania.
#
#     Args:
#         id: ID rekordu OkresPrzechowywania, który został zmieniony
#     """
#     # Pobierz aktualny obiekt okresu przechowywania
#     try:
#         okres = OkresPrzechowywania.objects.get(pk=id)
#     except OkresPrzechowywania.DoesNotExist:
#         return
#
#     # Sprawdź, czy okres został zmieniony od ostatniego zapisu
#     if okres.data_modyfikacji == okres.data_utworzenia:
#         return  # Nowy rekord, nie ma potrzeby aktualizacji
#
#     # Pobierz wszystkie powiązane rekordy Sklad
#     powiazane_rekordy = Sklad.objects.filter(okres_id=id)
#
#     # Jeśli nie ma powiązanych rekordów, nie ma nic do aktualizacji
#     if not powiazane_rekordy.exists():
#         return
#
#     # Wykonaj aktualizację w transakcji, aby zapewnić spójność danych
#     with transaction.atomic():
#         for rekord in powiazane_rekordy:
#             # Sprawdź, czy dane rekordu wymagają aktualizacji
#             zmiana_wymagana = False
#
#             # Zachowaj oryginalną wartość koszt_przech do użycia później
#             oryginalny_koszt = rekord.koszt_przech
#
#             # Sprawdź, czy daty się zmieniły
#             if rekord.czas_od != okres.data_od or rekord.czas_do != okres.data_do:
#                 zmiana_wymagana = True
#                 rekord.czas_od = okres.data_od
#                 rekord.czas_do = okres.data_do
#
#                 # Aktualizacja liczby dni przechowywania
#                 delta = rekord.czas_do - rekord.czas_od
#                 rekord.ilosc_dni = delta.days + 1  # Włącznie z początkiem i końcem
#
#             # Sprawdź, czy stawka się zmieniła
#             if rekord.stawka.amount != okres.stawka.amount:
#                 zmiana_wymagana = True
#                 rekord.stawka = okres.stawka
#
#             # Sprawdź, czy status zwolnienia się zmienił
#             if rekord.zwolnione != okres.zwolnione:
#                 zmiana_wymagana = True
#                 rekord.zwolnione = okres.zwolnione
#
#             # Jeśli wymagana jest zmiana, przelicz ponownie koszty przechowywania
#             if zmiana_wymagana:
#                 # Przelicz koszty tylko jeśli rekord ma wszystkie potrzebne dane
#                 if (rekord.liczyc and rekord.przech_pow and rekord.stawka.amount and
#                         rekord.czas_od and rekord.czas_do and rekord.ilosc_dni):
#                     # Aktualizuj koszt_przech niezależnie od statusu zwolnione
#                     rekord.koszt_przech = (rekord.przech_pow * (rekord.stawka.amount / 30) * rekord.ilosc_dni)
#
#                     # Obsługa pola zwolnione - ustawianie odpowiednich wartości w suma i suma_zw
#                     if rekord.zwolnione:
#                         rekord.suma = 0
#                         rekord.suma_zw = rekord.koszt_przech
#                     else:
#                         rekord.suma = rekord.koszt_przech
#                         rekord.suma_zw = 0
#                 else:
#                     # Jeśli nie można przeliczyć kosztów, zachowaj oryginalną wartość koszt_przech
#                     rekord.koszt_przech = oryginalny_koszt
#
#                     # Aktualizuj sumę i sumę_zw na podstawie koszt_przech
#                     if rekord.zwolnione:
#                         rekord.suma = 0
#                         rekord.suma_zw = rekord.koszt_przech
#                     else:
#                         rekord.suma = rekord.koszt_przech
#                         rekord.suma_zw = 0
#
#                 # Zapisz zaktualizowany rekord, ale unikamy wywołania metody save()
#                 # aby nie uruchamiać dodatkowej logiki która mogłaby nadpisać nasze zmiany
#                 Sklad.objects.filter(pk=rekord.pk).update(
#                     czas_od=rekord.czas_od,
#                     czas_do=rekord.czas_do,
#                     ilosc_dni=rekord.ilosc_dni,
#                     stawka=rekord.stawka,
#                     zwolnione=rekord.zwolnione,
#                     koszt_przech=rekord.koszt_przech,
#                     suma=rekord.suma,
#                     suma_zw=rekord.suma_zw
#                 )
#
#     # Aktualizuj pola sumaryczne w rekordzie okresu
#     update_summary(id)


def UpgradeDependence(id):
    """
    Aktualizuje wszystkie powiązane rekordy Sklad po zmianie wartości w OkresPrzechowywania.

    Args:
        id: ID rekordu OkresPrzechowywania, który został zmieniony
    """
    # from django.db import transaction

    # Pobierz aktualny obiekt okresu przechowywania
    try:
        okres = OkresPrzechowywania.objects.get(pk=id)
    except OkresPrzechowywania.DoesNotExist:
        return

    # Sprawdź, czy okres został zmieniony od ostatniego zapisu
    # Jeśli data_modyfikacji jest taka sama jak data_utworzenia,
    # to znaczy że rekord nie był modyfikowany (nowy rekord)
    if okres.data_modyfikacji == okres.data_utworzenia:
        return  # Nowy rekord, nie ma potrzeby aktualizacji

    # Pobierz wszystkie powiązane rekordy Sklad
    powiazane_rekordy = Sklad.objects.filter(okres_id=id)

    # Jeśli nie ma powiązanych rekordów, nie ma nic do aktualizacji
    if not powiazane_rekordy.exists():
        return

    # Wykonaj aktualizację w transakcji, aby zapewnić spójność danych
    with transaction.atomic():
        for rekord in powiazane_rekordy:
            # Sprawdź, czy dane rekordu wymagają aktualizacji
            zmiana_wymagana = False

            # Sprawdź, czy daty się zmieniły
            if rekord.czas_od != okres.data_od or rekord.czas_do != okres.data_do:
                zmiana_wymagana = True
                rekord.czas_od = okres.data_od
                rekord.czas_do = okres.data_do

                # Aktualizacja liczby dni przechowywania
                delta = rekord.czas_do - rekord.czas_od
                rekord.ilosc_dni = delta.days + 1  # Włącznie z początkiem i końcem

            # Sprawdź, czy stawka się zmieniła
            if rekord.stawka.amount != okres.stawka.amount:
                zmiana_wymagana = True
                rekord.stawka = okres.stawka

            # Sprawdź, czy status zwolnienia się zmienił
            if rekord.zwolnione != okres.zwolnione:
                zmiana_wymagana = True
                rekord.zwolnione = okres.zwolnione

            # Jeśli wymagana jest zmiana, przelicz ponownie koszty przechowywania
            if zmiana_wymagana:
                # Przelicz koszty tylko jeśli rekord ma wszystkie potrzebne dane
                if (rekord.liczyc and rekord.przech_pow and rekord.stawka.amount and
                        rekord.czas_od and rekord.czas_do and rekord.ilosc_dni):
                    rekord.koszt_przech = CalKosztPrzechowywania(rekord.przech_pow, rekord.stawka.amount, rekord.ilosc_dni) # (rekord.przech_pow * (rekord.stawka.amount / 30) * rekord.ilosc_dni)

                # Zapisz zaktualizowany rekord
                rekord.save()

    # Opcjonalnie: Aktualizuj pola sumaryczne w rekordzie okresu
    update_summary(id)


def update_summary(okres_id):
    """
    Aktualizuje pola sumaryczne w rekordzie OkresPrzechowywania

    Args:
        okres_id: ID rekordu OkresPrzechowywania
    """
    # from django.db.models import Sum

    try:
        okres = OkresPrzechowywania.objects.get(pk=okres_id)
    except OkresPrzechowywania.DoesNotExist:
        return

    # Oblicz sumę kosztów
    koszt_sum = Sklad.objects.filter(
        okres_id=okres_id
    ).aggregate(
        total=Sum('koszt_przech')
    )

    # Oblicz sumę powierzchni
    pow_sum = Sklad.objects.filter(
        okres_id=okres_id,
        liczyc=True
    ).aggregate(
        total=Sum('przech_pow')
    )

    # Przypisz obliczone wartości
    if koszt_sum['total'] is not None:
        okres.suma_kosztow = koszt_sum['total']
    else:
        okres.suma_kosztow = 0

    if pow_sum['total'] is not None:
        okres.suma_powierzchni = pow_sum['total']
    else:
        okres.suma_powierzchni = 0

    # Zapisz zmiany bez wywoływania pełnej metody save()
    OkresPrzechowywania.objects.filter(pk=okres_id).update(
        suma_kosztow=okres.suma_kosztow,
        suma_powierzchni=okres.suma_powierzchni
    )


