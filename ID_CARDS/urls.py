from django.urls import path
from . import views


urlpatterns = [
    path('', views.dowod_start, name='dowod_start'),
    path('search/', views.dowod_search, name='dowod_search'),
]