from django.urls import path
from . import views


urlpatterns = [
    path('',                      views.ser_start,  name='ser_start'),
    path('ser_new_u/',            views.ser_new_u,  name='ser_new_u'),
    path('ser_edit_u/<pk>/',      views.ser_edit_u, name='ser_edit_usluga'),
    path('ser_new_p/<pk>/',       views.ser_new_p,  name='ser_new_profil'),
    path('ser_edit_p/<pk>/<lp>/', views.ser_edit_p, name='ser_edit_profil'),
    path('ser_search/',           views.ser_search, name='ser_search'),
    path('ser_detail/<pk>/',      views.ser_detail, name='ser_detail'),
    path('ser_delete/<pk>',       views.ser_delete, name='ser_delete'),
    path('pro_delete/<pk>/<ret>/',views.pro_delete, name='pro_delete'),
]