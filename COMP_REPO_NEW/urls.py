from django.urls import path
from . import views

urlpatterns = [
    path('<mag>/n/', views.ncomp_list, name='ncomp_list'),
    path('detail/<mag>/<pk>/<st>/n/', views.ncomp_detail, name='ncomp_detail'),
    path('add/<mag>/n/', views.ncomp_add, name='ncomp_add'),
    path('add_d/<mag>/<pk>/<id>/n/', views.ncomp_add_d, name='ncomp_add_d'),
    path('edit/<pk>/<mag>/<det>/n/', views.ncomp_edit, name='ncomp_edit'),
    path('dedit/<mag>/<det>/n/', views.ncomp_doc_edit, name='ncomp_doc_edit'),
    path('del/<pk>/<mag>/<det>/n/', views.ncomp_delete, name='ncomp_delete'),
    path('get_filtered_data/', views.get_filtered_data, name='get_filtered_data'),
    path('pdf/<pk>/<mag>/', views.sklad_pdf, name='sklad_pdf'),
    path('pdf_bc/<pk>/<mag>/', views.sklad_pdf_bc, name='sklad_pdf_bc'),
    path('pdf_sim/<pk>/<mag>/n/', views.comp_pdf_sim, name='comp_pdf_sim'),

    path('firmy/<mag>/<fl>/firma/', views.nfirma_list, name='nfirma_strona'),
    path('firmy/<mag>/<fl>/firmy/', views.nfirma_list_create, name='nfirma_list_create'),
    path('firmy/<mag>/<fl>/firmy/<int:pk>/', views.nfirma_detail, name='nfirma_detail'),

    path('kat_el/<mag>/<st>/n/<zm>/', views.nkat_lista, name='nkat_el'),
    path('kat_add/<mag>/<st>/n/<zm>/', views.nkat_add, name='nkat_add'),
    path('kat_edit/<mag>/<pk>/<st>/n/<zm>/', views.nkat_edit, name='nkat_edit'),
    path('kat_del/<mag>/<pk>/<st>/n/<zm>/', views.nkat_delete, name='nkat_delete'),
    path('kat_pdf/<mag>/<pk>/', views.nkat_pdf, name='nkat_pdf'),

    path('okr/<mag>/<fl>/n/<zm>/', views.nokr_lista, name='nokr_lista'),
    path('okr/add/<mag>/<fl>/n/<zm>/', views.nokr_add, name='nokr_add'),
    path('okr/edit/<mag>/<fl>/<pk>/n/<zm>/', views.nokr_edit, name='nokr_edit'),
    path('okr/del/<mag>/<fl>/<pk>/n/<zm>/', views.nokr_delete, name='nokr_delete'),
    path('okr/sklad-by-okres/', views.get_sklad_by_okres, name='get_sklad_by_okres'),







    # path('ewu/<mag>/<fl>/n/', views.comp_multi, name='comp_multi'),


    #
    # path('ewu/edit/<pk>/<mag>/<fl>/n/', views.comp_medit, name='comp_medit'),
    #
    # path('pdf_sim/<pk>/<mag>/n/', views.comp_pdf_sim, name='comp_pdf_sim'),
    #
    #
    # #path('<mag>/', views.sklad_list, name='sklad_list'),
    # #path('detail/<mag>/<pk>/<st>/', views.sklad_detail, name='sklad_detail'),
    # path('detail_up/<mag>/<pk>/<st>/', views.sklad_detail_up, name='sklad_detail_up'),
    # #path('ewu/<mag>/<fl>/', views.sklad_multi, name='sklad_multi'),
    #
    # path('ewu/<mag>/<fl>/firmy/', views.firma_list_create, name='firma-list-create'),
    # path('ewu/<mag>/<fl>/firmy/<int:pk>/', views.firma_detail, name='firma-detail'),
    # path('ewu/get_multi_usage_details/', views.get_multi_usage_details, name='get_multi_usage_details'),
    # path('ewu/edit/<pk>/<mag>/<fl>/', views.sklad_medit, name='sklad_medit'),
    # path('add/<mag>/', views.sklad_add, name='sklad_add'),
    # path('edit/<pk>/<mag>/<det>/', views.sklad_edit, name='sklad_edit'),
    # path('pdf/<pk>/<mag>/', views.sklad_pdf, name='sklad_pdf'),
    # path('pdf_bc/<pk>/<mag>/', views.sklad_pdf_bc, name='sklad_pdf_bc'),
    # path('pdf_sim/<pk>/<mag>/', views.sklad_pdf_sim, name='sklad_pdf_sim'),
    # path('pdf_dok/<fl>/<sde>/', views.sklad_pdf_dok, name='sklad_pdf_dok'),
    # path('pdf_ewu/<pk>/<mag>/', views.ewu_pdf_bc, name='ewu_pdf_bc'),
    # path('del/<pk>/<mag>/', views.sklad_delete, name='sklad_delete'),
    # path('ewu_del/<pk>/<fl>/<mag>/', views.ewu_delete, name='ewu_delete'),
]