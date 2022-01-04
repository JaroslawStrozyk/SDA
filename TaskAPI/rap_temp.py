

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
            + '<span style="font-size:18px; font-weight:bold;">'+ data +' </span><br/><br/>'\
            + '<table style="border-spacing:0;" cellspacing="0" cellpadding="0">'

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