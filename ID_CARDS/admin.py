from django.contrib import admin
from . models import Dowod


class DowodAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'img1', 'img2', 'data', 'uwagi']
    search_fields = ['imie', 'nazwisko']
    ordering = ['-data' ]

admin.site.register(Dowod, DowodAdmin)

