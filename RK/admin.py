from django.contrib import admin
from .models import FirmaKasa, RaportKasowy, KwKp, Waluta

class WalutaAdmin(admin.ModelAdmin):
    list_display = ['tab', 'kod', 'poz', 'data', 'kurs', 'opis']


class FirmaKasaAdmin(admin.ModelAdmin):
    list_display = ['rodzaj','nazwa','adres','miasto','nip','kasa','konto','bo','stan','data_bo','uwagi']
    ordering = ['nazwa']

class RaportKasowyAdmin(admin.ModelAdmin):
    list_display = ['kasa','data','sum_przychod','sum_rozchod','stan_poprzedni','stan_obecny','kw','kp','mkw','mkp']
    ordering = ['data']


class KwKpAdmin(admin.ModelAdmin):
    list_display = ['kasa','rodzaj','numer','nazwa','adres','miasto','rozchod','przychod','data','opis','uwagi']
    ordering = ['data']

admin.site.register(Waluta, WalutaAdmin)
admin.site.register(FirmaKasa, FirmaKasaAdmin)
admin.site.register(RaportKasowy, RaportKasowyAdmin)
admin.site.register(KwKp, KwKpAdmin)

admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"
