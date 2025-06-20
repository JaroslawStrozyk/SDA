from django.contrib import admin
from . models import Asp, Waluta, Rok, URok, Ustawienia, Katalog, Plik


class AspKatalog(admin.ModelAdmin):
    list_display = ['nazwa', 'opis']
    search_fields = ['nazwa', 'opis']
    ordering = ['nazwa']


class AspPlik(admin.ModelAdmin):
    list_display = ['nazwa', 'katalog', 'dokument', 'form']
    search_fields = ['nazwa']
    ordering = ['nazwa']


class AspAdmin(admin.ModelAdmin):
    list_display = ['cel', 'adres', 'tytul', 'info', 'data']
    search_fields = ['adres',]
    ordering = ['-data' ]


class WalutaAdmin(admin.ModelAdmin):
    list_display = ['tab', 'kod', 'data', 'kurs']
    ordering = ['data']


# class LogAdmin(admin.ModelAdmin):
#     list_display = ['data', 'modul', 'usr', 'uwagi']
#     ordering = ['-data']

class RokAdmin(admin.ModelAdmin):
    list_display = ['rok', 'flg']
    ordering = ['rok']

class URokAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'rok']
    ordering = ['nazwa']

class UstawieniaAdmin(admin.ModelAdmin):
    list_display = ['co', 'medium', 'email', 'skype', 'dshift', 'tshift']
    ordering = ['co']


admin.site.register(Katalog, AspKatalog)
admin.site.register(Plik, AspPlik)

admin.site.register(Asp, AspAdmin)
admin.site.register(Waluta, WalutaAdmin)
# admin.site.register(Log, LogAdmin)
admin.site.register(Rok, RokAdmin)
admin.site.register(URok, URokAdmin)
admin.site.register(Ustawienia, UstawieniaAdmin)

admin.site.site_header = "Tech SmartDesign"
admin.site.site_title = "SmartDesign"
