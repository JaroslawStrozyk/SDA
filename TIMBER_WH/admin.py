from django.contrib import admin
from .models import Plyta, Przychod, Rozchod, Zwrot, StanObecny



class PlytaAdmin(admin.ModelAdmin):
    list_display = [
        'magazyn','nazwa', 'stan', 'opis', 'cena', 'prod_id', 'limit', 'inw_stan', 'inw_data'
    ]
    ordering = ['nazwa']


class PrzychodAdmin(admin.ModelAdmin):
    list_display = [
        'zrodlo', 'plyta', 'data', 'ilosc', 'cena', 'cena_j', 'doc_id'
    ]
    ordering = ['data']


class RozchodAdmin(admin.ModelAdmin):
    list_display = [
        'plyta', 'cel', 'data', 'nr_sde', 'ilosc', 'kwota', 'doc_id'
    ]
    ordering = ['data']


class ZwrotAdmin(admin.ModelAdmin):
    list_display = [
        'plyta', 'cel', 'data', 'nr_sde', 'ilosc', 'kwota', 'doc_id'
    ]
    ordering = ['data']


class StanObecnyAdmin(admin.ModelAdmin):
    list_display = [
        'plyta', 'przychod', 'rozchod', 'p_ilosc', 'r_ilosc', 'stan', 'nadmiar', 'p_cena_j', 'wartosc'
    ]
    ordering = ['plyta']


admin.site.register(Plyta, PlytaAdmin)
admin.site.register(Przychod, PrzychodAdmin)
admin.site.register(Rozchod, RozchodAdmin)
admin.site.register(Zwrot, ZwrotAdmin)
admin.site.register(StanObecny, StanObecnyAdmin)

admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"
