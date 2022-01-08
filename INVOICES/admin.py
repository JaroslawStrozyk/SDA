from django.contrib import admin
from .models import Faktura, Osoba


class FakturaAdmin(admin.ModelAdmin):
    list_display = [
        'data', 'imie', 'nazwisko', 'naz_imie', 'rfaktura', 'termin', 'targi',
        'stoisko', 'kwota', 'zaco', 'spec', 'uwagi', 'zrobione', 'confirm'
    ]
    ordering = ['-data']
    
class OsobaAdmin(admin.ModelAdmin):
    list_display = [
        'naz_imie', 'skype', 'email'
    ]
    ordering = ['naz_imie']


admin.site.register(Faktura, FakturaAdmin)
admin.site.register(Osoba, OsobaAdmin)

admin.site.site_header = "Tech SmartDesign"
admin.site.site_title = "SmartDesign"

