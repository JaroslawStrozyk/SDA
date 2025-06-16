from django.contrib import admin
from .models import Lan


class LanAdmin(admin.ModelAdmin):
    list_display = ['ip', 'nazwa', 'typ', 'opis', 'uwagi']
    ordering = ['ip']

admin.site.register(Lan, LanAdmin)


admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"