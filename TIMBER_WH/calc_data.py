from TIMBER_WH.models import Przychod, RozchodSzczegoly, Rozchod, Plyta
from datetime import date
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from moneyed import Money, PLN


def rozlicz_rozchod(plyta):
    rozchody = Rozchod.objects.filter(plyta=plyta).order_by('data')
    przychody = list(Przychod.objects.filter(plyta=plyta).order_by('data'))

    if not rozchody.exists():
        print(f"Brak rozchodów dla płyty: {plyta.nazwa} [{plyta.id}]")

        # Jak nie ma rozchodu to podliczmy tylko przychód
        pr = Przychod.objects.filter(plyta=plyta).order_by('data')
        cena = Money('00.00', PLN)
        ilosc = 0
        for p in pr:
             ilosc += p.ilosc
             cena = p.cena_j
        pl = Plyta.objects.get(pk=plyta.id)
        pl.stan = ilosc
        pl.cena = cena
        pl.save()

        return

    with transaction.atomic():
        stan_magazynu = sum(przychod.ilosc for przychod in przychody)
        wykorzystane_przychody = []

        for rozchod in rozchody:
            # Usuń istniejące szczegóły dla rozchodu
            RozchodSzczegoly.objects.filter(rozchod=rozchod).delete()

            pozostala_ilosc = rozchod.ilosc

            for przychod in przychody:
                if pozostala_ilosc <= 0:
                    break

                ilosc_do_pobrania = min(pozostala_ilosc, przychod.ilosc - sum(
                    s['ilosc'] for s in wykorzystane_przychody if s['przychod'] == przychod))

                if ilosc_do_pobrania <= 0:
                    continue

                kwota = ilosc_do_pobrania * przychod.cena_j.amount

                RozchodSzczegoly.objects.create(
                    rozchod=rozchod,
                    przychod=przychod,
                    ilosc=ilosc_do_pobrania,
                    cena_j=przychod.cena_j,
                    kwota=kwota
                )

                wykorzystane_przychody.append({
                    'przychod': przychod,
                    'ilosc': ilosc_do_pobrania,
                })

                pozostala_ilosc -= ilosc_do_pobrania

            if pozostala_ilosc > 0:
                print(f"Brak wystarczającego stanu magazynowego dla rozchodu: {rozchod.doc_id}")

            # Przelicz kwotę rozchodu na podstawie szczegółów
            rozchod.kwota = RozchodSzczegoly.objects.filter(rozchod=rozchod).aggregate(
                kwota_sum=Sum('kwota')
            )['kwota_sum'] or Decimal('0.00')
            rozchod.save()

        # Aktualizacja pola plyta.stan
        plyta.stan = stan_magazynu - sum(
            szczegol['ilosc'] for szczegol in wykorzystane_przychody
        )
        # Aktualizacja pola plyta.cena na podstawie ostatniego rozchodu
        ostatni_rozchod = RozchodSzczegoly.objects.filter(rozchod__plyta=plyta).order_by('-rozchod__data').first()
        plyta.cena = ostatni_rozchod.cena_j if ostatni_rozchod else plyta.cena
        plyta.save()

    print(f"Rozliczono wszystkie rozchody dla płyty: {plyta.nazwa}")




# def rozlicz_rozchod(plyta):
#     rozchody = Rozchod.objects.filter(plyta=plyta).order_by('data')
#     przychody = list(Przychod.objects.filter(plyta=plyta).order_by('data'))
#
#     if not rozchody.exists():
#         print(f"Brak rozchodów dla płyty: {plyta.nazwa}")
#         return
#
#     with transaction.atomic():
#         stan_magazynu = sum(przychod.ilosc for przychod in przychody)
#         wykorzystane_przychody = []
#
#         for rozchod in rozchody:
#             pozostala_ilosc = rozchod.ilosc
#
#             for przychod in przychody:
#                 if pozostala_ilosc <= 0:
#                     break
#
#                 ilosc_do_pobrania = min(pozostala_ilosc, przychod.ilosc - sum(
#                     s['ilosc'] for s in wykorzystane_przychody if s['przychod'] == przychod))
#
#                 if ilosc_do_pobrania <= 0:
#                     continue
#
#                 kwota = ilosc_do_pobrania * przychod.cena_j.amount
#
#                 RozchodSzczegoly.objects.create(
#                     rozchod=rozchod,
#                     przychod=przychod,
#                     ilosc=ilosc_do_pobrania,
#                     cena_j=przychod.cena_j,
#                     kwota=kwota
#                 )
#
#                 wykorzystane_przychody.append({
#                     'przychod': przychod,
#                     'ilosc': ilosc_do_pobrania,
#                 })
#
#                 pozostala_ilosc -= ilosc_do_pobrania
#
#             if pozostala_ilosc > 0:
#                 print(f"Brak wystarczającego stanu magazynowego dla rozchodu: {rozchod.doc_id}")
#                 # raise ValueError(f"Brak wystarczającego stanu magazynowego dla rozchodu: {rozchod.doc_id}")
#
#             rozchod.kwota = RozchodSzczegoly.objects.filter(rozchod=rozchod).aggregate(
#                 kwota_sum=Sum('kwota')
#             )['kwota_sum'] or Decimal('0.00')
#             rozchod.save()
#
#         plyta.stan = stan_magazynu - sum(
#             szczegol['ilosc'] for szczegol in wykorzystane_przychody
#         )
#         ostatni_rozchod = RozchodSzczegoly.objects.filter(rozchod__plyta=plyta).order_by('-rozchod__data').first()
#         plyta.cena = ostatni_rozchod.cena_j if ostatni_rozchod else plyta.cena
#         plyta.save()
#
#     print(f"Rozliczono wszystkie rozchody dla płyty: {plyta.nazwa}")




















# def rozlicz_rozchod(plyta):
#     # Pobierz nierozliczone rozchody dla danej płyty
#     rozchody = Rozchod.objects.filter(plyta=plyta).order_by('data')
#     przychody = Przychod.objects.filter(plyta=plyta, ilosc__gt=0).order_by('data')
#
#     if not rozchody.exists():
#         print(f"Brak rozchodów dla płyty: {plyta.nazwa}")
#         return
#
#     with transaction.atomic():
#         for rozchod in rozchody:
#             pozostala_ilosc = rozchod.ilosc
#
#             for przychod in przychody:
#                 if pozostala_ilosc <= 0:
#                     break
#
#                 dostepna_ilosc = przychod.ilosc
#                 ilosc_do_pobrania = min(pozostala_ilosc, dostepna_ilosc)
#                 kwota = ilosc_do_pobrania * przychod.cena_j.amount
#
#                 RozchodSzczegoly.objects.create(
#                     rozchod=rozchod,
#                     przychod=przychod,
#                     ilosc=ilosc_do_pobrania,
#                     cena_j=przychod.cena_j,
#                     kwota=kwota
#                 )
#
#                 # Aktualizacja ilości w przychodzie
#                 przychod.ilosc -= ilosc_do_pobrania
#                 przychod.save()
#
#                 # Zmniejszenie ilości do rozliczenia
#                 pozostala_ilosc -= ilosc_do_pobrania
#
#             if pozostala_ilosc > 0:
#                 raise ValueError(f"Brak wystarczającego stanu magazynowego dla rozchodu: {rozchod.doc_id}")
#
#             # Aktualizacja sumy kwoty w rozchodzie
#             rozchod.kwota = RozchodSzczegoly.objects.filter(rozchod=rozchod).aggregate(
#                 kwota_sum=Sum('kwota')
#             )['kwota_sum'] or Decimal('0.00')
#             rozchod.save()
#
#         # Aktualizacja stanu magazynowego i ostatniej ceny płyty
#         plyta.stan = przychody.aggregate(stan_sum=Sum('ilosc'))['stan_sum'] or Decimal('0.0')
#         ostatni_rozchod = RozchodSzczegoly.objects.filter(rozchod__plyta=plyta).order_by('-rozchod__data').first()
#         plyta.cena = ostatni_rozchod.cena_j if ostatni_rozchod else plyta.cena
#         plyta.save()
#
#     print(f"Rozliczono wszystkie rozchody dla płyty: {plyta.nazwa}")



def test_rozlicz_rozchod():
    with transaction.atomic():
        # Tworzenie przykładowej płyty
        plyta = Plyta.objects.create(
            prod_id=112345,
            magazyn='MAGAZYN1',
            nazwa='Płyta testowa',
            stan=0,
            cena=0,
        )

        # Tworzenie przychodów
        Przychod.objects.bulk_create([
            Przychod(plyta=plyta, data=date(2024, 12, 1), ilosc=10, cena_j=Decimal('20.00')),
            Przychod(plyta=plyta, data=date(2024, 12, 10), ilosc=5, cena_j=Decimal('22.00')),
            Przychod(plyta=plyta, data=date(2024, 12, 20), ilosc=15, cena_j=Decimal('24.00')),
        ])

        # Tworzenie rozchodów
        Rozchod.objects.bulk_create([
            Rozchod(plyta=plyta, data=date(2024, 12, 3), ilosc=8),
            Rozchod(plyta=plyta, data=date(2024, 12, 21), ilosc=9),
            Rozchod(plyta=plyta, data=date(2024, 12, 23), ilosc=7),
        ])

        # Rozliczanie
        rozlicz_rozchod(plyta)

        # Pobieranie wyników
        przychody = Przychod.objects.filter(plyta=plyta)
        rozchody = Rozchod.objects.filter(plyta=plyta)
        szczegoly = RozchodSzczegoly.objects.filter(rozchod__plyta=plyta).order_by('rozchod__data', 'przychod__data')

        # Wyświetlanie wyników
        print(f"Płyta: {plyta.nazwa}")
        print(f"Stan magazynowy: {plyta.stan}")
        print(f"Ostatnia cena: {plyta.cena}")
        print("\nSzczegóły rozchodów:")
        for szczegol in szczegoly:
            print(f"  Rozchod: {szczegol.rozchod.data}, Przychod: {szczegol.przychod.data}, "
                  f"Ilość: {szczegol.ilosc}, Cena jednostkowa: {szczegol.cena_j}, Kwota: {szczegol.kwota}")

        print("\nPodsumowanie przychodów:")
        for przychod in przychody:
            print(f"  Data: {przychod.data}, Ilość: {przychod.ilosc}, Cena jednostkowa: {przychod.cena_j}")

        print("\nPodsumowanie rozchodów:")
        for rozchod in rozchody:
            print(f"  Data: {rozchod.data}, Ilość: {rozchod.ilosc}, Kwota: {rozchod.kwota}")





























# #rozchod = Rozchod.objects.get(id=93)  # Rozchod do przetworzenia
# def rozlicz_rozchod(rozchod):
#     przychody = Przychod.objects.filter(plyta=rozchod.plyta, ilosc__gt=0).order_by('data')
#     pozostala_ilosc = rozchod.ilosc
#
#     with transaction.atomic():
#         for przychod in przychody:
#             if pozostala_ilosc <= 0:
#                 break
#
#             dostepna_ilosc = przychod.ilosc
#             ilosc_do_pobrania = min(pozostala_ilosc, dostepna_ilosc)
#             kwota = ilosc_do_pobrania * przychod.cena_j.amount
#
#             RozchodSzczegoly.objects.create(
#                 rozchod=rozchod,
#                 przychod=przychod,
#                 ilosc=ilosc_do_pobrania,
#                 cena_j=przychod.cena_j,
#                 kwota=kwota
#             )
#
#             przychod.ilosc -= ilosc_do_pobrania
#             przychod.save()
#
#             pozostala_ilosc -= ilosc_do_pobrania
#
#         if pozostala_ilosc > 0:
#             raise ValueError("Brak wystarczającego stanu magazynowego")
#
#     rozchod.kwota = sum([s.kwota for s in RozchodSzczegoly.objects.filter(rozchod=rozchod)])
#     rozchod.save()


