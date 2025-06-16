from django.contrib import admin
from .models import Ubezpieczenie, Termin


class UbezpieczenieAdmin(admin.ModelAdmin):
    list_display = [
        'firma', 'nazwa', 'dotyczy', 'suma', 'skladka', 'doc1', 'doc2',
        'data_od', 'data_do', 'raty', 'data_raty', 'uwagi']
    ordering = ['nazwa']

class TerminAdmin(admin.ModelAdmin):
    list_display = [
        'firma', 'dotyczy', 'suma', 'skladka', 'doc1', 'doc2',
        'data_od', 'data_do', 'uwagi']
    ordering = ['firma']


admin.site.register(Ubezpieczenie, UbezpieczenieAdmin)
admin.site.register(Termin, TerminAdmin)

admin.site.site_header = "SDE SmartDesign"
admin.site.site_title = "SmartDesign"

