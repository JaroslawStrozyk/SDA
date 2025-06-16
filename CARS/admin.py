from django.contrib import admin
from . models import Auto


class AutoAdmin(admin.ModelAdmin):
    list_display = ['rodzaj','typ' ,'rej' , 'imie_n', 'opis', 'img1', 'img2', 'data', 'pt',
                    'us', 'ps','stu','stp', 'spt', 'uwagi', 'nul', 'drl', 'dzl', 'rul', 'arch',
                    'stdrl', 'stdzl', 'koniecl', 'sprzedany', 'deleg_auto'
                    ]
    search_fields = ['typ', 'rej', 'imie', 'nazwisko']
    ordering = ['-data' ]

admin.site.register(Auto, AutoAdmin)
