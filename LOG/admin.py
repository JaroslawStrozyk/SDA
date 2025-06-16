from django.contrib import admin
from .models import LogSystem, ErrorList, ModulName

class LogSystemAdmin(admin.ModelAdmin):
    list_display = ['data', 'godz', 'modul_id',  'komunikat_id', 'opis']
    ordering = ['-data']

class ModulNameAdmin(admin.ModelAdmin):
    list_display = ['id','nazwa']

class ErrorListAdmin(admin.ModelAdmin):
    list_display = ['id','nazwa', 'status_id', 'status']

admin.site.register(LogSystem, LogSystemAdmin)
admin.site.register(ModulName, ModulNameAdmin)
admin.site.register(ErrorList, ErrorListAdmin)

admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"

