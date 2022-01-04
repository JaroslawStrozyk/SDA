from django.urls import path
from . import views

urlpatterns = [
    path('', views.logs_start, name='logs_start'),
    path('p/', views.logs_startp, name='logs_startp'),
]