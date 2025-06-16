from django.urls import path
from . import views


urlpatterns = [
    path('',                        views.worker_start,           name='worker_start'),  # !
    path('PR/',                     views.worker_pr,              name='worker_pr'),     # !
    path('PR/add/',                 views.worker_pr_add,          name='worker_pr_add'),  # !
    path('PR/edit/<pk>/',           views.worker_pr_edit,         name='worker_pr_edit'),  # !
    path('PR/del/<pk>/',            views.worker_pr_del,          name='worker_pr_del'),   # ???
    path('PR/update/<mc>/',         views.worker_pr_update,       name='worker_pr_update'),  # !
    path('PR/update_prev',          views.worker_pr_update_prev,  name='worker_pr_update_prev'),  # !
    path('MC/',                     views.worker_mc,              name='worker_mc'),
    path('MCZ/',                    views.worker_mc_zest,         name='worker_mc_zest'),
    path('MC/EDIT/<pk>/<mc>/<rk>/', views.worker_mc_edit,         name='worker_mc_edit'),  # !
    path('MC/OEDIT/<mc>/<rk>/',     views.worker_mc_oedit,        name='worker_mc_oedit'),
    path('MC/FU/<pk>/<col>/<brk>/<bmc>/', views.worker_flag,      name='worker_flag'),
    path('AR/<rk>/<mc>/',           views.worker_mc_arch,         name='worker_mc_arch'),  # !
    path('GEN_MC/<bmc>/<brok>/',    views.gen_mc,                 name='worker_gen_mc'), # !
    path('GEN_ST/',                 views.gen_staz,               name='worker_gen_staz'),
    #path('GEN/',                    views.upgrade_pensja,         name='generator'),
    path('RMCL/<b_mc>/<b_rk>/<fl>/', views.red_worker_mc,          name='red_worker_mc'),
    path('RMC/DET/<pk>/<fl>/',      views.red_worker_mc_detail,   name='red_worker_mc_detail'),
    path('RMC/DET/BLOK/<fl>/<mc>/<rk>/<fn>/',      views.red_worker_mc_blok,   name='red_worker_mc_blok'),
    path('RMC/PDF/<b_mc>/<b_rk>/<pk>/<fl>/',      views.red_worker_mc_pdf,      name='red_worker_mc_pdf'),
    path('RMC/ADD/<wo>/<fl>/',      views.red_worker_mc_add,      name='red_worker_mc_add'),
    path('RMC/EDIT/<wo>/<pk>/<fl>/',views.red_worker_mc_edit,     name='red_worker_mc_edit'),
    path('RMC/DEL/<wo>/<pk>/<fl>/', views.red_worker_mc_delete,   name='red_worker_mc_delete'),
    path('RMC/RED/<wo>/<fl>/',      views.red_worker_mc_redirect, name='red_worker_mc_redirect')
]