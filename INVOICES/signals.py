from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Faktura, Osoba
from TaskAPI.models import Asp
from TaskAPI.rap_temp import email_temp1, email_temp2, faktura_body
from django.conf import settings
from SDA.settings import INFO_PROGRAM

def TempSkype(cel, adres, instance):
    tytul = "Zgłoszenie faktury od " + instance.osoba.naz_imie
    # info = tytul + '\n\r' \
    #        + "TARGI ________: " + instance.targi + "\n" \
    #        + "STOISKO ______: " + instance.stoisko + "\n" \
    #        + "RODZAJ FV ____: " + instance.rfaktura + "\n" \
    #        + "TERMIN _______: " + str(instance.termin) + "\n" \
    #        + "KWOTA ________: " + str(instance.kwota) + "\n" \
    #        + "ZA CO ________: " + instance.zaco + "\n" \
    #        + "SPECYFIKACJA _: " + instance.spec + "\n"
    # info = info + "\n" + "ZGŁOSZENIE: " + str(instance.data)

    info = tytul + '\n\r' \
           + "\u2007\u2007\u2007\u2007\u2007\u2007\u2008TARGI:\u2003\u2007" + instance.targi + "\n" \
           + "\u2007\u2007\u2007\u2007\u2008STOISKO:\u2003\u2007" + instance.stoisko + "\n" \
           + "\u2007\u2007RODZAJ\u2007FV:\u2003\u2007" + instance.rfaktura + "\n" \
           + "\u2007\u2007\u2007\u2007\u2007TERMIN:\u2003\u2007" + str(instance.termin) + "\n" \
           + "\u2007\u2007\u2007\u2007\u2007\u2008KWOTA:\u2003\u2007" + str(instance.kwota) + "\n" \
           + "\u2007\u2007\u2007\u2007\u2007\u2007ZA\u2007CO:\u2003\u2007" + instance.zaco + "\n" \
           + "SPECYFIKACJA:\u2003\u2007" + instance.spec + "\n"
    formatted_time = instance.data.strftime('%Y-%m-%d %H:%M:%S')
    info = info + "\n" + "ZGŁOSZENIE: " + formatted_time    #str(instance.data)

    asp = Asp.objects.create(cel=cel, adres=adres, tytul=tytul, info=info, data=instance.data)
    asp.save()


def TempEmail(cel, adres, instance):
    tytul = "Zgłoszenie faktury od " + instance.osoba.naz_imie
    data = str(instance.data)

    osoba= instance.osoba.naz_imie
    targi= instance.targi
    stoisko= instance.stoisko
    rodzaj_fv= instance.rfaktura
    termin= str(instance.termin)
    kwota= str(instance.kwota)
    za_co= instance.zaco
    projekt_specyfikacja= instance.spec
    zgloszenie= data
    sda_wersja= INFO_PROGRAM[0]['WERSJA']
    info = faktura_body(osoba, targi, stoisko, rodzaj_fv, termin, kwota, za_co, projekt_specyfikacja, zgloszenie, sda_wersja)

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
                row = Osoba.objects.filter(naz_imie=instance.osoba.naz_imie).values_list('skype','email')

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