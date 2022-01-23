"""
    SDA URL Główny program
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
                  path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
                  path('', include('TaskAPI.urls')),
                  path('HIP/', include('HIP.urls')),
                  path('TELEFONY/', include('PHONES.urls')),
                  path('DOWODY/', include('ID_CARDS.urls')),
                  path('AUTA/', include('CARS.urls')),
                  path('USLUGI/', include('SERVICES.urls')),
                  path('DELEGACJE/', include('DELEGATIONS.urls')),
                  path('RK/', include('RK.urls')),
                  path('FAKTURY/', include('INVOICES.urls')),
                  path('UBEZPIECZENIA/', include('INSURANCE.urls')),
                  path('ZAMOWIENIA/', include('ORDERS.urls')),
                  path('ZALICZKA/', include('CASH_ADVANCES.urls')),
                  path('GDOCS/', include('GOOGLE.urls')),
                  path('MONIT/', include('MONIT.urls')),
                  path('LOG/', include('LOG.urls')),
                  path('PRACOWNIK/', include('WORKER.urls')),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
    Pamiętać o wyłaczeniu tej opcji po skończonej robocie - bezpieczeństwo
"""
