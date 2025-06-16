from django.contrib import admin
from .models import NrSDE, NrMPK, Zamowienie, FlagaSzukania, Nip


class NrSDEAdmin(admin.ModelAdmin):
    list_display = [
        'rok', 'nazwa', 'nazwa_id', 'klient', 'targi', 'stoisko', 'opis', 'rks', 'mcs', 'pm',  'uwagi', 'sum_direct',
        'sum_cash', 'pow_stoisko', 'pow_pietra'
    ]
    ordering = ['-nazwa']


class NrMPKAdmin(admin.ModelAdmin):
    list_display = ['rok', 'nazwa', 'sum_zam', 'sum_zal', 'opis', 'lsde', 'uwagi']
    ordering = ['-rok','-nazwa']


class ZamowienieAdmin(admin.ModelAdmin):
    list_display = [
        'rok', 'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_sde', 'nr_mpk', 'nr_dok1',
        'zal1', 'zal1_bi', 'nr_dok2', 'zal2', 'zal2_bi', 'nr_dok3', 'zal3', 'zal3_bi', 'kwota_netto', 'kwota_brutto',
        'data_zam', 'data_dost', 'data_fv', 'nr_fv', 'roz', 'kontrola', 'uwagi', 'inicjaly', 'kwota_netto_pl', 'kurs_walut',
        'flaga_sz', 'nip_ind', 'nip'
    ]
    ordering = ['-data_zam']


class FlagaSzukaniaAdmin(admin.ModelAdmin):
    list_display = [
        'nazwa', 'uwagi'
    ]


class NipAdmin(admin.ModelAdmin):
    list_display = [
        'nip', 'kontrahent'
    ]





admin.site.register(NrSDE, NrSDEAdmin)
admin.site.register(NrMPK, NrMPKAdmin)
admin.site.register(Zamowienie, ZamowienieAdmin)
admin.site.register(FlagaSzukania, FlagaSzukaniaAdmin)
admin.site.register(Nip, NipAdmin)

admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"
