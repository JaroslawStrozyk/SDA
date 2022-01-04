from django.urls import path
from . import views


urlpatterns = [
    path('',                       views.cash_start_p,    name='cash_start_p'),
    path('pw/',                    views.cash_start_pw,   name='cash_start_pw'),
    path('cash_new_p/',            views.cash_new_p,      name='cash_new_p'),
    path('cash_edit_p/<pk>/',      views.cash_edit_p,     name='cash_edit_p'),
    path('cash_search_p/',         views.cash_search_p,   name='cash_search_p'),
    path('cash_delete_p/<pk>',     views.cash_delete_p,   name='cash_delete_p'),
    path('r/',                     views.cash_start_r,    name='cash_start_r'),
    path('rw/',                    views.cash_start_rw,   name='cash_start_rw'),
    path('cash_new_r/',            views.cash_new_r,      name='cash_new_r'),
    path('cash_edit_r/<pk>/',      views.cash_edit_r,     name='cash_edit_r'),
    path('cash_search_r/',         views.cash_search_r,   name='cash_search_r'),
    path('cash_delete_r/<pk>',     views.cash_delete_r,   name='cash_delete_r'),
    path('cash_pdf_roz/<pk>',      views.cash_pdf_roz,    name='cash_pdf_roz'),
    path('cash_rok_akt1/<pk>',     views.cash_rok_akt1,   name='cash_rok_akt1'),
    path('cash_rok_akt2/<pk>',     views.cash_rok_akt2,   name='cash_rok_akt2'),
]
