from django.contrib import admin
from . models import Delegacja

class DelegacjaAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'targi', 'data_od', 'data_do', 'kasa_pln', 'kasa_euro', 'kasa_funt', 'kasa_inna', 'kasa_karta','zrobione']
    search_fields = ['imie', 'nazwisko']
    ordering = ['-data_od' ]

admin.site.register(Delegacja, DelegacjaAdmin)
