from django.contrib import admin
from .models import Sklad, Firma


class SkladAdmin(admin.ModelAdmin):
    list_display = [
        'magazyn', 'nr_sde','przech_nazwa', 'przech_zdjecie', 'przech_zdjecie2', 'przech_pow', 'wydano_ilosc',
        'wydano_data', 'zwroco_ilosc', 'zwroco_data', 'zwroco_uwagi', 'czas_od', 'czas_do', 'koszt_przech',
        'uszkodz_zdjecie1', 'uszkodz_zdjecie2', 'uszkodz_zdjecie3', 'uszkodz_zdjecie4', 'suma', 'suma_pow',
        'faktura', 'zwolnione', 'firma', 'dok_pdf1', 'dok_pdf2',  'dok_pdf3', 'dok_pdf4', 'fv_pdf1', 'uwagi', 'do_skasowania'
    ]
    ordering = ['przech_nazwa']

class FirmaAdmin(admin.ModelAdmin):
    list_display = ['nazwa']
    ordering = ['nazwa']


admin.site.register(Sklad, SkladAdmin)
admin.site.register(Firma, FirmaAdmin)

admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"
