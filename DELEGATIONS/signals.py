from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Delegacja
import datetime
from TaskAPI.models import Asp
from django.conf import settings

@receiver([post_save], sender=Delegacja)
def Delegacja_save(sender, instance, **kwargs):
    cel = settings.DELEGATIONS_TO_TARGET

    if cel==1:
        for adres in settings.DEL_SKYPE_DO_USERS:
            tytul = "Zgłoszenie delegacji od " + instance.imie + " " + instance.nazwisko
            info = tytul + '\n\r' \
            + "TARGI:        " + instance.targi + "\n" \
            + "DATA OD:      " + str(instance.data_od) + "\n" \
            + "DATA DO:      " + str(instance.data_do) + "\n" \
            + "KASA PLN:     " + str(instance.kasa_pln) + "\n" \
            + "KASA EURO:    " + str(instance.kasa_euro) + "\n" \
            + "KASA FUNT:    " + str(instance.kasa_funt) + "\n" \
            + "KASA INNA:    " + str(instance.kasa_inna) + "\n" \
            + "KASA KARTA:   " + str(instance.kasa_karta) + "\n"
            data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info = info + "\n" + "ZGŁOSZENIE: " + data
            asp = Asp.objects.create(cel=cel, adres=adres, tytul=tytul, info=info, data=data)
            asp.save()

    if cel==2:
        for adres in settings.DEL_EMAIL_DO_USERS:
            tytul = "Zgłoszenie delegacji od " + instance.imie + " " + instance.nazwisko
            info = "<h2><font color='#009900'>" + tytul + "</font></h2><br>" \
            + "<table witdh='100%'>" \
            + "<tr><td align='right' width='150'><strong>TARGI:</strong></td><td width='10'></td><td colspan='2' align='left'>" + instance.targi + "</td></tr>" \
            + "<tr><td align='right'><strong>DATA OD:</strong></td><td width='10'></td><td width='100' align='left'>" + str(instance.data_od) + "</td><td></td></tr>" \
            + "<tr><td align='right'><strong>DATA DO:</strong></td><td width='10'></td><td align='left'>" + str(instance.data_do) + "</td><td></td></tr>" \
            + "<tr><td align='right'><strong>KASA PLN:</strong></td><td width='10'></td><td align='left'>" + str(instance.kasa_pln) + "</td><td></td></tr>" \
            + "<tr><td align='right'><strong>KASA EURO:</strong></td><td width='10'></td><td align='left'>" + str(instance.kasa_euro) + "</td><td></td></tr>" \
            + "<tr><td align='right'><strong>KASA FUNT:</strong></td><td width='10'></td><td align='left'>" + str(instance.kasa_funt) + "</td><td></td></tr>" \
            + "<tr><td align='right'><strong>KASA INNA:</strong></td><td width='10'></td><td align='left'>" + str(instance.kasa_inna) + "</td><td></td></tr>" \
            + "<tr><td align='right'><strong>KASA KARTA:</strong></td><td width='10'></td><td align='left'>" + str(instance.kasa_karta) + "</td><td></td></tr>" \
            + "</table>"
            data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info = info + "<h4><font color='#000099'>" + "ZGŁOSZENIE: " + data + "</font></h4>"
            asp = Asp.objects.create(cel=cel, adres=adres, tytul=tytul, info=info, data=data)
            asp.save()