from django.contrib import admin
from . models import Pracownik, Pensja, Podsumowanie, Import, Stoisko, Premia_det


class PracownikAdmin(admin.ModelAdmin):
    list_display = [
        'imie', 'nazwisko', 'grupa', 'dzial', 'zatrudnienie', 'wymiar', 'data_zat', 'staz', 'pensja_ust',
        'pensja_brutto', 'stawka_godz', 'stawka_wyj', 'uwagi', 'lp_biuro' # , 'stawka_nadgodz', 'ppk', 'dystans',
    ]
    search_fields = ['imie', 'nazwisko']
    ordering = ['nazwisko']


class PensjaAdmin(admin.ModelAdmin):
    list_display = [
        'rok', 'miesiac','pracownik','wynagrodzenie', 'ppk', 'przelew', 'gotowka',
        'dodatek', 'dodatek_opis', 'obciazenie', 'obciazenie_opis', 'km_ilosc', 'km_wartosc',
        'nadgodz_ilosc', 'nadgodz', 'nadgodz_opis', 'del_ilosc_st', 'del_ilosc_we', 'del_ilosc_razem',
        'premia', 'premia_opis', 'razem', 'zaliczka', 'komornik', 'brutto_brutto', 'wyplata', 'sum_kosztow',
        'rozliczono', 'l4', 'uwagi'
    ]
    search_fields = ['wynagrodzenie']


class PodsumowanieAdmin(admin.ModelAdmin):
    list_display = [
        'rok', 'miesiac', 'suma_biuro'
    ]


class ImportAdmin(admin.ModelAdmin):
    list_display = [
        'up_load',
    ]


class StoiskoAdmin(admin.ModelAdmin):
    list_display = [
        'wielkosc', 'w_premii'
    ]


class Premia_detAdmin(admin.ModelAdmin):
    list_display = [
        'pensja', 'projekt', 'pr_wielkosc', 'del_ilosc_st', 'del_ilosc_we',
        'del_ilosc_razem', 'kw_sprzedazy', 'premia_proj', 'ind_pr_kwota'
    ]


admin.site.register(Pracownik, PracownikAdmin)
admin.site.register(Pensja, PensjaAdmin)
admin.site.register(Podsumowanie, PodsumowanieAdmin)
admin.site.register(Import, ImportAdmin)
admin.site.register(Stoisko, StoiskoAdmin)
admin.site.register(Premia_det, Premia_detAdmin)
