from django.http import HttpResponse
from django.shortcuts import redirect

from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle, Paragraph, SimpleDocTemplate
from reportlab.platypus.tables import Table
from PIL import Image
from django.conf import settings
from datetime import datetime
import os


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
    return name_log, inicjaly


def out_pdf_sde(request, sde, tytul):

    name_log, inicjaly = test_osoba(request)

    tytulw = 'plik: ' + tytul + '.pdf'
    adata = datetime.now().strftime('%Y-%m-%d')

    # PDF
    response = HttpResponse(content_type='application/pdf')
    titlefile = tytul + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=landscape(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, (20), (height - 80), width=80, height=68) #100, 85
    p.setFont("Dejavu", 10)
    p.drawString(((width - 80)), (height - 30), adata)
    p.setFont("Dejavu-Bold", 16)
    p.drawString(((width / 2) - 70), (height - 50), "Zestawienie SDE")
    p.setFont("Dejavu", 7)

    data = []
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    lp = 0
    ls = 0
    headings = ('Lp', 'Nr zlecenia', 'Klient', 'Targi', 'Stoisko/Opis', 'FV sprzed.', 'PM')  # MAX 25 wpisów

    for pz in sde:
        lp = lp + 1
        if lp <= 30:

            ls = 1
            if len(pz.klient) > 18:
                klient = pz.klient[0:18] +"..."
            else:
                klient = pz.klient

            if len(pz.targi) > 18:
                targi = pz.targi[0:18] +"..."
            else:
                targi = pz.targi

            if len(pz.opis) > 56:
                opis = pz.opis[0:56] +"..."
            else:
                opis = pz.opis
            data.append([lp, pz.nazwa, klient, targi, opis, pz.mcs+" "+pz.rks, pz.pm])
        else:

            ls = 2
            if lp <= 62:

                if len(pz.klient) > 18:
                    klient = pz.klient[0:18] + "..."
                else:
                    klient = pz.klient

                if len(pz.targi) > 18:
                    targi = pz.targi[0:18] + "..."
                else:
                    targi = pz.targi

                if len(pz.opis) > 56:
                    opis = pz.opis[0:56] + "..."
                else:
                    opis = pz.opis
                data1.append([lp, pz.nazwa, klient, targi, opis, pz.mcs + " " + pz.rks, pz.pm])
            else:

                ls = 3
                if lp <= 94:

                    if len(pz.klient) > 18:
                        klient = pz.klient[0:18] + "..."
                    else:
                        klient = pz.klient

                    if len(pz.targi) > 18:
                        targi = pz.targi[0:18] + "..."
                    else:
                        targi = pz.targi

                    if len(pz.opis) > 56:
                        opis = pz.opis[0:56] + "..."
                    else:
                        opis = pz.opis
                    data2.append([lp, pz.nazwa, klient, targi, opis, pz.mcs + " " + pz.rks, pz.pm])
                else:

                    ls = 4
                    if lp <= 126:

                        if len(pz.klient) > 18:
                            klient = pz.klient[0:18] + "..."
                        else:
                            klient = pz.klient

                        if len(pz.targi) > 18:
                            targi = pz.targi[0:18] + "..."
                        else:
                            targi = pz.targi

                        if len(pz.opis) > 56:
                            opis = pz.opis[0:56] + "..."
                        else:
                            opis = pz.opis
                        data3.append([lp, pz.nazwa, klient, targi, opis, pz.mcs + " " + pz.rks, pz.pm])
                    else:

                        ls = 5
                        if len(pz.klient) > 18:
                            klient = pz.klient[0:18] + "..."
                        else:
                            klient = pz.klient

                        if len(pz.targi) > 18:
                            targi = pz.targi[0:18] + "..."
                        else:
                            targi = pz.targi

                        if len(pz.opis) > 56:
                            opis = pz.opis[0:56] + "..."
                        else:
                            opis = pz.opis
                        data4.append([lp, pz.nazwa, klient, targi, opis, pz.mcs + " " + pz.rks, pz.pm])


    f = Table([headings] + data, rowHeights=16, colWidths=[20, 70, 110, 110, 310, 80, 100])
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    if len(sde) <= 30:
        shift = height - (100 + (16 * lp))
        f.drawOn(p, 20, shift)
    else:
        f.drawOn(p, 20, 16)

        datan = [(tytulw + ", strona: 1/"+ str(ls),)]
        f = Table(datan, rowHeights=10, colWidths=800)
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
            ('FONT', (0, 0), (-1, 0), 'Dejavu', 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 20, height - 15)


    if len(sde) > 30:
        p.showPage()
        f = Table([headings] + data1, rowHeights=16, colWidths=[20, 70, 110, 110, 310, 80, 100])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        shift = height - (480 + (16 * (len(data1) - 26)))  # lp
        f.drawOn(p, 20, shift)

        datan = [(tytulw + ", strona: 2/"+ str(ls),)]
        f = Table(datan, rowHeights=10, colWidths=800)
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
            ('FONT', (0, 0), (-1, 0), 'Dejavu', 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 20, height - 15)


    if len(sde) > 62:
        p.showPage()
        f = Table([headings] + data2, rowHeights=16, colWidths=[20, 70, 110, 110, 310, 80, 100])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        shift = height - (480 + (16 * (len(data2) - 26)))
        f.drawOn(p, 20, shift)

        datan = [(tytulw + ", strona: 3/"+ str(ls),)]
        f = Table(datan, rowHeights=10, colWidths=800)
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
            ('FONT', (0, 0), (-1, 0), 'Dejavu', 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 20, height - 15)



    if len(sde) > 94:
        p.showPage()
        f = Table([headings] + data3, rowHeights=16, colWidths=[20, 70, 110, 110, 310, 80, 100])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        shift = height - (480 + (16 * (len(data3) - 26)))
        f.drawOn(p, 20, shift)

        datan = [(tytulw + ", strona: 4/"+ str(ls),)]
        f = Table(datan, rowHeights=10, colWidths=800)
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
            ('FONT', (0, 0), (-1, 0), 'Dejavu', 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 20, height - 15)


    if len(sde) > 126:
        p.showPage()
        f = Table([headings] + data4, rowHeights=16, colWidths=[20, 70, 110, 110, 310, 80, 100])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        shift = height - (480 + (16 * (len(data4) - 26)))
        f.drawOn(p, 20, shift)

        datan = [(tytulw + ", strona: 5/"+ str(ls),)]
        f = Table(datan, rowHeights=10, colWidths=800)
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
            ('FONT', (0, 0), (-1, 0), 'Dejavu', 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 20, height - 15)



    p.showPage()
    p.save()
    return response


def FirstPage(p, height, DATA, ind_start, ind_stop, tytul, adata, suma, suma_c, fsc, opis, nr_strony, koniec):
    # Nagłówek
    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 30, (height - 85), width=80, height=68)

    datan = [(tytul + ", strona: " + str(nr_strony),)]
    f = Table(datan, rowHeights=10, colWidths=800)
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('FONT', (0, 0), (-1, 0), 'Dejavu', 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, height - 20)
    suma_w = ''
    if fsc:
        suma_w = suma + " [" + str(suma_c) + "]"
    else:
        suma_w = suma

    datan = [['','Zamówienia', adata],['','', suma_w],['',opis,'']]
    f = Table(datan, rowHeights=20, colWidths=[100, 370, 330])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.black),
        ('FONT', (1, 0), (1, 1), 'Dejavu-Bold', 16),
        ('FONT', (2, 0), (-1, -1), 'Dejavu', 11),
        ('FONT', (1, 2), (2, 2), 'Dejavu', 10),
        ('FONT', (2, 1), (2, 1), 'Dejavu', 9),
        ('TEXTCOLOR', (2, 1), (2, 1), colors.red),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (0, -1)),
        ('SPAN', (1, 0), (1, -2)),
        ('SPAN', (1, 2), (2, 2)),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, height - 80)
    # Koniec nagłówka
    # Generowanie strony
    dt_row = []
    for i in range(ind_start, ind_stop):
        dt_row.append(DATA[i])

    ll = len(dt_row)
    headings = ('Kontrahent', 'Opis', 'SDE/MPK', 'Sposób\npłatności', 'Rozliczenie', 'Netto', 'Brutto')
    f = Table([headings] + dt_row, rowHeights=25, colWidths=[200, 200, 85, 55, 100, 80, 80])
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
        ('ALIGN', (6, 1), (6, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, (height - 125) - (ll * 25))
    p.showPage()


def NextPage(p, height, DATA, ind_start, ind_stop, tytul, nr_strony, koniec):
    # Nagłówek

    datan = [(tytul + ", strona: " + str(nr_strony),)]
    f = Table(datan, rowHeights=10, colWidths=800)
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('FONT', (0, 0), (-1, 0), 'Dejavu', 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, height - 20)

    dt_row = []
    for i in range(ind_start, ind_stop):
        dt_row.append(DATA[i])

    ll = len(dt_row)
    headings = ('Kontrahent', 'Opis', 'SDE/MPK', 'Sposób\npłatności', 'Rozliczenie', 'Netto', 'Brutto')
    f = Table([headings] + dt_row, rowHeights=25, colWidths=[200, 200, 85, 55, 100, 80, 80])
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
        ('ALIGN', (6, 1), (6, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, (height - 50) - (ll * 25))
    p.showPage()


def GeneratePage(DATA_ROW):
    cll = len(DATA_ROW)
    KARTY = []
    llps = 19      # Liczba linii - pierwsza strona
    llks = 22      # liczba linii - kolejna strona
    ind_start = 0
    ind_stop = 18
    f = 0
    while cll > 0:
        if f==0:
            llns = llps
        else:
            llns = llks

        if cll >= llns:
            if f!=0:
                ind_start = ind_stop + 1
                ind_stop = ind_stop + llns

            KARTY.append([llns,'', ind_start, ind_stop, 0])
            cll = cll - llns
        else:
            if f==0:
                ind_start = 0
                ind_stop = cll
            else:
                ind_start = ind_stop + 1
                ind_stop = ind_stop + cll

            KARTY.append([cll,'',ind_start, ind_stop, 0])
            cll = cll - llns
        f = 1

    ls = len(KARTY)
    KARTY[ls - 1][4] = 1
    for i in range(0,ls):
        KARTY[i][1] = str(i + 1) + "/" + str(ls)

    return KARTY


def StrConwert(str, linia):
    s = ''
    if len(str) >= linia:
        s = str[:linia] + "\n"
        st = str[linia:]
        if len(st)>=linia:
            s = s + st[:linia-3]+"..."
        else:
            s = s + st
    else:
        s = str
    return s


def out_pdf_ord(request, zamowienia, tytul, suma, suma_c, fsc, opis_tab, adata):


    # PDF setup
    response = HttpResponse(content_type='application/pdf')
    titlefile = tytul + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=landscape(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))
    #
    # Konwersja tabeli
    DATA_ROW = []
    for z in zamowienia:

        sde_mpk = ""
        if z.nr_sde != None:
            sde_mpk = str(z.nr_sde).split("......")[0]
        elif z.nr_mpk != None:
            sde_mpk = str(z.nr_mpk).split("......")[0]

        linia = 38
        kontrahent = StrConwert(z.kontrahent, linia)
        linia = 38
        opis = StrConwert(z.opis, linia)
        linia = 18
        nr_dok3 = StrConwert(z.nr_dok3,linia)

        DATA_ROW.append([kontrahent, opis, sde_mpk, z.sposob_plat, nr_dok3, z.kwota_netto, z.kwota_brutto])

    f = 0
    for k in GeneratePage(DATA_ROW):
        if f==0:
            FirstPage(p, height, DATA_ROW, k[2], k[3], tytul, adata, suma, suma_c, fsc, opis_tab, k[1], k[4])
            f = 1
        else:
            NextPage(p, height, DATA_ROW, k[2], k[3], tytul,  k[1], k[4])

    p.save()

    return response
