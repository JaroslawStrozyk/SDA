from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Delegacja
from INVOICES.models import Osoba
import datetime
from TaskAPI.models import Asp
from TaskAPI.rap_temp import email_temp1, email_temp2
from django.conf import settings


def TempSkype(cel, adres, instance):
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


def TempEmail(cel, adres, instance):
    tytul = "Zgłoszenie delegacji od " + instance.imie + " " + instance.nazwisko

    info = email_temp1(tytul)
    info += "<tr><td width='150'><strong>Targi</strong></td><td width='10'>:</td><td>" + instance.targi + "</td></tr>" \
            + "<tr><td><strong>Data od</strong></td><td>:</td><td>" + str(instance.data_od) + "</td></tr>" \
            + "<tr><td><strong>Data do</strong></td><td>:</td><td>" + str(instance.data_do) + "</td></tr>" \
            + "<tr><td><strong>Kasa PLN</strong></td><td>:</td><td>" + str(instance.kasa_pln) + "</td></tr>" \
            + "<tr><td><strong>Kasa EURO</strong></td><td>:</td><td>" + str(instance.kasa_euro) + "</td></tr>" \
            + "<tr><td><strong>Kasa FUNT</strong></td><td>:</td><td>" + str(instance.kasa_funt) + "</td></tr>" \
            + "<tr><td><strong>KASA INNA</strong></td><td>:</td><td>" + str(instance.kasa_inna) + "</td></tr>" \
            + "<tr><td><strong>KASA KARTA</strong></td><td>:</td><td>" + str(instance.kasa_karta) + "</td></tr>"
    info += email_temp2()
    data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info += "<h4><font color='#000099'>" + "Zgłoszenie: " + data + "</font></h4>"

    asp = Asp.objects.create(cel=cel, adres=adres, tytul=tytul, info=info, data=data)
    asp.save()





@receiver([post_save], sender=Delegacja)
def Delegacja_save(sender, instance, **kwargs):
    cel = settings.DELEGATIONS_TO_TARGET

    if cel==1:
        for adres in settings.DEL_SKYPE_DO_USERS:
            TempSkype(cel, adres, instance)

    if cel==2:
        for adres in settings.DEL_EMAIL_DO_USERS:
            TempEmail(cel, adres, instance)


    con = 0
    if instance.confirm == 'SKYPE':
        con = 1
    if instance.confirm == 'E-MAIL':
        con = 2

    try:
        row = Osoba.objects.filter(naz_imie=instance.naz_imie).values_list('skype', 'email')
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
