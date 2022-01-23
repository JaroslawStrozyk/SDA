from moneyed import Money, PLN, USD, GBP, EUR, CHF




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


