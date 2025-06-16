# currency_tags.py

from django import template
from moneyed import CURRENCIES

register = template.Library()

@register.filter(name='currency_symbol')
def currency_symbol(currency_code):
    TCURR = {'PLN': 'zł', 'EUR': '€', 'USD': '$', 'GBP': '£'}

    cc = str(currency_code)

    if cc in TCURR:
        return TCURR[cc]
    else:
        # Zwróć kod waluty, jeśli symbol nie jest dostępny
        return cc
