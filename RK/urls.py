from django.urls import path
from . import views


urlpatterns = [
    path('', views.rk_start, name='rk_start'),
    path('new/', views.rk_new, name='rk_new'),
    path('edit/<pk>', views.rk_edit, name='rk_edit'),
    path('lrk/<idk>',views.lrk, name='lrk'),
    path('uplrk/<idk>',views.uplrk, name='uplrk'),
    path('updlrk/<idk>/<dd>/<mm>/<rrrr>',views.uplrk, name='updlrk'),
    path('lrk/<idk>/old/<mc>',views.lrk_old, name='lrk_old'),
    path('lrk/<idk>/arch/<idrk>',views.lrk_arch, name='arch'),
    path('lrk/<idk>/kwkp/', views.kwkp, name='kwkp'),
    path('lrk/<idk>/kwkp_new', views.kwkp_new, name='kwkp_new'),
    path('lrk/<idk>/kwkpedit/<pk>', views.kwkp_edit, name='kwkp_edit'),
    path('lrk/<idk>/kwkpcount/<mc>/<rok>', views.kwkp_count, name='kwkp_count'),
    path('lrk/<idk>/kwkppdf/<pk>', views.kwkppdf, name='kwkp_print'),
    path('lrk/<idk>/drkpdf/<dt>', views.drkpdf, name='drk_print'),
    path('lrk/<idk>/mrkpdf/<mc>', views.mrkpdf, name='mrk_print'),
    path('lrk/<idk>/smrkpdf/<mc>', views.smrkpdf, name='smrk_print'),
]