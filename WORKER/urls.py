from django.urls import path
from . import views


urlpatterns = [
    path('',                      views.worker_start,        name='worker_start'),
    path('PR/',                   views.worker_pr,           name='worker_pr'),
    path('PR/add',                views.worker_pr_add,       name='worker_pr_add'),
    path('PR/edit/<pk>',          views.worker_pr_edit,      name='worker_pr_edit'),
    path('PR/del/<pk>',           views.worker_pr_del,       name='worker_pr_del'),
    path('MC/',                   views.worker_mc,           name='worker_mc'),
    path('MC/calc/<mc>/<rk>/<ba>', views.worker_mc_calc,     name='worker_mc_calc'),
    path('MC/EDIT/<pk>',          views.worker_mc_edit,      name='worker_mc_edit'),
    path('MC/FU/<pk>/<col>',      views.worker_flag,         name='worker_flag'),
    path('MC/FA/<pk>/<col>',      views.worker_flag_arch,    name='worker_flag_arch'),
    path('AR/',                   views.worker_mc_arch,      name='worker_mc_arch'),
    path('AR/EDIT/<pk>',          views.worker_amc_edit,     name='worker_amc_edit'),
    path('AR/upload/',            views.file_upload_view,    name='upload-view'),
    path('GEN_MC/<bmc>/<brok>',   views.gen_mc,              name='worker_gen_mc'),
    path('GEN_ST/',               views.gen_staz,            name='worker_gen_staz'),
]