from django.contrib import admin
from . models import Auto


class AutoAdmin(admin.ModelAdmin):
    list_display = ['rodzaj','typ' ,'rej' , 'imie_n', 'opis', 'img1', 'img2', 'data',
                    'us', 'ps','stu','stp', 'uwagi', 'nul', 'drl', 'dzl', 'rul', 'arch',
                    'stdrl', 'stdzl', 'koniecl', 'sprzedany'
                    ]
    search_fields = ['typ', 'rej', 'imie', 'nazwisko']
    ordering = ['-data' ]

admin.site.register(Auto, AutoAdmin)
