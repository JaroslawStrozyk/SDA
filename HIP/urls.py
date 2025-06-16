from django.urls import path
from . import views


urlpatterns = [
    path('',                      views.hip_start,  name='hip_start'),
    path('hip_new_s/',            views.hip_new_s,  name='hip_new_sprzet'),
    path('hip_edit_s/<pk>/',      views.hip_edit_s, name='hip_edit_sprzet'),
    path('hip_delete_s/<pk>/',    views.hip_delete_s, name='hip_delete_sprzet'),
    path('hip_edit_m/<pk>/',      views.hip_edit_m, name='hip_edit_mag'),
    path('hip_pdf_pp/<pk>',       views.hip_pdf_pp, name='hip_sprzet_pp'),
    path('hip_pdf_pz/<pk>',       views.hip_pdf_pz, name='hip_sprzet_pz'),
    path('hip_arch/',             views.hip_arch,   name='hip_arch'),
    path('hip_mag/',              views.hip_mag,    name='hip_mag'),
    path('hip_new_p/<pk>/',       views.hip_new_p,  name='hip_new_profil'),
    path('hip_edit_p/<pk>/<lp>/', views.hip_edit_p, name='hip_edit_profil'),
    path('hip_delete_p/<pk>/<ret>/', views.hip_delete_p, name='hip_delete_profil'),
    path('hip_search/',           views.hip_search, name='hip_search'),
    path('hip_lista/<pk>/',       views.hip_lista,  name='hip_lista'),
    path('hip_konta/<pk>/',       views.hip_konta,  name='hip_konta'),
    path('hip_detail/<pk>/',      views.hip_detail, name='hip_detail'),
    path('<pk>/',                 views.hip_filtr,  name='hip_filtr'),
    path('sp/<pk>/',              views.hip_filtr_s,  name='hip_filtr_s'),
    path('serwis/<pk>/',          views.hip_serwis, name='hip_serwis'),
    path('hip_new_ser/<pk>/',     views.hip_new_ser, name='hip_new_serwis'),
    path('hip_edit_ser/<pk>/<lp>/', views.hip_edit_ser, name='hip_edit_serwis'),
]