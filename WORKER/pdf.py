from django.http import HttpResponse
from .models import Pensja, Premia_det
from reportlab.lib.colors import HexColor
from moneyed import Money, PLN
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






def worker_mc_pdf(request, pk):

    pen = Pensja.objects.get(pk=pk)
    osoba = pen.osoba
    rok = str(pen.rok)
    mc = str(pen.miesiac)
    rd = pen.del_rozli
    razem = pen.suma_pd

    try:
        premia = Premia_det.objects.filter(pensja=pk)
    except:
        premia = ''


    # dokument

    response = HttpResponse(content_type='application/pdf')
    titlefile = "Zestawienie miesięczne " + osoba + " " + mc + "_" + rok + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=landscape(A4)) # portrait
    p.setTitle(titlefile)
    height, width = A4
    # print("height:", height, "width:", width)

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))
    #pdfmetrics.registerFont(TTFont('Times-Italic', 'DejaVuSerif-Italic.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 40, 500, width=80, height=65)
    p.setFont("Dejavu-Bold", 17)
    p.drawString(280, 550, "ZESTAWIENIE MIESIĘCZNE " + mc + "/" + rok)

    p.setFont("Dejavu", 12)
    tytul = "Dla:"
    p.drawString(280, 520, tytul)
    p.setFont("Dejavu-Bold", 12)
    p.drawString(320, 520, osoba)

    data = [('Różnica z delegacji', rd), ]
    f = Table(data, rowHeights=20, colWidths=[150, 80])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 350, 470)

    data = [('Razem', razem), ]
    f = Table(data, rowHeights=30, colWidths=[60, 120])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 12),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.brown),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 650, 470)

    data = [('Nazwa\nprojektu', 'Wielkość\nstoiska', 'Wartość', 'Wyjazd\n[dr]', 'Wyjazd\n[SO]', 'Wyjazd\n[ND]', 'Wyjazd\nwartość', 'Premia\nprojekt', 'Premia\nindyw.','Opis'), ]
    f = Table(data, rowHeights=40, colWidths=[80, 80, 70, 50, 50, 50, 70, 70, 70, 220])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, 427)

    data = []
    licznik = 0
    for pr in premia:
        if pr.pr_wartosc == Money('0.00', PLN):
            war = ''
        else:
            war = pr.pr_wartosc
        if pr.del_ilosc_st == 0:
            st = ''
        else:
            st = pr.del_ilosc_st
        if pr.del_ilosc_so == 0:
            so = ''
        else:
            so = pr.del_ilosc_so
        if pr.del_ilosc_we == 0:
            we = ''
        else:
            we = pr.del_ilosc_we
        if pr.del_ilosc_razem == Money('0.00', PLN):
            ilr = ''
        else:
            ilr = pr.del_ilosc_razem
        if pr.premia_proj == Money('0.00', PLN):
            prp = ''
        else:
            prp = pr.premia_proj
        if pr.ind_pr_kwota == Money('0.00', PLN):
            pri = ''
        else:
            pri = pr.ind_pr_kwota

        try:
            row = (pr.projekt.nazwa , pr.pr_wielkosc, war, st, so, we, ilr, prp, pri, div_opis(pr.ind_pr_opis))
        except:
            row = ("MPK: 407-2", pr.pr_wielkosc, war, st, so, we, ilr, prp, pri, div_opis(pr.ind_pr_opis))

        licznik += 1
        data.append(row)

    if data == []:
        row = ('', '', '', '', '', '', '', '', '', '')
        data.append(row)
        rowH = 0
    else:
        rowH = 35

    f = Table(data, rowHeights=rowH, colWidths=[80, 80, 70, 50, 50, 50, 70, 70, 70, 220])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('ALIGN', (6, 0), (6, -1), 'RIGHT'),
        ('ALIGN', (7, 0), (7, -1), 'RIGHT'),
        ('ALIGN', (8, 0), (8, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, 427 - (licznik * 35))

    p.save()
    return response


def div_opis(str):
    dl = 45
    s1 = ''
    s2 = ''
    s3 = ''
    o = str.split()
    for i in o:
       if len(s1) <= dl:
          s1 += i + ' '
       else:
          if len(s2) <= dl:
             s2 += i + ' '
          else:
             if len(s3) <= dl:
                s3 += i + ' '
    s1 = s1.strip()
    if s2 != '':
       s1 += '\n' + s2.strip()
    if s3 != '':
       s1 += '\n' + s3.strip()
    return s1
