from django.urls import path
from . import views


urlpatterns = [
    path('',            views.auta,        name='auta_start'),
    path('arch/',       views.auta_arch,   name='auta_arch'),
    path('add/',        views.auto_add,    name='auto_add'),
    path('edit/<pk>',   views.auto_edit,   name='auto_edit'),
    path('delete/<pk>', views.auto_delete, name='auto_delete'),
    path('export/',     views.auto_export, name='auto_export'),
]