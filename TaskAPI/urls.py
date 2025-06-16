from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .views import CustomLogoutView


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='SDA/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='SDA/logout.html'), name='logout'),
    # path('doc/', views.doc_view, name='doc_view'),
    path('doc/', views.katalogi_view, name='doc_view'),
    path('doc/<int:katalog_id>/', views.pliki_view, name='pliki'),
    path('doc/pdf/<int:id>/', views.pliki_pdf, name='pliki_pdf'),
    path('task/', views.task, name='desktop'),
    path('task/ref/', views.refresh, name='refresh'),
    path('error/', views.error, name='error'),
    path('log/', views.log, name='log'),
]
