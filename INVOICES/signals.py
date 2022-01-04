from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Faktura
from TaskAPI.models import Asp
from django.conf import settings

@receiver([post_save], sender=Faktura)
def Faktura_save(sender, instance, **kwargs):

    if instance.zrobione == False:
        if instance.sig_source == False:

            cel = settings.INVOICES_TO_TARGET
            if cel==1:
                for adres in settings.INV_SKYPE_DO_USERS:
                    tytul = "Zgłoszenie faktury od " + instance.imie + " " + instance.nazwisko
                    info = tytul + '\n\r' \
                    + "TARGI ________: " + instance.targi + "\n" \
                    + "STOISKO ______: " + instance.stoisko + "\n" \
                    + "RODZAJ FV ____: " + instance.rfaktura + "\n" \
                    + "TERMIN _______: " + str(instance.termin) + "\n" \
                    + "KWOTA ________: " + str(instance.kwota) + "\n" \
                    + "ZA CO ________: " + instance.zaco + "\n" \
                    + "SPECYFIKACJA _: " + instance.spec + "\n"
                    info = info + "\n" + "ZGŁOSZENIE: " + str(instance.data)
                    asp = Asp.objects.create(cel=cel, adres=adres, tytul=tytul, info=info, data=instance.data)
                    asp.save()

            if cel==2:
                for adres in settings.INV_EMAIL_DO_USERS:
                    tytul = "Zgłoszenie faktury od " + instance.imie + " " + instance.nazwisko
                    info = "<h2><font color='#009900'>" + tytul + "</font></h2><br>" \
                    + "<table witdh='100%'>" \
                    + "<tr><td align='right' width='150'><strong>TARGI:</strong></td><td width='10'></td><td colspan='2' align='left'>" + instance.targi + "</td></tr>" \
                    + "<tr><td align='right'><strong>STOISKO:</strong></td><td width='10'></td><td width='100' align='left'>" + instance.stoisko + "</td><td></td></tr>" \
                    + "<tr><td align='right'><strong>RODZAJ FV:</strong></td><td width='10'></td><td align='left'>" + instance.rfaktura + "</td><td></td></tr>" \
                    + "<tr><td align='right'><strong>TERMIN:</strong></td><td width='10'></td><td align='left'>" + str(instance.termin) + "</td><td></td></tr>" \
                    + "<tr><td align='right'><strong>KWOTA:</strong></td><td width='10'></td><td align='left'>" + str(instance.kwota) + "</td><td></td></tr>" \
                    + "<tr><td align='right'><strong>ZA CO:</strong></td><td width='10'></td><td align='left'>" + instance.zaco + "</td><td></td></tr>" \
                    + "<tr><td align='right'><strong>SPECYFIKACJA:</strong></td><td width='10'></td><td align='left'>" + instance.spec + "</td><td></td></tr>" \
                    + "</table>"
                    data = str(instance.data)
                    info = info + "<h4><font color='#000099'>" + "ZGŁOSZENIE: " + data + "</font></h4>"
                    asp = Asp.objects.create(cel=cel, adres=adres, tytul=tytul, info=info, data=data)
                    asp.save()