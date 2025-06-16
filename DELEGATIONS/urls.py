from django.urls import path
from . import views

urlpatterns = [
    path('', views.delegacja_lista, name='delegacja_lista'),
    path('add/<fl>/', views.delegacja_add, name='delegacja_add'),
    path('edit/<pk>/', views.delegacja_edit, name='delegacja_edit'),
    path('del/<pk>/', views.delegacja_delete, name='delegacja_delete'),
    path('diet/', views.delegacja_dieta, name='delegacja_dieta'),
    path('diet_edit/<pk>/', views.delegacja_dieta_edit, name="delegacja_dieta_edit"),
    path('redit/<pk>/', views.rdelegacja_edit, name='rdelegacja_edit'),
    path('pw/<pk>/', views.delegacja_pw, name='delegacja_pw'),
    path('rz/<pk>/', views.delegacja_rz, name='delegacja_rz'),
    path('rz_out/<pk>/', views.delegacja_rz_out, name='delegacja_rz_out'),
    path('rz_out_z/<pk>/', views.delegacja_rz_out_z, name='delegacja_rz_out_z'),
    path('search/', views.delegacja_search, name='delegacja_search'),
    path('radd/<pk>/<wal>/', views.rdelegacja_add_poz, name='rdelegacja_add_poz'),
    path('redit/<pk>/<po>/<wal>/', views.rdelegacja_edit_poz, name='rdelegacja_edit_poz'),
    path('rdel/<pk>/<po>/<wal>/', views.rdelegacja_delete_poz, name='rdelegacja_del_poz'),
    path('rlist/<pk>/<wal>/', views.rdelegacja_list_poz, name='rdelegacja_list_poz'),
]