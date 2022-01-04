from django.contrib import admin
from .models import Rozliczenie, Pozycja


class NrSDEAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'uwagi']
    ordering = ['nazwa']


class NrMPKAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'opis', 'uwagi']
    ordering = ['nazwa']


class RozliczenieAdmin(admin.ModelAdmin):
    list_display = [
        'rok', 'data_zal', 'data_roz', 'kw', 'nazwisko', 'zal_kwota', 'zal_suma', 'saldo', 'uwagi', 'roz', 'uwagi',
        'kontrola', 'przek'
    ]
    ordering = ['nazwisko']


class PozycjaAdmin(admin.ModelAdmin):
    list_display = [
        'rok', 'nr_roz', 'kontrahent', 'nr_fv', 'kwota_netto', 'kwota_brutto', 'data_zam', 'data_zak', 'opis', 'nr_sde',
        'nr_mpk', 'kontrola', 'uwagi', 'kwota_netto_pl', 'kurs_walut'
    ]


admin.site.register(Rozliczenie, RozliczenieAdmin)
admin.site.register(Pozycja, PozycjaAdmin)

admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"
