from django.urls import path
from . import views

urlpatterns = [
    path('', views.gog_start, name='gog_start'),
    path('KP/', views.gog_kp, name='gog_kp'),
    #path('KBP/', views.gog_kbp, name='gog_kbp'),
    #path('KG/', views.gog_kg, name='gog_kg'),
    #path('KGP/', views.gog_kgp, name='gog_kgp'),
    path('KS/', views.gog_ks, name='gog_ks'),
    #path('KSP/', views.gog_ksp, name='gog_ksp'),
]
