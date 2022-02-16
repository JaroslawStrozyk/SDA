from django.contrib import admin
from . models import Pracownik, Pensja, Import


class PracownikAdmin(admin.ModelAdmin):
    list_display = [
        'imie', 'nazwisko', 'grupa', 'dzial', 'zatrudnienie', 'wymiar', 'data_zat', 'staz',
        'pensja_ust', 'stawka_nadgodz', 'stawka_wyj', 'ppk', 'dystans', 'uwagi'
    ]
    search_fields = ['imie', 'nazwisko']
    ordering = ['nazwisko']


class PensjaAdmin(admin.ModelAdmin):
    list_display = [
        'rok', 'miesiac','pracownik','wynagrodzenie', 'ppk', 'przelew', 'gotowka',
        'dodatek', 'dodatek_opis', 'obciazenie', 'obciazenie_opis', 'km_ilosc', 'km_wartosc',
        'nadgodz_ilosc', 'nadgodz', 'nadgodz_opis', 'del_ilosc_100', 'del_ilosc_50', 'del_ilosc_razem',
        'premia', 'razem', 'zaliczka', 'komornik', 'brutto_brutto', 'wyplata', 'sum_kosztow',
        'rozliczono', 'l4', 'uwagi'
    ]
    search_fields = ['wynagrodzenie']


class ImportAdmin(admin.ModelAdmin):
    list_display = [
        'up_load',
    ]



admin.site.register(Pracownik, PracownikAdmin)
admin.site.register(Pensja, PensjaAdmin)
admin.site.register(Import, ImportAdmin)
