from django.contrib import admin
from . models import Delegacja, Dieta, Pozycja

class DelegacjaAdmin(admin.ModelAdmin):
    list_display = [
        'dataz', 'numer', 'osoba', 'targi', 'lok_targi', 'data_od', 'data_do', 'cel_wyj', 'transport', 'kasa_pln',
        'kasa_euro', 'kasa_funt', 'kasa_dolar', 'kasa_inna', 'kasa_karta', 'zrobione', 'confirm','dc_rozpo', 'dc_zakon',
        'przekr_gran', 'powrot_kraj', 'sniadanie', 'obiad', 'kolacja', 'dieta_kr', 'dieta_za', 'dieta_za_zl', 'dieta_razem',
        'wydatki_sum',  'kurs', 'kurs_data',
        'silnik_poj', 'data_rozl', 'data_pobr_zal', 'kod_sde_targi1', 'kod_sde_targi1'
    ]
    search_fields = ['osoba']
    ordering = ['-data_od']


class DietaAdmin(admin.ModelAdmin):
    list_display = [
        'panstwo', 'dieta', 'nocleg'
    ]


class PozycjaAdmin(admin.ModelAdmin):
    list_display = [
        'delegacja', 'pozycja', 'kwota_waluta', 'kwota_pln'
    ]


admin.site.register(Delegacja, DelegacjaAdmin)
admin.site.register(Dieta, DietaAdmin)
admin.site.register(Pozycja, PozycjaAdmin)