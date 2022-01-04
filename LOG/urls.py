from django.urls import path
from . import views

urlpatterns = [
    path('a/', views.log_all, name='log_all'),
    path('a_search/', views.log_search, name='log_search'),
    path('t/', views.log_tech, name='log_tech'),
    path('o/', views.log_oper, name='log_oper'),
]
