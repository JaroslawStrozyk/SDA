from django.urls import path
from . import views

urlpatterns = [
    path('',            views.LanView,   name='lan_start'),
    path('create/',     views.LanAdd,    name='lan_create'),
    path('read/',       views.LanRead,   name='lan_read'),
    path('edit/<id>',   views.LanEdit,   name='lan_edit'),
    path('edit/update/<id>', views.LanUpdate, name='lan_update'),
    path('delete/<id>',  views.LanDelete, name='lan_delete'),
]