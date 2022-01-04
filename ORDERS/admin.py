from django.contrib import admin
from .models import NrSDE, NrMPK, Zamowienie

class NrSDEAdmin(admin.ModelAdmin):
    list_display = [
        'rok', 'nazwa', 'nazwa_id', 'klient', 'targi', 'opis', 'rks', 'mcs', 'pm',  'uwagi', 'sum_direct',
        'sum_cash'
    ]
    ordering = ['-nazwa']

class NrMPKAdmin(admin.ModelAdmin):
    list_display = ['rok', 'nazwa', 'sum_zam', 'sum_zal', 'opis', 'uwagi']
    ordering = ['nazwa']


class ZamowienieAdmin(admin.ModelAdmin):
    list_display = [
        'rok', 'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_sde', 'nr_mpk', 'nr_dok1',
        'zal1', 'nr_dok2', 'zal2', 'nr_dok3', 'zal3', 'kwota_netto', 'kwota_brutto', 'data_zam', 'data_dost', 'data_fv', 'nr_fv',
        'roz', 'kontrola', 'uwagi', 'inicjaly', 'kwota_netto_pl', 'kurs_walut'
    ]
    ordering = ['-data_zam']



admin.site.register(NrSDE, NrSDEAdmin)
admin.site.register(NrMPK, NrMPKAdmin)
admin.site.register(Zamowienie, ZamowienieAdmin)

admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"