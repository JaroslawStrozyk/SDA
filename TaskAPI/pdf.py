from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
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

pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

pdfmetrics.registerFont(TTFont('Calibri', os.path.join(settings.STATIC_ROOT, 'fonts/calibri.ttf')))
pdfmetrics.registerFont(TTFont('Calibri-Bold', os.path.join(settings.STATIC_ROOT, 'fonts/calibrib.ttf')))
pdfmetrics.registerFont(TTFont('Calibri-Italic', os.path.join(settings.STATIC_ROOT, 'fonts/calibrii.ttf')))


def out_pdf_doc(request, nazwa,  mid, iin, pesel, mc, kw, fl):

    adata = datetime.now().strftime('%Y-%m-%d')

    # PDF
    response = HttpResponse(content_type='application/pdf')
    titlefile = nazwa + ' ' + adata + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4)) #landscape(A4))
    p.setTitle(titlefile)
    width, height = A4

    # NAGŁÓWEK
    data = [
        ('', 'SMART DESIGN EXPO Sp. z o.o.'),
        ('', 'ul. Szparagowa 12'),
        ('', '62-081 Wysogotowo'),
        ('', 'office@smartdesign-expo.com'),
        ('', 'smartdesign-expo.com')
    ]
    f = Table(data, rowHeights=13, colWidths=[280, 260])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('FONT', (0, 0), (-1, -1), 'Calibri', 11),
        ('FONT', (0, 0), (-1, 0), 'Calibri-Bold', 11),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.grey),
        ('LINEBELOW', (0, 4), (-1, 4), 0.15, colors.grey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, height - 90)

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sde.png'))
    p.drawInlineImage(im, (21), (height - 89), width=80, height=68) #100, 85

    # MIEJSCOWOŚĆ, DATA, IMIĘ I NAZWISKO
    data = [
        ('', '', 'miejscowość, data'),
        ('', '', mid),
        ('', '', ''),
        (iin, '', ''),
        ('Imię i Nazwisko', '', '')
    ]
    f = Table(data, rowHeights=17, colWidths=[220, 80, 220])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('BACKGROUND', (2, 1), (2, 1), colors.lightgrey),
        ('BACKGROUND', (0, 3), (0, 3), colors.lightgrey),
        ('LINEBELOW', (2, 1), (2, 1), 0.30, colors.darkgrey),
        ('LINEBELOW', (0, 3), (0, 3), 0.30, colors.darkgrey),
        ('FONT', (0, 0), (-1, -1), 'Calibri', 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('ALIGN', (0, 4), (0, 4), 'CENTER'),
        ('TEXTCOLOR', (2, 1), (2, 1), colors.black),
        ('TEXTCOLOR', (0, 3), (0, 3), colors.black),
        ('FONT', (2, 1), (2, 1), 'Calibri-Bold', 12),
        ('ALIGN', (2, 1), (2, 1), 'CENTER'),
        ('FONT', (0, 3), (0, 3), 'Calibri-Bold', 12),
        ('ALIGN', (0, 3), (0, 3), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, height - 200)

    # PESEL
    data = [
        [pesel[0], pesel[1], pesel[2], pesel[3], pesel[4], pesel[5], pesel[6], pesel[7], pesel[8], pesel[9], pesel[10]],
        ['PESEL']
    ]
    f = Table(data, rowHeights=[17, 17], colWidths=[20]*11)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, 0), 0.15, colors.grey),
        ('SPAN', (0, 1), (-1, 1)),
        ('FONT', (0, 0), (-1, -1), 'Calibri', 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
        ('ALIGN', (0, 1), (0, 1), 'CENTER'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONT', (0, 0), (-1, 0), 'Calibri-Bold', 12),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, height - 240)

    #TYTUŁ
    data = [
        ['Oświadczenie o wyrażeniu zgody'],
        ['na dokonywanie potrąceń z wynagrodzenia'],
        ['(art. 91 ustawy z dnia 26 czerwca 1974r. Kodeks pracy)']
    ]
    f = Table(data, rowHeights=[20, 20, 17], colWidths=520)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('SPAN', (0, 1), (-1, 1)),
        ('FONT', (0, 0), (-1, -1), 'Calibri', 18),
        ('FONT', (0, 2), (0, 2), 'Calibri', 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, height - 360)

    data = [
        ['Wyrażam zgodę na potrącenia z mojego wynagrodzenia należności z tytułu składek na ubezpieczenie'],
        ['grupowe, '],
        ['zgodnie z zawartą  polisą - POLISA GRUPOWEGO UBEZPIECZENIA NA ŻYCIE - OCHRONA Z PLUSEM'],
        ['NR 50209259 UNIQA']
    ]
    f = Table(data, rowHeights=17, colWidths=520)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('SPAN', (0, 1), (-1, 1)),
        ('FONT', (0, 0), (-1, -1), 'Calibri', 12),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, height - 480)

    # OD M_C,KWOTA
    data = [
        ['począwszy od miesiąca', mc],
        [' ', ' '],
        ['w kwocie', kw]
    ]
    f = Table(data, rowHeights=17, colWidths=[140, 220])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('FONT', (0, 0), (-1, -1), 'Calibri', 12),
        ('BACKGROUND', (1, 0), (1, 0), colors.lightgrey),
        ('LINEBELOW', (1, 0), (1, 0), 0.30, colors.darkgrey),
        ('BACKGROUND', (1, 2), (1, 2), colors.lightgrey),
        ('LINEBELOW', (1, 2), (1, 2), 0.30, colors.darkgrey),
        ('FONT', (1, 0), (1, -1), 'Calibri-Bold', 12),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, height - 600)

    # PODPIS
    data = [
        ['.......................................................................................'],
        ['podpis pracownika']
    ]
    f = Table(data, rowHeights=[17, 10], colWidths=200)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, 0), 0.15, colors.white),
        ('SPAN', (0, 1), (-1, 1)),
        ('FONT', (0, 0), (-1, -1), 'Calibri', 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 350, height - 700)

    data = [
        ['DISCOVER SMART DESIGN STYLE'],
        ['NUMER KRS: 0000402898. SĄD REJONOWY POZNAŃ NOWE MIASTO I WILDA W POZNANIU, VIII WYDZIAŁ GOSPODARCZY KRAJOWEGO REJESTRU SĄDOWEGO'],
        ['NIP 7811875078, REGON 301976834, BDO 000177124, WYSOKOŚĆ KAPITAŁU ZAKŁADOWEGO: 667 650,00 PLN']
    ]
    f = Table(data, rowHeights=[15, 10, 10], colWidths=520)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, 0), 0.15, colors.white),
        ('SPAN', (0, 1), (-1, 1)),
        ('FONT', (0, 0), (-1, -1), 'Calibri', 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LINEABOVE', (0, 0), (0, 0), 0.30, colors.darkgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, height - 800)

    p.showPage()
    p.save()
    return response