from django.contrib import admin
from .models import Firma, OkresPrzechowywania, ElementKatalogowy, HistoriaPalety, Sklad


def get_all_fields(model):
    return [field.name for field in model._meta.fields]


class FirmaAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Firma)
    ordering = ['nazwa']


class OkresPrzechowywaniaAdmin(admin.ModelAdmin):
    list_display = get_all_fields(OkresPrzechowywania)
    ordering = ['nazwa']


class ElementKatalogowyAdmin(admin.ModelAdmin):
    list_display = get_all_fields(ElementKatalogowy)
    ordering = ['nazwa']


class HistoriaPaletyAdmin(admin.ModelAdmin):
    list_display = get_all_fields(HistoriaPalety)
    ordering = ['sklad']


class SkladAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Sklad)
    ordering = ['firma']


admin.site.register(Firma, FirmaAdmin)
admin.site.register(OkresPrzechowywania, OkresPrzechowywaniaAdmin)
admin.site.register(ElementKatalogowy, ElementKatalogowyAdmin)
admin.site.register(HistoriaPalety, HistoriaPaletyAdmin)
admin.site.register(Sklad, SkladAdmin)


admin.site.site_header = "SDA SmartDesign"
admin.site.site_title = "SmartDesign"

