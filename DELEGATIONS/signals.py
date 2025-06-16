from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Delegacja
from INVOICES.models import Osoba
import datetime
from TaskAPI.models import Asp
from TaskAPI.rap_temp import email_temp1, email_temp2
from django.conf import settings
from SDA.settings import INFO_PROGRAM




def TempSkype(cel, adres, instance):
    tytul = "Zgłoszenie delegacji od " + instance.osoba.naz_imie
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


def delegacja_body(osoba, targi, data_od, data_do, kasa_pln, kasa_euro, kasa_funt, kasa_inna, kasa_karta, zgloszenie,
                   sda_wersja):
    """
    Generuje treść HTML dla powiadomienia o delegacji.

    Parametry:
    - osoba: Imię i nazwisko osoby delegowanej
    - targi: Nazwa targów
    - data_od: Data rozpoczęcia delegacji w formacie RRRR-MM-DD
    - data_do: Data zakończenia delegacji w formacie RRRR-MM-DD
    - kasa_pln: Kwota w PLN
    - kasa_euro: Kwota w EUR
    - kasa_funt: Kwota w GBP
    - kasa_inna: Kwota w innej walucie
    - kasa_karta: Kwota na karcie (z jednostką walutową)
    - zgloszenie: Data i czas zgłoszenia w formacie RRRR-MM-DD GG:MM:SS
    - sda_wersja: Wersja SDA

    Zwraca:
    - String zawierający kod HTML
    """

    html = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; ">
            <style type="text/css">
                table {{
                    table-layout: fixed;
                }}
                body {{
                    width: 100% !important;
                    -webkit-text-size-adjust: 100%;
                    -ms-text-size-adjust: 100%;
                    margin: 0;
                    padding: 0;
                }}
                table td {{
                    border-collapse: collapse;
                }}
                .content-td {{
                    color: #525252;
                    font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;
                }}
                .content-div p {{
                    margin: 0 0 17px 0;
                    line-height: 1.5;
                }}
                .content-div a {{
                    color: #1251ba;
                    text-decoration:underline;
                }}
                .content-div a:hover {{
                    color: unset;
                }}
                .content-div ol {{
                    list-style: decimal;
                    margin: 0 0 0 40px;
                    padding: 0;
                }}
                .content-div > :first-child {{
                    margin-top: 0 !important;
                    padding-top: 0 !important;
                }}
                .content-div > :last-child {{
                    margin-bottom: 0 !important;
                    padding-bottom: 0 !important;
                }}
            </style>
        </head>

        <body style="background-color:#f9f9f9;" bgcolor="#f9f9f9">
            <table cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="#f9f9f9" style="background-color:#f9f9f9;border-collapse:collapse;font-size:1px!important;line-height:100%!important;min-width:320px;width:100%!important;margin:0;padding:0;mso-table-lspace:0pt;mso-table-rspace:0pt;">
                <tbody>
                    <tr>
                        <td align="center" valign="top">
                            <div style="height:20px;line-height:20px;font-size:15px;background-color:#f9f9f9;padding:0;margin:0;" bgcolor="#f9f9f9">&nbsp;</div>
                            <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;max-width:935px;min-width:320px;mso-table-lspace:0pt;mso-table-rspace:0pt;" class="main-wrap">
                                <tbody>
                                    <tr>
                                        <td width="20" style="width:20px;max-width:20px;min-width:20px;background-color:#f9f9f9;padding:0;" bgcolor="#f9f9f9">&nbsp;</td>
                                        <td valign="top" align="center">
                                            <div style="height:2px;line-height:2px;font-size:1px;background-color:#ff0000;padding:0;margin:0;" bgcolor="#ff0000">&nbsp;</div>
                                            <table cellpadding="0" cellspacing="0" border="0" class="message_body" width="100%" style="border-collapse:collapse;border-color:#dddddd;border-style:solid;border-width:0 1px 1px 1px;mso-table-lspace:0pt;mso-table-rspace:0pt;width:100%;">
                                                <tbody>
                                                    <tr>
                                                        <td width="40" style="width:40px;max-width:40px;min-width:40px;background-color:#ffffff;padding:0;" bgcolor="#ffffff">&nbsp;</td>
                                                        <td class="content-td" style="background-color:white;color:#525252;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:15px;line-height:22px;overflow:hidden;" bgcolor="white">
                                                            <div style="height:30px;line-height:30px;font-size:25px;background-color:#ffffff;padding:0;margin:0;" bgcolor="#ffffff">&nbsp;</div>
                                                            <div class="content-div">
                                                                <div style="font-family: 'Helvetica Neue', helvetica, sans-serif; font-size: 16px; line-height: 22px; margin: 6px 0 9px;">
                                                                    <br>
                                                                    <span style="font-size:18px; font-weight:bold;"><span style="font-size:22px; font-weight:bold;">Zgłoszenie delegacji</span> od {osoba}</span><br><br>
                                                                    <table style="border-spacing:0; width:90%;" cellspacing="0" cellpadding="0">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>TARGI: </b></td>
                                                                                <td style="width:60%;">{targi}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>DATA OD: </b></td>
                                                                                <td style="width:60%;">{data_od}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>DATA DO: </b></td>
                                                                                <td style="width:60%;">{data_do}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>KASA PLN: </b></td>
                                                                                <td style="width:60%;">{kasa_pln}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>KASA EURO: </b>&nbsp;&nbsp;&nbsp;</td>
                                                                                <td style="width:60%;">{kasa_euro}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>KASA FUNT: </b></td>
                                                                                <td style="width:60%;">{kasa_funt}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>KASA INNA: </b></td>
                                                                                <td style="width:60%;">{kasa_inna}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>KASA KARTA: </b></td>
                                                                                <td style="width:60%;">{kasa_karta}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>ZGŁOSZENIE: </b></td>
                                                                                <td style="width:60%;">{zgloszenie}</td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                    <hr>
                                                                    <small style="color: gray;">
                                                                        <p>SDA wersja: {sda_wersja}</p>
                                                                    </small>
                                                                </div>
                                                            </div>
                                                            <div style="height:30px;line-height:30px;font-size:25px;background-color:#ffffff;padding:0;margin:0;" bgcolor="#ffffff">&nbsp;</div>
                                                        </td>
                                                        <td width="40" style="width:40px;max-width:40px;min-width:40px;background-color:#ffffff;padding:0;" bgcolor="#ffffff">&nbsp;</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                        <td width="20" style="width:20px;max-width:20px;min-width:20px;background-color:#f9f9f9;padding:0;" bgcolor="#f9f9f9">&nbsp;</td>
                                    </tr>
                                </tbody>
                            </table>
                            <div style="height:20px;line-height:20px;font-size:15px;background-color:#f9f9f9;padding:0;margin:0;" bgcolor="#f9f9f9">&nbsp;</div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>"""

    return html























def TempEmail(cel, adres, instance):
    tytul = "Zgłoszenie delegacji od " + instance.osoba.naz_imie
    data = str(instance.dataz) # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #str(instance.data)

    osoba= instance.osoba.naz_imie
    targi= instance.targi
    data_od = str(instance.data_od)
    data_do = str(instance.data_do)
    kasa_pln = str(instance.kasa_pln)
    kasa_euro = str(instance.kasa_euro)
    kasa_funt = str(instance.kasa_funt)
    kasa_inna = str(instance.kasa_inna)
    kasa_karta = str(instance.kasa_karta)
    zgloszenie = data
    sda_wersja= INFO_PROGRAM[0]['WERSJA']
    info = delegacja_body(osoba, targi, data_od, data_do, kasa_pln, kasa_euro, kasa_funt, kasa_inna, kasa_karta, zgloszenie, sda_wersja)

    asp = Asp.objects.create(cel=cel, adres=adres, tytul=tytul, info=info, data=data)
    asp.save()





@receiver([post_save], sender=Delegacja)
def Delegacja_save(sender, instance, **kwargs):
    if kwargs['created']:
        cel = settings.DELEGATIONS_TO_TARGET
        # print(">>> <<< ", instance)

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
