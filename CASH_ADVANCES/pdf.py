from django.http import HttpResponse
from reportlab.lib.colors import HexColor

from .models import Rozliczenie, Pozycja
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle, Paragraph, SimpleDocTemplate
from reportlab.platypus.tables import Table
from PIL import Image
from django.conf import settings
import datetime
import os


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
    return name_log, inicjaly


def cash_out_pdf_roz(request, pk):
    rozliczenie = Rozliczenie.objects.get(id=pk)
    pozycje = Pozycja.objects.filter(nr_roz=rozliczenie.id, data_zak__isnull=False).order_by('id')
    # licznik = Pozycja.objects.filter(nr_roz=rozliczenie.id, data_zak__isnull=False).count()
    name_log, inicjaly = test_osoba(request)

    wydatki = 0
    for poz in pozycje:
        wydatki = wydatki + poz.kwota_brutto

    response = HttpResponse(content_type='application/pdf')
    titlefile = "Rozliczenie_" + rozliczenie.data_zal.strftime("%Y-%m-%d") + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=landscape(A4))
    p.setTitle(titlefile)
    height, width = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, (40), (height - 100), width=100, height=85)

    p.setFont("Dejavu-Bold", 16)
    p.drawString((width / 2 - 110), (height - 60), "ROZLICZENIE ZALICZKI")
    p.setFont("Dejavu-Bold", 12)
    p.drawString((width / 2 - 50), (height - 80), rozliczenie.kw)

    data = [('Otrzymane zaliczki',)]
    f = Table(data, rowHeights=16, colWidths=170)
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, height - 113)

    if rozliczenie.data_zal == None:
        zal_d = ''
    else:
        zal_d = rozliczenie.data_zal

    if rozliczenie.data_roz != None:
        roz_d = rozliczenie.data_roz.strftime("%d-%m-%Y")
    else:
        roz_d = ''

    data = [('Data', 'Kwota'),
            (zal_d, rozliczenie.zal_kwota),
            ]
    f = Table(data, rowHeights=16, colWidths=85)
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('BACKGROUND', (1, 1), (-1, -1), colors.lightgoldenrodyellow),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 20, height - 145)
    ###
    data = [(name_log,)]
    f = Table(data, rowHeights=16, colWidths=170)
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, (width - 188), height - 81)

    ######
    saldo = rozliczenie.zal_kwota - wydatki
    data = [
        ('Rozliczenie', roz_d),
        ('Suma', rozliczenie.zal_kwota),
        ('Wydatki', wydatki),
        ('Saldo', saldo),
    ]
    f = Table(data, rowHeights=16, colWidths=85)
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (1, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, (width - 188), height - 145)

    data = [('Imię i Nazwisko',), (rozliczenie.nazwisko,)]
    f = Table(data, rowHeights=22, colWidths=180)
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 12),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, (width / 2 - 90), height - 145)

    data = []
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    lp = 0
    headings = (
    'Lp', 'Kontrahent', 'Nr Faktury', 'War. [Netto]', 'War.[Brutto]', 'Data', 'Opis', 'SDE/MPK')  # MAX 25 wpisów

    for pz in pozycje:
        lp = lp + 1
        if lp <= 25:
            sdempk = ""
            if pz.nr_sde != None:
                sdempk = pz.nr_sde.nazwa
            if pz.nr_mpk != None:
                sdempk = pz.nr_mpk.nazwa

            data.append([lp, pz.kontrahent, pz.nr_fv, pz.kwota_netto, pz.kwota_brutto, pz.data_zak.strftime('%d-%m-%Y'),
                         pz.opis, sdempk])
        else:
            if lp <= 58:
                sdempk = ""
                if pz.nr_sde != None:
                    sdempk = pz.nr_sde.nazwa
                if pz.nr_mpk != None:
                    sdempk = pz.nr_mpk.nazwa
                data1.append(
                    [lp, pz.kontrahent, pz.nr_fv, pz.kwota_netto, pz.kwota_brutto, pz.data_zak.strftime('%d-%m-%Y'),
                     pz.opis, sdempk])
            else:
                if lp <= 91:
                    sdempk = ""
                    if pz.nr_sde != None:
                        sdempk = pz.nr_sde.nazwa
                    if pz.nr_mpk != None:
                        sdempk = pz.nr_mpk.nazwa
                    data2.append(
                        [lp, pz.kontrahent, pz.nr_fv, pz.kwota_netto, pz.kwota_brutto, pz.data_zak.strftime('%d-%m-%Y'),
                         pz.opis, sdempk])
                else:
                    if lp <= 124:
                        sdempk = ""
                        if pz.nr_sde != None:
                            sdempk = pz.nr_sde.nazwa
                        if pz.nr_mpk != None:
                            sdempk = pz.nr_mpk.nazwa
                        data3.append([lp, pz.kontrahent, pz.nr_fv, pz.kwota_netto, pz.kwota_brutto,
                                      pz.data_zak.strftime('%d-%m-%Y'), pz.opis, sdempk])
                    else:
                        sdempk = ""
                        if pz.nr_sde != None:
                            sdempk = pz.nr_sde.nazwa
                        if pz.nr_mpk != None:
                            sdempk = pz.nr_mpk.nazwa
                        data4.append([lp, pz.kontrahent, pz.nr_fv, pz.kwota_netto, pz.kwota_brutto,
                                      pz.data_zak.strftime('%d-%m-%Y'), pz.opis, sdempk])

    f = Table([headings] + data, rowHeights=16, colWidths=[20, 190, 115, 80, 80, 60, 180, 80])
    f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
        ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
    ]))
    f.wrapOn(p, 300, 300)
    if len(pozycje) <= 25:
        shift = height - (180 + (16 * lp))
        f.drawOn(p, 20, shift)

    else:
        f.drawOn(p, 20, 16)

    if len(pozycje) > 25:
        p.showPage()
        f = Table([headings] + data1, rowHeights=16, colWidths=[20, 190, 115, 80, 80, 60, 180, 80])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
        ]))
        f.wrapOn(p, 300, 300)
        shift = height - (464 + (16 * (len(data1) - 26)))  # lp
        print(shift)
        f.drawOn(p, 20, shift)

    if len(pozycje) > 58:
        p.showPage()
        f = Table([headings] + data2, rowHeights=16, colWidths=[20, 190, 115, 80, 80, 60, 180, 80])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
        ]))
        f.wrapOn(p, 300, 300)
        shift = height - (464 + (16 * (len(data2) - 26)))
        f.drawOn(p, 20, shift)

    if len(pozycje) > 91:
        p.showPage()
        f = Table([headings] + data3, rowHeights=16, colWidths=[20, 190, 115, 80, 80, 60, 180, 80])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
        ]))
        f.wrapOn(p, 300, 300)
        shift = height - (464 + (16 * (len(data3) - 26)))
        f.drawOn(p, 20, shift)

    if len(pozycje) > 124:
        p.showPage()
        f = Table([headings] + data4, rowHeights=16, colWidths=[20, 190, 115, 80, 80, 60, 180, 80])
        f.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
        ]))
        f.wrapOn(p, 300, 300)
        shift = height - (464 + (16 * (len(data4) - 26)))
        f.drawOn(p, 20, shift)

    p.showPage()
    p.save()
    return response
