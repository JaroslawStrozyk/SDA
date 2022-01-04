from django.urls import path
from . import views


urlpatterns = [
    path('',                      views.order_start,        name='order_start'),
    path('ord_all/',              views.order_start_all,    name='order_start_all'),
    path('ord_new/',              views.order_new,          name='ord_new'),
    path('ord_edit/<pk>/<src>/<fl>/',   views.order_edit,         name='ord_edit'),
    path('ord_search_er/',        views.order_search_er,    name='ord_search_er'),
    path('ord_search_pro/',        views.ord_search_pro,    name='ord_search_pro'),
    path('ord_search/<src>/',      views.order_search,       name='ord_search'),
    path('ord_search_sde/<src>/',  views.order_search_sde,   name='ord_search_sde'),
    path('ord_search_mpk/<src>/',  views.order_search_mpk,   name='ord_search_mpk'),
    path('ord_delete/<pk>/',       views.order_delete,       name='ord_delete'),
    path('ord_exp_xls/<rok>',     views.order_export_xls,   name='ord_export_xls'),
    path('ord_rok_akt/<pk>',      views.order_rok_akt,      name='ord_rok_akt'),
    path('sde_rok_akt/<pk>',      views.sde_rok_akt,        name='sde_rok_akt'),
    path('sde_main/',             views.sde_start,          name='sde_start'),
    path('sde_new/',              views.sde_new,            name='sde_new'),
    path('sde_edit/<pk>/',        views.sde_edit,           name='sde_edit'),
    path('sde_delete/<pk>',       views.sde_delete,         name='sde_delete'),
    path('sde_search/',           views.sde_search,         name='ord_sde_search'),
    path('sde_pdf/<kl>',          views.sde_pdf,            name='ord_sde_pdf'),
    path('ord_pdf/<src>/<fl>/',   views.ord_pdf,            name='ord_pdf'),
]