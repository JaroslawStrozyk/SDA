from django.http import HttpResponse
from reportlab.lib.colors import HexColor
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
from .models import Sklad
from django.shortcuts import redirect
import textwrap

def pdf_naglowek(p, biezaca_strona, liczba_stron, magazyn, nr_pal, nr_zlec, pnazwa, klient, targi, stoisko, pm, wys, szer, gl, pole, suma_j, suma_c, czas_od, czas_do):
    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 30, 738, width=100, height=85)

    data = [('Warehouse:', magazyn, 'Pallet no:', nr_pal, 'SDE:', nr_zlec, '', str(biezaca_strona)+'/'+str(liczba_stron))]
    f = Table(data, rowHeights=20, colWidths=[80, 70, 70, 50 , 50, 80, 3, 47])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (5, 0), 0.15, colors.gray),
        ('GRID', (7, 0), (-1, 0), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('FONT', (2, 0), (2, 0), 'Dejavu-Bold', 10),
        ('FONT', (4, 0), (4, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, 0), colors.lightgrey),
        ('BACKGROUND', (4, 0), (4, 0), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 130, 800)

    data = [
        ('Client:', klient, 'Fair:', targi),
        ('Stand:', stoisko, 'PM:', pm),
    ]
    f = Table(data, rowHeights=20, colWidths=[70, 155, 70, 155])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 10),
        ('FONT', (2, 0), (2, -1), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 130, 757)

    data = [('Object name:', pnazwa)]
    f = Table(data, rowHeights=20, colWidths=[100, 350])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (1, 0), 0.15, colors.gray),
        ('GRID', (3, 0), (-1, 0), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 130, 734)

    data = [
        ('Surface area', 'Height:', wys+' m', 'Width:', szer+' m', 'Depth:', gl+' m', 'Surface:', pole+' m²')
    ]
    f = Table(data, rowHeights=20, colWidths=[80, 55, 60, 55, 60, 55, 60, 55, 60])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('FONT', (1, 0), (1, 0), 'Dejavu-Bold', 10),
        ('FONT', (3, 0), (3, 0), 'Dejavu-Bold', 10),
        ('FONT', (5, 0), (5, 0), 'Dejavu-Bold', 10),
        ('FONT', (7, 0), (7, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, 0), colors.lightgrey),
        ('BACKGROUND', (3, 0), (3, 0), colors.lightgrey),
        ('BACKGROUND', (5, 0), (5, 0), colors.lightgrey),
        ('BACKGROUND', (7, 0), (7, 0), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 714)

    data = [
        ('Storage time', 'From:', czas_od, 'To:', czas_do),
    ]
    f = Table(data, rowHeights=20, colWidths=[140, 50, 150, 50, 150])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('FONT', (1, 0), (1, 0), 'Dejavu-Bold', 10),
        ('FONT', (3, 0), (3, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, 0), colors.lightgrey),
        ('BACKGROUND', (3, 0), (3, 0), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 691)

    data = [
        ('The cost for the selected item:', suma_j, 'Total cost for ['+nr_zlec+']:', suma_c),
    ]
    f = Table(data, rowHeights=20, colWidths=[190, 80, 190, 80])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('FONT', (1, 0), (1, 0), 'Dejavu-Bold', 10),
        ('FONT', (2, 0), (2, 0), 'Dejavu-Bold', 10),
        ('FONT', (3, 0), (3, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, 0), colors.lightgrey),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.blue),
        ('TEXTCOLOR', (3, 0), (3, 0), colors.brown),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 668)

'''
    Ilosc: 
        0 - brak zdjęć
        1 - pierwsze zdjęcie
        2 - drugie zdjęcie
        3 - oba zdjęcia
'''
def pdf_proporcja(p, ilosc, im1, im2):
    szer = 540
    wys = 550
    shift = 600

    if ilosc == 1:
        width11, height11 = im1.size
        if width11 >= height11:
            x = szer
            y = int((height11 * szer)/width11)
            p.drawInlineImage(im1, 40, shift - y, width=x, height=y)
        else:
            x = int((width11 * wys)/height11)
            y = wys
            xx = 40 + (int(szer/2) - int(x/2))
            p.drawInlineImage(im1, xx, shift - y, width=x, height=y)

    if ilosc == 2:
        width22, height22 = im2.size
        if width22 >= height22:
            x = szer
            y = int((height22 * szer)/width22)
            p.drawInlineImage(im2, 40, shift - y, width=x, height=y)
        else:
            x = int((width22 * wys)/height22)
            y = wys
            xx = 40 + (int(szer/2) - int(x/2))
            p.drawInlineImage(im2, xx, shift - y, width=x, height=y)


    if ilosc == 3:
        szer = 350
        wys = 300
        shift = 640
        width11, height11 = im1.size
        width22, height22 = im2.size

        if width11 >= height11: #poziom
            x = szer
            y = int((height11 * szer)/width11)
            p.drawInlineImage(im1, 140, shift - y, width=x, height=y)
        else:
            x = int((width11 * wys)/height11)
            y = wys
            xx = 140 + (int(szer/2) - int(x/2))
            p.drawInlineImage(im1, xx, shift - y, width=x, height=y)


        if width22 >= height22: #poziom
            x = szer
            y = int((height22 * szer)/width22)
            p.drawInlineImage(im2, 140, (shift - y)-320, width=x, height=y)
        else:
            x = int((width22 * wys)/height22)
            y = wys
            xx = 140 + (int(szer/2) - int(x/2))
            p.drawInlineImage(im2, xx, (shift - y)-320, width=x, height=y)


def pdf_zdjecia(p, zdjecie1, zdjecie2):
    im1 = ''
    im2 = ''
    ilosc = 0

    if zdjecie1 != '':
        ilosc += 1
        im1 = Image.open(os.path.join(settings.MEDIA_ROOT, str(zdjecie1)))

    if zdjecie2 != '':
        ilosc += 2
        im2 = Image.open(os.path.join(settings.MEDIA_ROOT, str(zdjecie2)))

    if ilosc != 0:
        pdf_proporcja(p, ilosc, im1, im2)



def sklad_pdf_out(request, pk, mag):
    # try:
    nr_sde = Sklad.objects.get(pk=pk).nr_sde.nazwa
    id_sde = Sklad.objects.get(pk=pk).nr_sde.pk
    skl = Sklad.objects.filter(nr_sde=id_sde).order_by('czas_od')
    liczba_stron = skl.count()

    # dokument

    response = HttpResponse(content_type='application/pdf')
    titlefile = "list_of_stored_for_" + nr_sde + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    biezaca_strona = 1
    for s in skl:
        magazyn = s.magazyn
        nr_pal  = str(s.przech_nrpalet)
        nr_zlec = s.nr_sde.nazwa
        klient  = s.nr_sde.klient
        targi   = s.nr_sde.targi
        stoisko = s.nr_sde.stoisko
        pm = s.nr_sde.pm
        pnazwa = s.przech_nazwa
        wys = str(s.przech_wys)
        szer = str(s.przech_sze)
        gl = str(s.przech_gl)
        pole = str(s.przech_pow)
        suma_j = str(s.koszt_przech)
        suma_c = str(s.suma)
        czas_od = str(s.czas_od)
        czas_do = str(s.czas_do)
        zdjecie1 = s.przech_zdjecie
        zdjecie2 = s.przech_zdjecie2

        pdf_naglowek(p, biezaca_strona, liczba_stron, magazyn, nr_pal, nr_zlec, pnazwa, klient, targi, stoisko, pm, wys, szer, gl, pole, suma_j, suma_c, czas_od, czas_do)
        pdf_zdjecia(p, zdjecie1, zdjecie2)

        biezaca_strona += 1
        p.showPage()

    p.save()
    return response



def sklad_pdf_sim_out(request, pk, mag):
    # try:
    nr_sde = Sklad.objects.get(pk=pk).nr_sde.nazwa
    id_sde = Sklad.objects.get(pk=pk).nr_sde.pk
    skl = Sklad.objects.filter(pk=pk)
    liczba_stron = skl.count()

    # dokument

    response = HttpResponse(content_type='application/pdf')
    titlefile = "list_of_stored_for_" + nr_sde + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    biezaca_strona = 1
    for s in skl:
        magazyn = s.magazyn
        nr_pal  = str(s.przech_nrpalet)
        nr_zlec = s.nr_sde.nazwa
        klient  = s.nr_sde.klient
        targi   = s.nr_sde.targi
        stoisko = s.nr_sde.stoisko
        pm = s.nr_sde.pm
        pnazwa = s.przech_nazwa
        wys = str(s.przech_wys)
        szer = str(s.przech_sze)
        gl = str(s.przech_gl)
        pole = str(s.przech_pow)
        suma_j = str(s.koszt_przech)
        suma_c = str(s.suma)
        czas_od = str(s.czas_od)
        czas_do = str(s.czas_do)
        zdjecie1 = s.przech_zdjecie
        zdjecie2 = s.przech_zdjecie2

        pdf_naglowek(p, biezaca_strona, liczba_stron, magazyn, nr_pal, nr_zlec, pnazwa, klient, targi, stoisko, pm, wys, szer, gl, pole, suma_j, suma_c, czas_od, czas_do)
        pdf_zdjecia(p, zdjecie1, zdjecie2)

        biezaca_strona += 1
        p.showPage()

    p.save()
    return response


def process_string(klient, fl=False, max_length=25):
    # Sprawdzenie długości i ustawienie flagi
    if len(klient) > max_length:
        fl = True
        # Dzielimy string na fragmenty z uwzględnieniem spacji
        klient = '\n'.join(textwrap.wrap(klient, width=max_length))
    return klient, fl


def pdf_naglowek_bc(p, biezaca_strona, liczba_stron, magazyn, nr_pal, nr_zlec, pnazwa, klient, targi, stoisko, pm, wys, szer, gl, pole, suma_j, suma_c, czas_od, czas_do):
    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sde.png'))
    p.drawInlineImage(im, 30, 738, width=100, height=85)

    data = [('Warehouse:', magazyn, 'Pallet no:', nr_pal, 'SDE:', nr_zlec, '', str(biezaca_strona)+'/'+str(liczba_stron))]
    f = Table(data, rowHeights=20, colWidths=[80, 70, 70, 50 , 50, 80, 3, 47])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (5, 0), 0.15, colors.gray),
        ('GRID', (7, 0), (-1, 0), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('FONT', (2, 0), (2, 0), 'Dejavu-Bold', 10),
        ('FONT', (4, 0), (4, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, 0), colors.lightgrey),
        ('BACKGROUND', (4, 0), (4, 0), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 130, 800)

    klient, fl = process_string(klient)

    data = [
        ('Client:', klient, 'Fair:', targi),
        ('Stand:', stoisko, 'PM:', pm),
    ]
    f = Table(data, rowHeights=20, colWidths=[70, 155, 70, 155])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 10),
        ('FONT', (2, 0), (2, -1), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
    ]))

    if fl:
        f.setStyle(TableStyle([('FONT', (1, 0), (1, 0), 'Dejavu', 8),]))

    f.wrapOn(p, 300, 300)
    f.drawOn(p, 130, 757)

    data = [('Object name:', pnazwa)]
    f = Table(data, rowHeights=20, colWidths=[100, 350])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (1, 0), 0.15, colors.gray),
        ('GRID', (3, 0), (-1, 0), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 130, 734)

    data = [
        ('Surface area', 'Height:', wys+' m', 'Width:', szer+' m', 'Depth:', gl+' m', 'Surface:', pole+' m²')
    ]
    f = Table(data, rowHeights=20, colWidths=[80, 55, 60, 55, 60, 55, 60, 55, 60])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('FONT', (1, 0), (1, 0), 'Dejavu-Bold', 10),
        ('FONT', (3, 0), (3, 0), 'Dejavu-Bold', 10),
        ('FONT', (5, 0), (5, 0), 'Dejavu-Bold', 10),
        ('FONT', (7, 0), (7, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, 0), colors.lightgrey),
        ('BACKGROUND', (3, 0), (3, 0), colors.lightgrey),
        ('BACKGROUND', (5, 0), (5, 0), colors.lightgrey),
        ('BACKGROUND', (7, 0), (7, 0), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 714)

    data = [
        ('Storage time', 'From:', czas_od, 'To:', czas_do),
    ]
    f = Table(data, rowHeights=20, colWidths=[140, 50, 150, 50, 150])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('FONT', (1, 0), (1, 0), 'Dejavu-Bold', 10),
        ('FONT', (3, 0), (3, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, 0), colors.lightgrey),
        ('BACKGROUND', (3, 0), (3, 0), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 691)

    # data = [
    #     ('The cost for the selected item:', suma_j, 'Total cost for ['+nr_zlec+']:', suma_c),
    # ]
    # f = Table(data, rowHeights=20, colWidths=[190, 80, 190, 80])
    # f.setStyle(TableStyle([
    #     ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
    #     ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
    #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    #     ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
    #     ('FONT', (1, 0), (1, 0), 'Dejavu-Bold', 10),
    #     ('FONT', (2, 0), (2, 0), 'Dejavu-Bold', 10),
    #     ('FONT', (3, 0), (3, 0), 'Dejavu-Bold', 10),
    #     ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
    #     ('BACKGROUND', (2, 0), (2, 0), colors.lightgrey),
    #     ('TEXTCOLOR', (1, 0), (1, 0), colors.blue),
    #     ('TEXTCOLOR', (3, 0), (3, 0), colors.brown),
    # ]))
    # f.wrapOn(p, 300, 300)
    # f.drawOn(p, 40, 668)


def sklad_pdf_bc_out(request, pk, mag):
    # try:
    nr_sde = Sklad.objects.get(pk=pk).nr_sde.nazwa
    id_sde = Sklad.objects.get(pk=pk).nr_sde.pk
    skl = Sklad.objects.filter(nr_sde=id_sde).order_by('czas_od')
    liczba_stron = skl.count()

    # dokument

    response = HttpResponse(content_type='application/pdf')
    titlefile = "list_of_stored_for_" + nr_sde + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    biezaca_strona = 1
    for s in skl:
        magazyn = s.magazyn
        nr_pal  = str(s.przech_nrpalet)
        nr_zlec = s.nr_sde.nazwa
        klient  = s.nr_sde.klient
        targi   = s.nr_sde.targi
        stoisko = s.nr_sde.stoisko
        pm = s.nr_sde.pm
        pnazwa = s.przech_nazwa
        wys = str(s.przech_wys)
        szer = str(s.przech_sze)
        gl = str(s.przech_gl)
        pole = str(s.przech_pow)
        suma_j = str(s.koszt_przech)
        suma_c = str(s.suma)
        czas_od = str(s.czas_od)
        czas_do = str(s.czas_do)
        zdjecie1 = s.przech_zdjecie
        zdjecie2 = s.przech_zdjecie2

        pdf_naglowek_bc(p, biezaca_strona, liczba_stron, magazyn, nr_pal, nr_zlec, pnazwa, klient, targi, stoisko, pm, wys, szer, gl, pole, suma_j, suma_c, czas_od, czas_do)
        pdf_zdjecia(p, zdjecie1, zdjecie2)

        biezaca_strona += 1
        p.showPage()

    p.save()
    return response


def ewu_pdf_bc_out(request, pk, mag, sklad, naz):

    #skl = Sklad.objects.filter(multi_uzycie=True, firma=pk).order_by('przech_nazwa')
    skl = sklad
    nazwa = naz
    liczba_stron = skl.count()

    # dokument

    response = HttpResponse(content_type='application/pdf')
    titlefile = "list_of_items_stored_for_" + nazwa + '.pdf'
    # titlefile = "list_of_items_stored_for_.pdf"
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    biezaca_strona = 1
    for s in skl:
        magazyn = s.magazyn
        nr_pal  = str(s.przech_nrpalet)
        nr_zlec = s.nr_sde.nazwa
        klient  = s.nr_sde.klient
        targi   = s.nr_sde.targi
        stoisko = s.nr_sde.stoisko
        pm = s.nr_sde.pm
        pnazwa = s.przech_nazwa
        wys = str(s.przech_wys)
        szer = str(s.przech_sze)
        gl = str(s.przech_gl)
        pole = str(s.przech_pow)
        suma_j = str(s.koszt_przech)
        suma_c = str(s.suma)
        czas_od = str(s.czas_od)
        czas_do = str(s.czas_do)
        zdjecie1 = s.przech_zdjecie
        zdjecie2 = s.przech_zdjecie2

        pdf_naglowek_bc(p, biezaca_strona, liczba_stron, magazyn, nr_pal, nr_zlec, pnazwa, klient, targi, stoisko, pm, wys, szer, gl, pole, suma_j, suma_c, czas_od, czas_do)
        pdf_zdjecia(p, zdjecie1, zdjecie2)

        biezaca_strona += 1
        p.showPage()

    p.save()
    return response

