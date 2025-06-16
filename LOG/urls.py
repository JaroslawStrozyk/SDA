from django.urls import path
from . import views

urlpatterns = [
    path('', views.log, name='log'),
    path('arch/', views.log_arch, name='log_arch'),
    path('get_logs/', views.get_logs, name='get_logs'),
    path('a/', views.log_all, name='log_all'),
    path('a_search/', views.log_search, name='log_search'),
    path('t/', views.log_tech, name='log_tech'),
    path('o/', views.log_oper, name='log_oper'),
    path('gen/', views.log_create, name="gen_logs"),
    path('list_logs/', views.list_logs, name='list_logs'),
    path('get_log_content/', views.get_log_content, name='get_log_content'),
]
