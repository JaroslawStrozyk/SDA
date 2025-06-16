from django.urls import path
from . import views

urlpatterns = [
    path('<mag>/n/', views.comp_list, name='comp_list'),
    path('detail/<mag>/<pk>/<st>/n/', views.comp_detail, name='comp_detail'),
    path('ewu/<mag>/<fl>/n/', views.comp_multi, name='comp_multi'),

    path('ewu/<mag>/<fl>/firma/', views.firma_list, name='firma-strona'),

    path('add/<mag>/n/', views.comp_add, name='comp_add'),
    path('edit/<pk>/<mag>/<det>/n/', views.comp_edit, name='comp_edit'),
    path('del/<pk>/<mag>/n/', views.comp_delete, name='comp_delete'),

    path('ewu/edit/<pk>/<mag>/<fl>/n/', views.comp_medit, name='comp_medit'),

    path('pdf_sim/<pk>/<mag>/n/', views.comp_pdf_sim, name='comp_pdf_sim'),


    #path('<mag>/', views.sklad_list, name='sklad_list'),
    #path('detail/<mag>/<pk>/<st>/', views.sklad_detail, name='sklad_detail'),
    path('detail_up/<mag>/<pk>/<st>/', views.sklad_detail_up, name='sklad_detail_up'),
    #path('ewu/<mag>/<fl>/', views.sklad_multi, name='sklad_multi'),

    path('ewu/<mag>/<fl>/firmy/', views.firma_list_create, name='firma-list-create'),
    path('ewu/<mag>/<fl>/firmy/<int:pk>/', views.firma_detail, name='firma-detail'),
    path('ewu/get_multi_usage_details/', views.get_multi_usage_details, name='get_multi_usage_details'),
    path('ewu/edit/<pk>/<mag>/<fl>/', views.sklad_medit, name='sklad_medit'),
    path('add/<mag>/', views.sklad_add, name='sklad_add'),
    path('edit/<pk>/<mag>/<det>/', views.sklad_edit, name='sklad_edit'),
    path('pdf/<pk>/<mag>/', views.sklad_pdf, name='sklad_pdf'),
    path('pdf_bc/<pk>/<mag>/', views.sklad_pdf_bc, name='sklad_pdf_bc'),
    path('pdf_sim/<pk>/<mag>/', views.sklad_pdf_sim, name='sklad_pdf_sim'),
    path('pdf_dok/<fl>/<sde>/', views.sklad_pdf_dok, name='sklad_pdf_dok'),
    path('pdf_ewu/<pk>/<mag>/', views.ewu_pdf_bc, name='ewu_pdf_bc'),
    path('del/<pk>/<mag>/', views.sklad_delete, name='sklad_delete'),
    path('ewu_del/<pk>/<fl>/<mag>/', views.ewu_delete, name='ewu_delete'),
]