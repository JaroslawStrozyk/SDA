from django.urls import path
from . import views

urlpatterns = [
    path('', views.faktura_start, name='faktura_start'),
    path('add/', views.faktura_add, name='faktura_add'),
    path('edit/<pk>', views.faktura_edit, name='faktura_edit'),
    path('search/', views.faktura_search, name='faktura_search'),
]
