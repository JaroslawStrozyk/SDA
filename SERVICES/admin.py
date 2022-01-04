from django.contrib import admin
from .models import Usluga, Profil


class UslugaAdmin(admin.ModelAdmin):
    list_display = ['nazwa_siec', 'usr', 'dostawca', 'hosting', 'uwagi', 'zdj', 'data_waznosci', 'termin']
    search_fields = ['nazwa_siec', 'usr', 'dostawca', 'hosting']
    ordering = ['nazwa_siec',]

class ProfilAdmin(admin.ModelAdmin):
    list_display = ['usluga', 'rodzaj_konta', 'konto', 'haslo', 'adres', 'uwagi']
    search_fields = ['rodzaj_konta',  'konto']
    ordering = ['-usluga' ]


admin.site.register(Usluga, UslugaAdmin)
admin.site.register(Profil, ProfilAdmin)


admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"
