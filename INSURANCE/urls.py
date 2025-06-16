from django.urls import path
from . import views

urlpatterns = [
    path('', views.ub_start, name='ub_start'),
    path('add/', views.ub_add, name='ub_add'),
    path('edit/<pk>', views.ub_edit, name='ub_edit'),
    path('delete/<pk>', views.ub_delete, name='ub_delete'),
    path('t_add/', views.ubt_add, name='ubt_add'),
    path('t_edit/<pk>', views.ubt_edit, name='ubt_edit'),
    path('t_delete/<pk>', views.ubt_delete, name='ubt_delete'),
]