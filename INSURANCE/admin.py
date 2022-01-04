from django.contrib import admin
from .models import Ubezpieczenie


class UbezpieczenieAdmin(admin.ModelAdmin):
    list_display = ['nazwa','dotyczy', 'opiekun', 'skn1', 'skn2', 'daod', 'dado', 'uwagi']
    ordering = ['nazwa']

admin.site.register(Ubezpieczenie, UbezpieczenieAdmin)

admin.site.site_header = "SDE SmartDesign"
admin.site.site_title = "SmartDesign"

