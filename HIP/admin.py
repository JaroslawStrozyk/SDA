from django.contrib import admin
from .models import Sprzet, Profil, System

class SystemAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'uwagi']
    ordering = ['nazwa']


class SprzetAdmin(admin.ModelAdmin):
    list_display = ['system', 'nazwa_siec', 'kik', 'host', 'usr', 'typ','adres_ip','domena','sw_gn', 'snk', 'uwagi' ,'zdj', 'arch', 'gw', 'doc', 'docz', 'zam', 'pesel', 'pr', 'pz','mag', 'stan', 'opis', 'historia', 'wartosc', 'sprzedany']
    search_fields = ['nazwa_siec', 'kik', 'host', 'adres_ip']
    ordering = ['usr',]

class ProfilAdmin(admin.ModelAdmin):
    list_display = ['sprzet', 'rodzaj_konta', 'kod', 'konto', 'haslo', 'adres', 'uwagi', 'fv', 'data_waznosci', 'termin', 'auto_platnosc', 'karta']
    search_fields = ['rodzaj_konta', 'kod', 'konto']
    ordering = ['-sprzet' ]


admin.site.register(System, SystemAdmin)
admin.site.register(Sprzet, SprzetAdmin)
admin.site.register(Profil, ProfilAdmin)


admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"