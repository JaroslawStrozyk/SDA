from django.contrib import admin
from .models import Faktura


class FakturaAdmin(admin.ModelAdmin):
    list_display = ['data','imie','nazwisko','rfaktura','termin','targi','stoisko','kwota','zaco','spec','uwagi','zrobione']
    ordering = ['-data']


admin.site.register(Faktura, FakturaAdmin)

admin.site.site_header = "Tech SmartDesign"
admin.site.site_title = "SmartDesign"

