def faktura_body(osoba, targi, stoisko, rodzaj_fv, termin, kwota, za_co, projekt_specyfikacja, zgloszenie, sda_wersja):
    """
    Generuje treść HTML dla powiadomienia o fakturze.

    Parametry:
    - osoba: Imię i nazwisko osoby zgłaszającej fakturę
    - targi: Nazwa targów
    - stoisko: Nazwa stoiska
    - rodzaj_fv: Rodzaj faktury (np. PROFORMA)
    - termin: Data terminu płatności w formacie RRRR-MM-DD
    - kwota: Kwota faktury (z jednostką walutową)
    - za_co: Dodatkowe informacje (za co jest faktura)
    - projekt_specyfikacja: Dodatkowe informacje o projekcie
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
                                                                    <span style="font-size:18px; font-weight:bold;"><span style="font-size:22px; font-weight:bold;">Zgłoszenie faktury</span> od {osoba}</span><br><br>
                                                                    <table style="border-spacing:0; width:90%;" cellspacing="0" cellpadding="0">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>TARGI: </b></td>
                                                                                <td style="width:60%;">{targi}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>STOISKO: </b></td>
                                                                                <td style="width:60%;">{stoisko}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>RODZAJ FV: </b></td>
                                                                                <td style="width:60%;">{rodzaj_fv}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>TERMIN: </b></td>
                                                                                <td style="width:60%;">{termin}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>KWOTA: </b>&nbsp;&nbsp;&nbsp;</td>
                                                                                <td style="width:60%;">{kwota}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>ZA CO: </b></td>
                                                                                <td style="width:60%;">{za_co}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>PROJEKT SPECYFIKACJA: </b></td>
                                                                                <td style="width:60%;">{projekt_specyfikacja}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="width:40%;"><b>NIE ZGŁOSZENIE: </b></td>
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


def delegacja_body(osoba, targi, data_od, data_do, kasa_pln, kasa_euro, kasa_funt, kasa_inna, kasa_karta, zgloszenie, sda_wersja):
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




























def email_body(title, data):
    temp = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"><html>'\
            + '<head><meta http-equiv="Content-Type" content="text/html; "><style type="text/css">'\
            + 'table { table-layout: fixed; }'\
            + 'body { width: 100% !important; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; margin: 0; padding: 0; }'\
            + 'table td { border-collapse: collapse; }'\
            + '.content-td { color: #525252; /*box-shadow: 0 1px 3px 0 rgba(0,0,0,.05);*/ font-family: &#39;Helvetica Neue&#39;,Helvetica,Arial,sans-serif; }'\
            + '.content-div p { margin: 0 0 17px 0; line-height: 1.5; }'\
            + '.content-div a { color: #1251ba; text-decoration:underline; }'\
            + '.content-div a:hover { color: unset; }'\
            + '.content-div ol { list-style: decimal; margin: 0 0 0 40px; padding: 0; }'\
            + '.content-div > :first-child { margin-top: 0 !important; padding-top: 0 !important; }'\
            + '.content-div > :last-child { margin-bottom: 0 !important; padding-bottom: 0 !important; }'\
            + '@media screen and (max-width: 935px) { .main-wrap { width: 100% !important; } }'\
            + '</style></head><body style="background-color:#f9f9f9;" bgcolor="#f9f9f9">'\
            + '<table cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="#f9f9f9" style="background-color:#f9f9f9;border-collapse:collapse;font-size:1px!important;line-height:100%!important;min-width:320px;width:100%!important;margin:0;padding:0;mso-table-lspace:0pt;mso-table-rspace:0pt;">'\
            + '<tr><td align="center" valign="top"><div style="height:20px;line-height:20px;font-size:15px;background-color:#f9f9f9;padding:0;margin:0;" bgcolor="#f9f9f9">&nbsp;</div>'\
            + '<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;max-width:935px;min-width:320px;mso-table-lspace:0pt;mso-table-rspace:0pt;" class="main-wrap">'\
            + '<tr><td width="20" style="width:20px;max-width:20px;min-width:20px;background-color:#f9f9f9;padding:0;" bgcolor="#f9f9f9">&nbsp;</td>'\
            + '<td valign="top" align="center"><div style="height:2px;line-height:2px;font-size:1px;background-color:#00a94f;padding:0;margin:0;" bgcolor="#00a94f">&nbsp;</div>'\
            + '<table cellpadding="0" cellspacing="0" border="0" class="message_body" width="100%" style="border-collapse:collapse;border-color:#dddddd;border-style:solid;border-width:0 1px 1px 1px;mso-table-lspace:0pt;mso-table-rspace:0pt;width:100%;">'\
            + '<tr><td width="40" style="width:40px;max-width:40px;min-width:40px;background-color:#ffffff;padding:0;" bgcolor="#ffffff">&nbsp;</td>'\
            + '<td class="content-td" style="background-color:white;color:#525252;font-family:&#39;Helvetica Neue&#39;,Helvetica,Arial,sans-serif;font-size:15px;line-height:22px;overflow:hidden;" bgcolor="white">'\
            + '<div style="height:30px;line-height:30px;font-size:25px;background-color:#ffffff;padding:0;margin:0;" bgcolor="#ffffff">&nbsp;</div><div class="content-div">'\
            + '<div style="font-family: \'Helvetica Neue\', helvetica, sans-serif; font-size: 16px; line-height: 22px; margin: 6px 0 9px;"><br/>'\
            + '<span style="font-size:18px; font-weight:bold;"><span style=\'font-size:22px; font-weight:bold;\'>Raport z SDA</span>&nbsp;&nbsp;moduł powiadomień&nbsp;-&nbsp;'+title+'</span><br/><br/>'\
            + '<span style="font-size:18px; font-weight:bold;">Data raportu: '+ data +' </span><br/><br/>'\
            + '<table style="border-spacing:0;" cellspacing="0" cellpadding="0" width="100%">'
    return temp


def email_temp1(data):
    temp = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"><html>'\
            + '<head><meta http-equiv="Content-Type" content="text/html; "><style type="text/css">'\
            + 'table { table-layout: fixed; }'\
            + 'body { width: 100% !important; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; margin: 0; padding: 0; }'\
            + 'table td { border-collapse: collapse; }'\
            + '.content-td { color: #525252; /*box-shadow: 0 1px 3px 0 rgba(0,0,0,.05);*/ font-family: &#39;Helvetica Neue&#39;,Helvetica,Arial,sans-serif; }'\
            + '.content-div p { margin: 0 0 17px 0; line-height: 1.5; }'\
            + '.content-div a { color: #1251ba; text-decoration:underline; }'\
            + '.content-div a:hover { color: unset; }'\
            + '.content-div ol { list-style: decimal; margin: 0 0 0 40px; padding: 0; }'\
            + '.content-div > :first-child { margin-top: 0 !important; padding-top: 0 !important; }'\
            + '.content-div > :last-child { margin-bottom: 0 !important; padding-bottom: 0 !important; }'\
            + '@media screen and (max-width: 935px) { .main-wrap { width: 100% !important; } }'\
            + '</style></head><body style="background-color:#f9f9f9;" bgcolor="#f9f9f9">'\
            + '<table cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="#f9f9f9" style="background-color:#f9f9f9;border-collapse:collapse;font-size:1px!important;line-height:100%!important;min-width:320px;width:100%!important;margin:0;padding:0;mso-table-lspace:0pt;mso-table-rspace:0pt;">'\
            + '<tr><td align="center" valign="top"><div style="height:20px;line-height:20px;font-size:15px;background-color:#f9f9f9;padding:0;margin:0;" bgcolor="#f9f9f9">&nbsp;</div>'\
            + '<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;max-width:935px;min-width:320px;mso-table-lspace:0pt;mso-table-rspace:0pt;" class="main-wrap">'\
            + '<tr><td width="20" style="width:20px;max-width:20px;min-width:20px;background-color:#f9f9f9;padding:0;" bgcolor="#f9f9f9">&nbsp;</td>'\
            + '<td valign="top" align="center"><div style="height:2px;line-height:2px;font-size:1px;background-color:#00a94f;padding:0;margin:0;" bgcolor="#00a94f">&nbsp;</div>'\
            + '<table cellpadding="0" cellspacing="0" border="0" class="message_body" width="100%" style="border-collapse:collapse;border-color:#dddddd;border-style:solid;border-width:0 1px 1px 1px;mso-table-lspace:0pt;mso-table-rspace:0pt;width:100%;">'\
            + '<tr><td width="40" style="width:40px;max-width:40px;min-width:40px;background-color:#ffffff;padding:0;" bgcolor="#ffffff">&nbsp;</td>'\
            + '<td class="content-td" style="background-color:white;color:#525252;font-family:&#39;Helvetica Neue&#39;,Helvetica,Arial,sans-serif;font-size:15px;line-height:22px;overflow:hidden;" bgcolor="white">'\
            + '<div style="height:30px;line-height:30px;font-size:25px;background-color:#ffffff;padding:0;margin:0;" bgcolor="#ffffff">&nbsp;</div><div class="content-div">'\
            + '<div style="font-family: \'Helvetica Neue\', helvetica, sans-serif; font-size: 16px; line-height: 22px; margin: 6px 0 9px;"><br/>'\
            + '<span style="font-size:18px; font-weight:bold;"><span style=\'font-size:22px; font-weight:bold;\'>Raport z SDA</span>&nbsp;&nbsp;moduł powiadomień</span><br/><br/>'\
            + '<span style="font-size:18px; font-weight:bold;">Data raportu: '+ data +' </span><br/><br/>'\
            + '<table style="border-spacing:0;" cellspacing="0" cellpadding="0" width="100%">'

    return temp


def email_temp2():
    temp = '</table>'\
           + '<br><br></body></html>'
    return temp


def ubezpieczenie(us, rodzaj, typ, rej):
    temp = '<tr><td><b>Ubezpieczenie<b></td><td colspan="2">&nbsp;</td></tr>'\
           + '<tr><td><b>Zdarzenie</b></td><td width="10">:</td><td style="color:blue;">Zbliża się termin płatności.</td></tr>'\
           + '<tr><td><b>Data</b></td><td>:</td><td>' + str(us) + '</td></tr>'\
           + '<tr><td><b>Dotyczy</b></td><td>:</td><td>' + rodzaj + ', ' + typ + ', ' + rej + '</td></tr>'\
           + '<tr><td colspan="4">&nbsp;</td></tr>'
    return temp


def ubezpieczenie_p(us, rodzaj, typ, rej):
    temp = '<tr><td><b>Ubezpieczenie<b></td><td colspan="2">&nbsp;</td></tr>'\
           + '<tr><td><b>Zdarzenie</b></td><td width="10">:</td><td style="color:red;">Minął termin płatności.</td></tr>'\
           + '<tr><td><b>Data</b></td><td>:</td><td>' + str(us) + '</td></tr>'\
           + '<tr><td><b>Dotyczy</b></td><td>:</td><td>' + rodzaj + ', ' + typ + ', ' + rej + '</td></tr>'\
           + '<tr><td colspan="4">&nbsp;</td></tr>'
    return temp


def insurance(dt, firma, nazwa, dotyczy):
    temp = '<tr><td style="width:150px;color:brown;"><b>Ubezpieczenie<b></td><td style="width:10px;"></dt><td>&nbsp;</td></tr>'\
           + '<tr><td><b>Zdarzenie</b></td><td>:</td><td style="color:blue;width:100%">Zbliża się termin płatności.</td></tr>'\
           + '<tr><td><b>Data</b></td><td>:</td><td>' + str(dt) + '</td></tr>'\
           + '<tr><td><b>Dotyczy</b></td><td>:</td><td>' + firma + ', ' + nazwa + ', ' + dotyczy + '</td></tr>'\
           + '<tr><td colspan="3">&nbsp;</td></tr>'
    return temp


def insurance_after(dt, firma, nazwa, dotyczy):
    temp = '<tr><td style="width:150px;color:brown;"><b>Ubezpieczenie<b></td><td style="width:10px;"></dt><td>&nbsp;</td></tr>'\
           + '<tr><td><b>Zdarzenie</b></td><td>:</td><td style="color:red;width:100%">Minął termin płatności.</td></tr>'\
           + '<tr><td><b>Data</b></td><td>:</td><td>' + str(dt) + '</td></tr>'\
           + '<tr><td><b>Dotyczy</b></td><td>:</td><td>' + firma + ', ' + nazwa + ', ' + dotyczy + '</td></tr>'\
           + '<tr><td colspan="3">&nbsp;</td></tr>'
    return temp


def term(dt, firma, dotyczy):
    temp = '<tr><td style="width:150px;color:brown;"><b>Terminy<b></td><td style="width:10px;"></dt><td>&nbsp;</td></tr>'\
           + '<tr><td><b>Zdarzenie</b></td><td>:</td><td style="color:blue;width:100%">Zbliża się termin płatności.</td></tr>'\
           + '<tr><td><b>Data</b></td><td>:</td><td>' + str(dt) + '</td></tr>'\
           + '<tr><td><b>Dotyczy</b></td><td>:</td><td>' + firma + ', ' + dotyczy + '</td></tr>'\
           + '<tr><td colspan="3">&nbsp;</td></tr>'
    return temp


def term_after(dt, firma, dotyczy):
    temp = '<tr><td style="width:150px;color:brown;"><b>Terminy<b></td><td style="width:10px;"></dt><td>&nbsp;</td></tr>'\
           + '<tr><td><b>Zdarzenie</b></td><td>:</td><td style="color:red;width:100%">Minął termin płatności.</td></tr>'\
           + '<tr><td><b>Data</b></td><td>:</td><td>' + str(dt) + '</td></tr>'\
           + '<tr><td><b>Dotyczy</b></td><td>:</td><td>' + firma + ', ' + dotyczy + '</td></tr>'\
           + '<tr><td colspan="3">&nbsp;</td></tr>'
    return temp


def timber(dt, magazyn, nr_sde_nazwa, targi, klient, stoisko, pm): #dt, firma, nazwa, dotyczy
    temp = '<tr><td style="width:150px;color:#525252;"><b>Dotyczy</b></td><td style="width:10px;">:</dt><td style="color:gray;"><b>Czas przechowywania<b></td></tr>'\
           + '<tr><td style="color:#525252;"><b>Zdarzenie</b></td><td>:</td><td style="color:blue;width:100%"><b>Zbliża się termin przechowywania.</b></td></tr>'\
           + '<tr><td style="color:#525252;"><b>Data</b></td><td>:</td><td>' + str(dt) + '</td></tr>' \
           + '<tr><td style="color:#525252;"><b>Magazyn</b></td><td>:</td><td>' + magazyn.upper() + '</td></tr>' \
           + '<tr><td style="color:#525252;"><b>Dane</b></td><td>:</td><td> SDE ' + nr_sde_nazwa + ', ' + targi + ', ' + klient + ', ' + stoisko + '</td></tr>' \
           + '<tr><td style="color:#525252;"><b>PM</b></td><td>:</td><td style="color:gray">' + pm + '</td></tr>' \
           + '<tr><td colspan="3">&nbsp;</td></tr>'
    return temp


def timber_after(dt, magazyn, nr_sde_nazwa, targi, klient, stoisko, pm):
    temp = '<tr><td style="width:150px;color:#525252;"><b>Dotyczy<b></td><td style="width:10px;">:</dt><td style="color:gray;"><b>Czas przechowywania<b></td></tr>'\
           + '<tr><td style="color:#525252;"><b>Zdarzenie</b></td><td>:</td><td style="color:red;width:100%"><b>Minął termin przechowywania.</b></td></tr>'\
           + '<tr><td style="color:#525252;"><b>Data</b></td><td>:</td><td>' + str(dt) + '</td></tr>' \
           + '<tr><td style="color:#525252;"><b>Magazyn</b></td><td>:</td><td>' + magazyn.upper() + '</td></tr>' \
           + '<tr><td style="color:#525252;"><b>Dane</b></td><td>:</td><td> SDE ' + nr_sde_nazwa + ', ' + targi + ', ' + klient + ', ' + stoisko + '</td></tr>' \
           + '<tr><td style="color:#525252;"><b>PM</b></td><td>:</td><td style="color:gray">' + pm + '</td></tr>' \
           + '<tr><td colspan="3">&nbsp;</td></tr>'
    return temp


# <tr><td style="width:150px;color:brown;"><b>Czas przechowywania<b></td><td style="width:10px;"></dt><td>&nbsp;</td></tr>