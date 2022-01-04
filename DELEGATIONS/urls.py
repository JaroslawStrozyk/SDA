from django.urls import path
from . import views

urlpatterns = [
    path('', views.delegacja_lista, name='delegacja_lista'),
    path('add/', views.delegacja_add, name='delegacja_add'),
    path('edit/<pk>', views.delegacja_edit, name='delegacja_edit'),
    path('search/', views.delegacja_search, name='delegacja_search'),
]