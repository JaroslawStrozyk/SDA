from django.contrib import admin
from . models import Pracownik, Pensja


class PracownikAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'grupa', 'dzial', 'zatrudnienie', 'wymiar', 'data_zat', 'staz', 'pensja_ust', 'uwagi']
    search_fields = ['imie', 'nazwisko']
    ordering = ['nazwisko']


class PensjaAdmin(admin.ModelAdmin):
    list_display = ['rok', 'miesiac','pracownik','wynagrodzenie', 'ppk', 'przelew', 'gotowka', 'dodatek', 'obciazenie', 'nadgodz_ilosc', 'nadgodz']
    search_fields = ['wynagrodzenie']



admin.site.register(Pracownik, PracownikAdmin)
admin.site.register(Pensja, PensjaAdmin)
