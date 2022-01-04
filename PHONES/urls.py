from django.urls import path
from . import views

urlpatterns = [
    path('', views.phone, name='phone_start'),
    path('phone_add/', views.phone_add, name='phone_add'),
    path('phone_edit/<pk>', views.phone_edit, name='phone_edit'),
    path('phone_addc/<pk>', views.phone_addc, name='phone_addc'),
    path('phone_pp/<pk>', views.phone_pp, name='phone_pp'),
    path('phone_pz/<pk>', views.phone_pz, name='phone_pz'),
    path('phone_arch/', views.phone_arch, name='phone_arch'),
    path('phone_mag/', views.phone_mag, name='phone_mag'),
    path('phone_delete/<pk>', views.phone_delete, name='phone_delete'),
    path('phone_export/', views.phone_export, name='phone_export'),
]
