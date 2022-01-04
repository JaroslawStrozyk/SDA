from django.urls import path
from . import views

urlpatterns = [
    path('', views.ub_start, name='ub_start'),
    path('add/', views.ub_add, name='ub_add'),
    path('edit/<pk>', views.ub_edit, name='ub_edit'),
    #path('search/', views.faktura_search, name='faktura_search'),
]