from .models import Plyta, Rozchod, Przychod, Zwrot, Zestawienie
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle, Paragraph, SimpleDocTemplate
from reportlab.platypus.tables import Table
from PIL import Image
from django.conf import settings
import os
from datetime import datetime


def wz_pdf(request, pk, po):

    pl = Plyta.objects.get(pk=pk)
    poz = Rozchod.objects.get(pk=po)

    data = poz.data.strftime('%d-%m-%Y')
    cel = poz.cel
    nazwa = pl.nazwa
    opis = pl.opis
    jm = pl.jm
    ilosc = poz.ilosc
    try:
        sde = poz.nr_sde.opis
    except:
        sde = ''

    dok_id = poz.doc_id #"WZ-"+str(pl.id)+"."+str(poz.id)

    response = HttpResponse(content_type='application/pdf')
    titlefile = "Protokol przekazania z dnia"+ str(data) + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))
    #pdfmetrics.registerFont(TTFont('Times-Italic', 'DejaVuSerif-Italic.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 20, 760, width=80, height=65)
    p.setFont("Dejavu-Bold", 17)
    p.drawString(150, 780, "PROTOKÓŁ PRZEKAZANIA TOWARU - WZ")
    p.setFont("Dejavu", 10)
    p.drawString(480, 605, "ID:")
    p.drawString(470, 590, "Data:")
    p.setFont("Dejavu-Bold", 10)
    p.drawString(500, 605, dok_id)
    p.drawString(500, 590, data)


    data = [
        ('Cel rozchodu', '', cel),
        ('Nazwa towaru','',nazwa),
        ('Opis towaru', '',opis),
        ('Ilość', '', str(ilosc) + " " + jm),
        ('Nr SDE', '', sde),
            ]
    f = Table(data, rowHeights=[60,30,20,30, 20], colWidths=[124, 3, 400])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (0, -1), 0.1, colors.gray),
        ('GRID', (2, 0), (2, -1), 0.1, colors.gray),
        ('GRID', (4, 0), (4, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONT', (-1, 0), (-1, 0), 'Dejavu-Bold', 11),
        ('TEXTCOLOR', (-1, 0), (-1, 0), colors.red),
        ('FONT', (-1, 1), (-1, 1), 'Dejavu-Bold', 10),
        ('FONT', (-1, 3), (-1, 3), 'Dejavu-Bold', 13),
        ('TEXTCOLOR', (-1, 3), (-1, 3), colors.blue),

    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 420)

    data = [
        ('Wydał', 'Odebrał'),
        ('(data) (podpis)', '(data) (podpis)'),

    ]
    f = Table(data, rowHeights=[20, 50], colWidths=[265, 265])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 1), (1, 1), 'Dejavu', 8),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.gray),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 167) #87

    data = [
        ('Uwagi: ',),
    ]
    f = Table(data, rowHeights=[130], colWidths=[530])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 34)


    p.showPage()
    p.save()
    return response


def pz_pdf(request, pk, po):

    pl = Plyta.objects.get(pk=pk)
    poz = Przychod.objects.get(pk=po)

    data = poz.data.strftime('%d-%m-%Y')
    zrodlo = poz.zrodlo
    nazwa = pl.nazwa
    opis = pl.opis
    stan = pl.stan
    jm = pl.jm
    ilosc = poz.ilosc
    c_j = poz.cena_j
    war = poz.cena

    dok_id = poz.doc_id # "PZ-" + str(pl.id) + "." + str(poz.id)

    response = HttpResponse(content_type='application/pdf')
    titlefile = "Protokol przyjęcia z dnia"+ str(data) + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))
    #pdfmetrics.registerFont(TTFont('Times-Italic', 'DejaVuSerif-Italic.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 20, 760, width=80, height=65)
    p.setFont("Dejavu-Bold", 17)
    p.drawString(150, 780, "PROTOKÓŁ PRZYJĘCIA TOWARU - PZ")
    p.setFont("Dejavu", 10)
    p.drawString(480, 620, "ID:")
    p.drawString(470, 605, "Data:")
    p.setFont("Dejavu-Bold", 10)
    p.drawString(500, 620, dok_id)
    p.drawString(500, 605, data)


    data = [
        ('Zródło przychodu', '', zrodlo),
        ('Nazwa towaru','',nazwa),
        ('Opis towaru', '',opis),
        ('Przyjmowana Ilość', '', str(ilosc) + " " + jm),
        ('Cena jednostkowa', '', str(c_j) + "/" + jm),
        ('Wartość', '', str(war)),
        ('Stan aktualny', '', str(stan) + " " + jm),
            ]
    f = Table(data, rowHeights=[60,30,20,30,20,20,20], colWidths=[124, 3, 400])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (0, -1), 0.1, colors.gray),
        ('GRID', (2, 0), (2, -1), 0.1, colors.gray),
        ('GRID', (4, 0), (4, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONT', (-1, 0), (-1, 0), 'Dejavu-Bold', 11),
        ('TEXTCOLOR', (-1, 0), (-1, 0), colors.red),
        ('FONT', (-1, 1), (-1, 1), 'Dejavu-Bold', 10),
        ('FONT', (-1, 3), (-1, 3), 'Dejavu-Bold', 13),
        ('TEXTCOLOR', (-1, 3), (-1, 3), colors.blue),
        ('TEXTCOLOR', (-1, 4), (-1, 4), colors.green),
        ('FONT', (-1, 5), (-1, 5), 'Dejavu-Bold', 10),
        ('TEXTCOLOR', (-1, 5), (-1, 5), colors.brown),

    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 400)

    data = [
        ('Zatwierdził', 'Przyjął'),
        ('(data) (podpis)', '(data) (podpis)'),

    ]
    f = Table(data, rowHeights=[20, 50], colWidths=[265, 265])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 1), (1, 1), 'Dejavu', 8),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.gray),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 167) #87

    data = [
        ('Uwagi: ',),
    ]
    f = Table(data, rowHeights=[130], colWidths=[530])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 34)


    p.showPage()
    p.save()
    return response


def ze_pdf(request, pk, mag, fl, sel):

    pl = Plyta.objects.get(pk=pk)
    poz = ''
    if sel == 'pr':
        poz = Zestawienie.objects.filter(operacja='Przychód').order_by('-data')
    elif sel == 'ro':
        poz = Zestawienie.objects.filter(operacja='Rozchód').order_by('-data')
    elif sel == 'zw':
        poz = Zestawienie.objects.filter(operacja='Zwrot').order_by('-data')
    elif sel == 'ze':
        poz = Zestawienie.objects.all().order_by('-data')
    else:
        poz = Zestawienie.objects.filter(nr_sde__nazwa=sel).order_by('-data')

    if fl == 'dre':
        magazyn = "Magazyn płyt drewnianych"
    elif fl == 'wew':
        magazyn = "Magazyn wewnętrzny"
    else:
        magazyn = ""

    if mag == 'mag1':
        tytul = "MAGAZYN SZPARAGOWA"
    elif mag == 'mag2':
        tytul = "MAGAZYN PODOLANY"
    else:
        tytul = ""

    data = datetime.today().strftime('%d-%m-%Y')

    response = HttpResponse(content_type='application/pdf')
    titlefile = "Zestawienie operacji "+magazyn+" z dnia "+ str(data) + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    width, height = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 20, 760, width=80, height=65)
    p.setFont("Dejavu-Bold", 17)
    p.drawString(150, 800, "ZESTAWIENIE OPERACJI")
    p.setFont("Dejavu-Bold", 13)
    p.drawString(170, 785, tytul)
    p.drawString(170, 770, magazyn)
    p.setFont("Dejavu", 12)
    p.drawString(490, 785, data)

    dt_row = []
    for r in poz:
        try:
            ns = r.nr_sde.nazwa
        except:
            ns = ''
        dt_row.append([r.dok_id, r.data, r.operacja, r.opis, r.ilosc, r.jm, r.kwota, ns])

    ll = len(dt_row)
    headings = ('ID', 'Data', 'Operacja', 'Opis', 'Ilość','jm', 'Kwota', 'Nr SDE')
    f = Table([headings] + dt_row, rowHeights=25, colWidths=[35, 60, 50, 230, 40, 20, 60, 60])
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (6, 1), (6, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, (height - 125) - (ll * 25))

    p.showPage()
    p.save()
    return response


def pzw_pdf(request, pk, po):

    pl = Plyta.objects.get(pk=pk)
    poz = Zwrot.objects.get(pk=po)

    data = poz.data.strftime('%d-%m-%Y')
    zrodlo = poz.cel
    nazwa = pl.nazwa
    opis = pl.opis
    stan = pl.stan
    jm = pl.jm
    ilosc = poz.ilosc
    try:
        sde = poz.nr_sde.opis
    except:
        sde = ''

    dok_id = "ZT-" + str(pl.id) + "." + str(poz.id)

    response = HttpResponse(content_type='application/pdf')
    titlefile = "Protokol zwrotu z dnia"+ str(data) + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))
    #pdfmetrics.registerFont(TTFont('Times-Italic', 'DejaVuSerif-Italic.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 20, 760, width=80, height=65)
    p.setFont("Dejavu-Bold", 17)
    p.drawString(150, 780, "PROTOKÓŁ ZWROTU TOWARU")
    p.setFont("Dejavu", 10)
    p.drawString(480, 605, "ID:")
    p.drawString(470, 590, "Data:")
    p.setFont("Dejavu-Bold", 10)
    p.drawString(500, 605, dok_id)
    p.drawString(500, 590, data)


    data = [
        ('Opis zwrotu', '', zrodlo),
        ('Nazwa towaru','',nazwa),
        ('Opis towaru', '',opis),
        ('Przyjmowana Ilość', '', str(ilosc) + " " + jm),
        ('Nr SDE', '', sde),
            ]
    f = Table(data, rowHeights=[60,30,20,30, 20], colWidths=[124, 3, 400])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (0, -1), 0.1, colors.gray),
        ('GRID', (2, 0), (2, -1), 0.1, colors.gray),
        ('GRID', (4, 0), (4, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONT', (-1, 0), (-1, 0), 'Dejavu-Bold', 11),
        ('TEXTCOLOR', (-1, 0), (-1, 0), colors.red),
        ('FONT', (-1, 1), (-1, 1), 'Dejavu-Bold', 10),
        ('FONT', (-1, 3), (-1, 3), 'Dejavu-Bold', 13),
        ('TEXTCOLOR', (-1, 3), (-1, 3), colors.blue),

    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 420)

    data = [
        ('Zatwierdził', 'Przyjął'),
        ('(data) (podpis)', '(data) (podpis)'),

    ]
    f = Table(data, rowHeights=[20, 50], colWidths=[265, 265])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 1), (1, 1), 'Dejavu', 8),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.gray),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 167) #87

    data = [
        ('Uwagi: ',),
    ]
    f = Table(data, rowHeights=[130], colWidths=[530])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 34)


    p.showPage()
    p.save()
    return response


def inw_pdf(request, mag, db):
    ext = ''
    if mag == 'mag1':
        tytul = 'Inwentura magazynu Szparagowa'
    elif mag == 'mag2':
        tytul = 'Inwentura magazynu Podolany'
    elif mag == 'mag3':
        tytul = 'Inwentura u Dostawcy'
        #ext = '_chemia'
    else:
        print("MAGAZYN SPOZA ZAKRESU !!!")


    tytulw = 'plik: ' + tytul + ext + '.pdf'
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

    p.setFont("Dejavu-Bold", 16)
    ltxt = int((len(tytul) * 12)/2)
    szer = int((width / 2) - ltxt)

    p.drawString(szer , (height - 50), tytul)
    p.setFont("Dejavu", 7)

    suma_calkowita = 0
    naglowek = []
    data = []
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    lp = 0
    ls = 0
    headings = ('Id.', 'Magazyn', 'Nazwa', 'Opis', 'Wartość', 'Stan', 'Stan z nat.')  # MAX 25 wpisów , 'Test'

    for pz in db:
        suma_calkowita += pz['suma_wart']
        lp = lp + 1
        if lp <= 30:

            ls = 1

            if pz['rodzaj'] == 'dre':
                magazyn = "DREWNA"
            else:
                if mag == 'mag3':
                    magazyn = "CHEMII"
                else:
                    magazyn = "WEWNĘTRZNY"
            nazwa = pz['nazwa']
            opis = pz['opis']
            stan = pz['stan']
            wartosc = pz['suma_wart']

            if pz['brak_ceny'] == 0:
                test = "" #"√"
            else:
                test = "×"

            data.append([pz['id'], magazyn, nazwa, opis, wartosc, stan, '']) # , test
        else:

            ls = 2
            if lp <= 62:

                if pz['rodzaj'] == 'dre':
                    magazyn = "DREWNA"
                else:
                    if mag == 'mag3':
                        magazyn = "CHEMII"
                    else:
                        magazyn = "WEWNĘTRZNY"
                nazwa = pz['nazwa']
                opis = pz['opis']
                stan = pz['stan']
                wartosc = pz['suma_wart']
                if pz['brak_ceny'] == 0:
                    test = ""  # "√"
                else:
                    test = "×"

                data1.append([pz['id'], magazyn, nazwa, opis, wartosc, stan, ''])
            else:

                ls = 3
                if lp <= 94:

                    if pz['rodzaj'] == 'dre':
                        magazyn = "DREWNA"
                    else:
                        if mag == 'mag3':
                            magazyn = "CHEMII"
                        else:
                            magazyn = "WEWNĘTRZNY"
                    nazwa = pz['nazwa']
                    opis = pz['opis']
                    stan = pz['stan']
                    wartosc = pz['suma_wart']
                    if pz['brak_ceny'] == 0:
                        test = ""  # "√"
                    else:
                        test = "×"

                    data2.append([pz['id'], magazyn, nazwa, opis, wartosc, stan, ''])
                else:

                    ls = 4
                    if lp <= 126:

                        if pz['rodzaj'] == 'dre':
                            magazyn = "DREWNA"
                        else:
                            if mag == 'mag3':
                                magazyn = "CHEMII"
                            else:
                                magazyn = "WEWNĘTRZNY"
                        nazwa = pz['nazwa']
                        opis = pz['opis']
                        stan = pz['stan']
                        wartosc = pz['suma_wart']
                        if pz['brak_ceny'] == 0:
                            test = ""  # "√"
                        else:
                            test = "×"

                        data3.append([pz['id'], magazyn, nazwa, opis, wartosc, stan, ''])
                    else:

                        ls = 5

                        if pz['rodzaj'] == 'dre':
                            magazyn = "DREWNA"
                        else:
                            if mag == 'mag3':
                                magazyn = "CHEMII"
                            else:
                                magazyn = "WEWNĘTRZNY"
                        nazwa = pz['nazwa']
                        opis = pz['opis']
                        stan = pz['stan']
                        wartosc = pz['suma_wart']
                        if pz['brak_ceny'] == 0:
                            test = ""  # "√"
                        else:
                            test = "×"

                        data4.append([pz['id'], magazyn, nazwa, opis, wartosc, stan, ''])

    naglowek.append(['DATA', adata])
    naglowek.append(['SUMA', suma_calkowita])

    f = Table(naglowek, rowHeights=30, colWidths=[60, 100])
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 1), (1, 1), 'RIGHT'),
        ('FONT', (1, 1), (1, 1), 'Dejavu-Bold', 10),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.brown),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 660, 515)


    f = Table([headings] + data, rowHeights=16, colWidths=[30, 70, 230, 250, 80, 60, 80]) #800
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
        ('TEXTCOLOR', (4, 1), (4, -1), colors.blue),
        ('TEXTCOLOR', (5, 1), (5, -1), colors.brown),
        ('FONT', (-2, 1), (-1, -1), 'Dejavu-Bold', 9),
    ]))
    f.wrapOn(p, 300, 300)
    if len(db) <= 30:
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


    if len(db) > 30:
        p.showPage()
        f = Table([headings] + data1, rowHeights=16, colWidths=[30, 70, 230, 250, 80, 60, 80])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ('TEXTCOLOR', (4, 1), (4, -1), colors.blue),
            ('TEXTCOLOR', (5, 1), (5, -1), colors.brown),
            ('FONT', (-2, 1), (-1, -1), 'Dejavu-Bold', 9),
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


    if len(db) > 62:
        p.showPage()
        f = Table([headings] + data2, rowHeights=16, colWidths=[30, 70, 230, 250, 80, 60, 80])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ('TEXTCOLOR', (4, 1), (4, -1), colors.blue),
            ('TEXTCOLOR', (5, 1), (5, -1), colors.brown),
            ('FONT', (-2, 1), (-1, -1), 'Dejavu-Bold', 9),
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



    if len(db) > 94:
        p.showPage()
        f = Table([headings] + data3, rowHeights=16, colWidths=[30, 70, 230, 250, 80, 60, 80])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ('TEXTCOLOR', (4, 1), (4, -1), colors.blue),
            ('TEXTCOLOR', (5, 1), (5, -1), colors.brown),
            ('FONT', (-2, 1), (-1, -1), 'Dejavu-Bold', 9),
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


    if len(db) > 126:
        p.showPage()
        f = Table([headings] + data4, rowHeights=16, colWidths=[30, 70, 230, 250, 80, 60, 80])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ('TEXTCOLOR', (4, 1), (4, -1), colors.blue),
            ('TEXTCOLOR', (5, 1), (5, -1), colors.brown),
            ('FONT', (-2, 1), (-1, -1), 'Dejavu-Bold', 9),
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


def inw_pdf_data(request, mag, db, dt):
    ext = ''
    if mag == 'mag1':
        tytul = 'Inwentura magazynu Szparagowa'
    elif mag == 'mag2':
        tytul = 'Inwentura magazynu Podolany'
    elif mag == 'mag3':
        tytul = 'Inwentura magazynu Podolany'
        ext = '_chemia'
    else:
        print("MAGAZYN SPOZA ZAKRESU !!!")


    tytulw = 'plik: ' + tytul + ext + '.pdf'
    adata = dt #datetime.now().strftime('%Y-%m-%d')

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

    p.setFont("Dejavu-Bold", 16)
    ltxt = int((len(tytul) * 12)/2)
    szer = int((width / 2) - ltxt)

    p.drawString(szer , (height - 50), tytul)
    p.setFont("Dejavu", 7)

    suma_calkowita = 0
    naglowek = []
    data = []
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    lp = 0
    ls = 0
    headings = ('Lp', 'Magazyn', 'Nazwa', 'Opis', 'Stan', 'Wartość')  # MAX 25 wpisów , 'Test'

    for pz in db:
        suma_calkowita += pz['suma_wart']
        lp = lp + 1
        if lp <= 30:

            ls = 1

            if pz['rodzaj'] == 'dre':
                magazyn = "DREWNA"
            else:
                if mag == 'mag3':
                    magazyn = "CHEMII"
                else:
                    magazyn = "WEWNĘTRZNY"
            nazwa = pz['nazwa']
            opis = pz['opis']
            stan = pz['i_stan']
            wartosc = pz['suma_wart']
            if pz['brak_ceny'] == 0:
                test = "" #"√"
            else:
                test = "×"

            data.append([lp, magazyn, nazwa, opis, stan, wartosc]) # , test
        else:

            ls = 2
            if lp <= 62:

                if pz['rodzaj'] == 'dre':
                    magazyn = "DREWNA"
                else:
                    if mag == 'mag3':
                        magazyn = "CHEMII"
                    else:
                        magazyn = "WEWNĘTRZNY"
                nazwa = pz['nazwa']
                opis = pz['opis']
                stan = pz['i_stan']
                wartosc = pz['suma_wart']
                if pz['brak_ceny'] == 0:
                    test = ""  # "√"
                else:
                    test = "×"

                data1.append([lp, magazyn, nazwa, opis, stan, wartosc])
            else:

                ls = 3
                if lp <= 94:

                    if pz['rodzaj'] == 'dre':
                        magazyn = "DREWNA"
                    else:
                        if mag == 'mag3':
                            magazyn = "CHEMII"
                        else:
                            magazyn = "WEWNĘTRZNY"
                    nazwa = pz['nazwa']
                    opis = pz['opis']
                    stan = pz['i_stan']
                    wartosc = pz['suma_wart']
                    if pz['brak_ceny'] == 0:
                        test = ""  # "√"
                    else:
                        test = "×"

                    data2.append([lp, magazyn, nazwa, opis, stan, wartosc])
                else:

                    ls = 4
                    if lp <= 126:

                        if pz['rodzaj'] == 'dre':
                            magazyn = "DREWNA"
                        else:
                            if mag == 'mag3':
                                magazyn = "CHEMII"
                            else:
                                magazyn = "WEWNĘTRZNY"
                        nazwa = pz['nazwa']
                        opis = pz['opis']
                        stan = pz['i_stan']
                        wartosc = pz['suma_wart']
                        if pz['brak_ceny'] == 0:
                            test = ""  # "√"
                        else:
                            test = "×"

                        data3.append([lp, magazyn, nazwa, opis, stan, wartosc])
                    else:

                        ls = 5

                        if pz['rodzaj'] == 'dre':
                            magazyn = "DREWNA"
                        else:
                            if mag == 'mag3':
                                magazyn = "CHEMII"
                            else:
                                magazyn = "WEWNĘTRZNY"
                        nazwa = pz['nazwa']
                        opis = pz['opis']
                        stan = pz['i_stan']
                        wartosc = pz['suma_wart']
                        if pz['brak_ceny'] == 0:
                            test = ""  # "√"
                        else:
                            test = "×"

                        data4.append([lp, magazyn, nazwa, opis, stan, wartosc])

    naglowek.append(['DATA', adata])
    naglowek.append(['SUMA', suma_calkowita])

    f = Table(naglowek, rowHeights=30, colWidths=[60, 100])
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 1), (1, 1), 'RIGHT'),
        ('FONT', (1, 1), (1, 1), 'Dejavu-Bold', 10),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.brown),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 660, 515)


    f = Table([headings] + data, rowHeights=16, colWidths=[20, 80, 270, 270, 60, 100]) #800
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
        ('TEXTCOLOR', (4, 1), (4, -1), colors.blue),
        ('TEXTCOLOR', (5, 1), (5, -1), colors.brown),
        ('FONT', (-2, 1), (-1, -1), 'Dejavu-Bold', 9),
    ]))
    f.wrapOn(p, 300, 300)
    if len(db) <= 30:
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


    if len(db) > 30:
        p.showPage()
        f = Table([headings] + data1, rowHeights=16, colWidths=[20, 80, 270, 270, 60, 100])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
            ('TEXTCOLOR', (4, 1), (4, -1), colors.blue),
            ('TEXTCOLOR', (5, 1), (5, -1), colors.brown),
            ('FONT', (-2, 1), (-1, -1), 'Dejavu-Bold', 9),
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


    if len(db) > 62:
        p.showPage()
        f = Table([headings] + data2, rowHeights=16, colWidths=[20, 80, 270, 270, 60, 100])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
            ('TEXTCOLOR', (4, 1), (4, -1), colors.blue),
            ('TEXTCOLOR', (5, 1), (5, -1), colors.brown),
            ('FONT', (-2, 1), (-1, -1), 'Dejavu-Bold', 9),
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



    if len(db) > 94:
        p.showPage()
        f = Table([headings] + data3, rowHeights=16, colWidths=[20, 80, 270, 270, 60, 100])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
            ('TEXTCOLOR', (4, 1), (4, -1), colors.blue),
            ('TEXTCOLOR', (5, 1), (5, -1), colors.brown),
            ('FONT', (-2, 1), (-1, -1), 'Dejavu-Bold', 9),
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


    if len(db) > 126:
        p.showPage()
        f = Table([headings] + data4, rowHeights=16, colWidths=[20, 80, 270, 270, 60, 100])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
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








