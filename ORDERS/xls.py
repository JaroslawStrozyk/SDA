from django.http import HttpResponse
import xlwt
from .models import Zamowienie
import datetime
import csv



def gen_xls(rok):
    stytul = 'Zamówienia ' + str(rok)
    fname = "Zamówienia_" + str(rok) + ".xls"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + fname + '"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(stytul)
    ws.row(0).height = 256 * 3

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.font.italic = True
    font_style.font.colour_index = 4
    a = xlwt.Alignment()
    font_style.alignment.horz = a.HORZ_CENTER
    font_style.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    font_style.borders = borders


    columns = [
        'Opis', 'Kontrahent', 'Wartość zamówienia', 'Nr zamówienia', 'Sposób płatności', 'Rodzaj płatności', 'Nr sde', 'Nr mpk',
        'Nr dokumentu 1', 'Zaliczka 1', 'Nr dokumentu 2', 'Zaliczka 2', 'Nr dokumentu 3', 'Zaliczka 3', 'Kwota netto', 'Kwota brutto',
        'Data zamówienia', 'Data dostawy', 'Data FV', 'Nr FV', 'rozliczono', 'Uwagi'
    ]

    col_width = [50, 50, 20, 20, 20, 20, 20, 20, 50, 20, 50, 20, 50, 20, 30, 30, 20, 20, 20, 50, 20, 100]
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = Zamowienie.objects.filter(rok=rok)

    # OPIS
    style1 = xlwt.XFStyle() # 2 - czerwony; 4- niebieski; 8 -czarny; 11 - zielony
    font = xlwt.Font()
    font.bold = False
    font.colour_index = 8
    style1.font = font
    a = xlwt.Alignment()
    style1.alignment.horz = a.HORZ_CENTER
    style1.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    style1.borders = borders

    # WALUTA
    style2 = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = False
    font.colour_index = 2
    style2.font = font
    a = xlwt.Alignment()
    style2.alignment.horz = a.HORZ_RIGHT
    style2.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    style2.borders = borders

    # ROZLICZONO
    style3 = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = False
    font.colour_index = 4
    style3.font = font
    a = xlwt.Alignment()
    style3.alignment.horz = a.HORZ_CENTER
    style3.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    style3.borders = borders

    for row in rows:
        row_num += 1
        ws.row(row_num).height = 256 * 2
        ws.write(row_num, 0, row.opis, style=style1)
        ws.write(row_num, 1, row.kontrahent, style=style1)
        ws.write(row_num, 2, str(row.wartosc_zam), style=style2)
        ws.write(row_num, 3, row.nr_zam, style=style1)
        ws.write(row_num, 4, row.sposob_plat, style=style1)
        ws.write(row_num, 5, row.rodzaj_plat, style=style1)
        r = str(row.nr_sde)
        r = r.split('.')[0]
        if r == 'None':
            r = ""
        ws.write(row_num, 6, str(r), style=style1)
        r = str(row.nr_mpk)
        r = r.split('.')[0]
        if r == 'None':
            r = ""
        ws.write(row_num, 7, str(r), style=style1)
        ws.write(row_num, 8, row.nr_dok1, style=style1)
        ws.write(row_num, 9, str(row.zal1), style=style2)
        ws.write(row_num, 10, row.nr_dok2, style=style1)
        ws.write(row_num, 11, str(row.zal2), style=style2)
        ws.write(row_num, 12, row.nr_dok3, style=style1)
        ws.write(row_num, 13, str(row.zal3), style=style2)
        ws.write(row_num, 14, str(row.kwota_netto), style=style2)
        ws.write(row_num, 15, str(row.kwota_brutto), style=style2)
        d = row.data_zam
        if d != None:
            d = d.strftime('%Y-%m-%d')
        else:
            d = ''
        ws.write(row_num, 16, d, style=style1)
        d = row.data_dost
        if d != None:
            d = d.strftime('%Y-%m-%d')
        else:
            d = ''
        ws.write(row_num, 17, d, style=style1)
        d = row.data_fv
        if d != None:
            d = d.strftime('%Y-%m-%d')
        else:
            d = ''
        ws.write(row_num, 18, d, style=style1)
        ws.write(row_num, 19, row.nr_fv, style=style1)
        ro = row.roz
        if ro == True:
            ro = "TAK"
        else:
            ro = "NIE"
        ws.write(row_num, 20, ro, style=style3)
        ws.write(row_num, 21, row.uwagi, style=style1)

    wb.save(response)
    return response


def out_xls_sde(request, sde, tytul):

    fname = str(tytul) + ".xls"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + fname + '"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(tytul)
    ws.row(0).height = 256 * 3

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.font.italic = True
    font_style.font.colour_index = 2
    a = xlwt.Alignment()
    font_style.alignment.horz = a.HORZ_CENTER
    font_style.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    font_style.borders = borders

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 22
    font_style.pattern = pattern

    # Ustawienie obramowania
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    # Kolor obramowania - czarny
    borders.left_colour = 0
    borders.right_colour = 0
    borders.top_colour = 0
    borders.bottom_colour = 0

    font_style.borders = borders


    columns = [
        'Nr zlecenia', 'Klient', 'Targi', 'Stoisko', 'Opis', 'miesiąc', 'rok',
        'PM', 'Pow. stoiska', 'Pow. piętra'
    ]

    col_width = [20, 50, 50, 50, 80, 20, 20, 30, 20, 20]
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num].upper(), font_style)

    rows = sde

    # # OPIS
    style1 = xlwt.XFStyle() # 2 - czerwony; 4- niebieski; 8 -czarny; 11 - zielony
    font = xlwt.Font()
    font.bold = False
    font.colour_index = 8
    style1.font = font
    a = xlwt.Alignment()
    style1.alignment.horz = a.HORZ_CENTER
    style1.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    borders.left_colour = 0
    borders.right_colour = 0
    borders.top_colour = 0
    borders.bottom_colour = 0
    style1.borders = borders

    for row in rows:
        row_num += 1
        ws.row(row_num).height = 256 * 2
        ws.write(row_num, 0, row.nazwa, style=style1)
        ws.write(row_num, 1, row.klient, style=style1)
        ws.write(row_num, 2, row.targi, style=style1)
        ws.write(row_num, 3, row.stoisko, style=style1)
        ws.write(row_num, 4, row.opis, style=style1)
        ws.write(row_num, 5, row.mcs, style=style1)
        ws.write(row_num, 6, row.rks, style=style1)
        ws.write(row_num, 7, row.pm, style=style1)
        ws.write(row_num, 8, row.pow_stoisko, style=style1)
        ws.write(row_num, 9, row.pow_pietra, style=style1)

    wb.save(response)
    return response



def out_xls_ord(request, zamowienia, tytul, t):

    fname = str(tytul) + ".xls"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + fname + '"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(t[1:])
    ws.row(0).height = 256 * 3

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.font.italic = True
    font_style.font.colour_index = 4
    a = xlwt.Alignment()
    font_style.alignment.horz = a.HORZ_CENTER
    font_style.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    font_style.borders = borders


    columns = [
        'Opis', 'Kontrahent', 'Wartość zamówienia', 'Nr zamówienia', 'Sposób płatności', 'Rodzaj płatności', 'Nr sde',
        'Nr mpk', 'Nr dokumentu 1', 'Zaliczka 1', 'Nr dokumentu 2', 'Zaliczka 2', 'Nr dokumentu 3', 'Zaliczka 3',
        'Kwota netto', 'Kwota brutto', 'Data zamówienia', 'Data dostawy', 'Data FV', 'Nr FV', 'rozliczono', 'Uwagi'
    ]

    col_width = [50, 50, 20, 20, 20, 20, 20, 20, 50, 20, 50, 20, 50, 20, 30, 30, 20, 20, 20, 50, 20, 100]
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = zamowienia # Zamowienie.objects.filter(rok=rok)

    # OPIS
    style1 = xlwt.XFStyle() # 2 - czerwony; 4- niebieski; 8 -czarny; 11 - zielony
    font = xlwt.Font()
    font.bold = False
    font.colour_index = 8
    style1.font = font
    a = xlwt.Alignment()
    style1.alignment.horz = a.HORZ_CENTER
    style1.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    style1.borders = borders

    # WALUTA
    style2 = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = False
    font.colour_index = 2
    style2.font = font
    a = xlwt.Alignment()
    style2.alignment.horz = a.HORZ_RIGHT
    style2.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    style2.borders = borders

    # ROZLICZONO
    style3 = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = False
    font.colour_index = 4
    style3.font = font
    a = xlwt.Alignment()
    style3.alignment.horz = a.HORZ_CENTER
    style3.alignment.vert = a.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = borders.THIN
    borders.right = borders.THIN
    borders.top = borders.THIN
    borders.bottom = borders.THIN
    style3.borders = borders

    for row in rows:
        row_num += 1
        ws.row(row_num).height = 256 * 2
        ws.write(row_num, 0, row.opis, style=style1)
        ws.write(row_num, 1, row.kontrahent, style=style1)
        ws.write(row_num, 2, str(row.wartosc_zam), style=style2)
        ws.write(row_num, 3, row.nr_zam, style=style1)
        ws.write(row_num, 4, row.sposob_plat, style=style1)
        ws.write(row_num, 5, row.rodzaj_plat, style=style1)
        r = str(row.nr_sde)
        r = r.split('.')[0]
        if r == 'None':
            r = ""
        ws.write(row_num, 6, str(r), style=style1)
        r = str(row.nr_mpk)
        r = r.split('.')[0]
        if r == 'None':
            r = ""
        ws.write(row_num, 7, str(r), style=style1)
        ws.write(row_num, 8, row.nr_dok1, style=style1)
        ws.write(row_num, 9, str(row.zal1), style=style2)
        ws.write(row_num, 10, row.nr_dok2, style=style1)
        ws.write(row_num, 11, str(row.zal2), style=style2)
        ws.write(row_num, 12, row.nr_dok3, style=style1)
        ws.write(row_num, 13, str(row.zal3), style=style2)
        ws.write(row_num, 14, str(row.kwota_netto), style=style2)
        ws.write(row_num, 15, str(row.kwota_brutto), style=style2)
        d = row.data_zam
        if d != None:
            d = d.strftime('%Y-%m-%d')
        else:
            d = ''
        ws.write(row_num, 16, d, style=style1)
        d = row.data_dost
        if d != None:
            d = d.strftime('%Y-%m-%d')
        else:
            d = ''
        ws.write(row_num, 17, d, style=style1)
        d = row.data_fv
        if d != None:
            d = d.strftime('%Y-%m-%d')
        else:
            d = ''
        ws.write(row_num, 18, d, style=style1)
        ws.write(row_num, 19, row.nr_fv, style=style1)
        ro = row.roz
        if ro == True:
            ro = "TAK"
        else:
            ro = "NIE"
        ws.write(row_num, 20, ro, style=style3)
        ws.write(row_num, 21, row.uwagi, style=style1)

    wb.save(response)
    return response


def out_csv_ord(request, zamowienia, tytul, t):
    fname = str(tytul) + ".csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + fname + '"'

    writer = csv.writer(response)
    head = [
        'Opis', 'Kontrahent', 'Wartość zamówienia', 'Nr zamówienia', 'Sposób płatności', 'Rodzaj płatności', 'Nr sde',
        'Nr mpk', 'Nr dokumentu 1', 'Zaliczka 1', 'Nr dokumentu 2', 'Zaliczka 2', 'Nr dokumentu 3', 'Zaliczka 3',
        'Kwota netto', 'Kwota brutto', 'Data zamówienia', 'Data dostawy', 'Data FV', 'Nr FV', 'rozliczono', 'Uwagi'
    ]
    writer.writerow(head)

    for row in zamowienia:

        r1 = str(row.nr_sde)
        r1 = r1.split('.')[0]
        if r1 == 'None':
            r1 = ""

        r2 = str(row.nr_mpk)
        r2 = r2.split('.')[0]
        if r2 == 'None':
            r2 = ""

        d1 = row.data_zam
        if d1 != None:
            d1 = d1.strftime('%Y-%m-%d')
        else:
            d1 = ''

        d2 = row.data_dost
        if d2 != None:
            d2 = d2.strftime('%Y-%m-%d')
        else:
            d2 = ''

        d3 = row.data_fv
        if d3 != None:
            d3 = d3.strftime('%Y-%m-%d')
        else:
            d3 = ''

        ro = row.roz
        if ro == True:
            ro = "TAK"
        else:
            ro = "NIE"

        ro = [
            row.opis, row.kontrahent, str(row.wartosc_zam), row.nr_zam, row.sposob_plat, row.rodzaj_plat, r1, r2,
            row.nr_dok1, str(row.zal1), row.nr_dok2, str(row.zal2), row.nr_dok3, str(row.zal3), str(row.kwota_netto),
            str(row.kwota_brutto), d1, d2, d3, row.nr_fv, ro, row.uwagi
        ]

        writer.writerow(ro)



    return response