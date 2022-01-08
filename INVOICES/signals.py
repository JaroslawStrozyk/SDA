from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Faktura, Osoba
from TaskAPI.models import Asp
from TaskAPI.rap_temp import email_temp1, email_temp2
from django.conf import settings

def TempSkype(cel, adres, instance):
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


def TempEmail(cel, adres, instance):
    tytul = "Zgłoszenie faktury od " + instance.imie + " " + instance.nazwisko

    info = email_temp1(tytul)
    info = info \
           + "<tr><td width='150'><strong>Targi</strong></td><td width='10'>:</td><td>" + instance.targi + "</td></tr>" \
           + "<tr><td><strong>Stoisko</strong></td><td>:</td><td>" + instance.stoisko + "</td></tr>" \
           + "<tr><td><strong>Rodzaj FV</strong></td><td>:</td><td>" + instance.rfaktura + "</td></tr>" \
           + "<tr><td><strong>Termin</strong></td><td>:</td><td>" + str(instance.termin) + "</td></tr>" \
           + "<tr><td><strong>Kwota</strong></td><td>:</td><td>" + str(instance.kwota) + "</td></tr>" \
           + "<tr><td><strong>Za co</strong></td><td>:</td><td>" + instance.zaco + "</td></tr>" \
           + "<tr><td><strong>Specyfikacja</strong></td><td>:</td><td>" + instance.spec + "</td></tr>" \
           + "<tr><td><strong>Uwagi</strong></td><td>:</td><td>" + instance.uwagi + "</td></tr>"
    info = info + email_temp2()
    data = str(instance.data)
    info = info + "<h4><font color='#000099'>" + "Zgłoszenie: " + data + "</font></h4>"

    asp = Asp.objects.create(cel=cel, adres=adres, tytul=tytul, info=info, data=data)
    asp.save()


@receiver([post_save], sender=Faktura)
def Faktura_save(sender, instance, **kwargs):

    if instance.zrobione == False:
        if instance.sig_source == False:

            cel = settings.INVOICES_TO_TARGET
            if cel==1:
                for adres in settings.INV_SKYPE_DO_USERS:
                    TempSkype(cel, adres, instance)

            if cel==2:
                for adres in settings.INV_EMAIL_DO_USERS:
                    TempEmail(cel, adres, instance)

            con = 0
            if instance.confirm == 'SKYPE':
                con = 1
            if instance.confirm == 'E-MAIL':
                con = 2

            try:
                row = Osoba.objects.filter(naz_imie=instance.naz_imie).values_list('skype','email')
                adres1 = str(row[0][0])
                adres2 = str(row[0][1])
            except:
                con = 0
                adres1 = ''
                adres2 = ''

            if con == 1:
                TempSkype(con, adres1, instance)

            if con == 2:
                TempEmail(con, adres2, instance)