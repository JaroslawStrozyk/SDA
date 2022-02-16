from moneyed import Money, PLN, USD, GBP, EUR, CHF
from django.conf import settings



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




def suma_wartosci(pozycje):
    DICT = {}
    zero = Money('00.00', 'PLN')
    suma_c = zero
    fsc = False
    tab = settings.CURRENCIES
    for t in tab:
        DICT[t] = Money('00.00', t)

    for poz in pozycje:
        if poz.data_zak != '':
            c = poz.kwota_netto.currency
            d = poz.kwota_netto.amount
            suma_c += Money(poz.kwota_netto_pl.amount, poz.kwota_netto_pl.currency)
            DICT[str(c)] = Money(d, c) + DICT[str(c)]

    if suma_c > zero:
        suma_c += DICT['PLN']
        fsc = True

    suma = ''
    for i in DICT.items():
        tst = Money('00.00', i[1].currency)
        if i[1] != tst:
            suma += str(i[1].currency) + ': ' + str(i[1].amount) + ' / '
    suma = suma[:-3]
    DICT.clear()
    if len(suma)==0:
        suma = str(zero)
    return suma, suma_c, fsc



