from django.contrib import admin
from .models import  Telefon

class TelefonAdmin(admin.ModelAdmin):
    list_display = [
        'usr', 'model', 'imei', 'sim', 'msisdn', 'kod', 'bkod', 'konto', 'haslo', 'data', 'uwagi', 'arch', 'pz',
        'doc', 'docz', 'zam', 'pesel', 'mag'
    ]
    search_fields = ['usr', 'model', 'imei', 'sim', 'msisdn']
    ordering = ['usr']

admin.site.register(Telefon, TelefonAdmin)

admin.site.site_header = "Tech SmartDesign"
admin.site.site_title = "SmartDesign"