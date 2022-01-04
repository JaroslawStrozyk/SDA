from django.http import HttpResponse
import xlwt
from .models import Zamowienie





def gen_xls(rok):
    stytul = 'Zamówienia ' + str(rok)
    fname = "Zamówienia_" + str(rok) + ".xls"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + fname + '"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(stytul)

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_sde', 'nr_mpk',
        'nr_dok1', 'zal1', 'nr_dok2', 'zal2', 'nr_dok3', 'zal3', 'kwota_netto', 'kwota_brutto', 'data_zam', 'data_dost',
        'data_fv', 'nr_fv', 'roz', 'uwagi'
    ]

    col_width = [50, 50, 20, 20, 20, 20, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100]
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()

    rows = Zamowienie.objects.filter(rok=rok).values_list('opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat',
                                                          'rodzaj_plat', 'nr_sde__nazwa', 'nr_mpk__nazwa', 'nr_dok1',
                                                          'zal1', 'nr_dok2',
                                                          'zal2', 'nr_dok3', 'zal3', 'kwota_netto', 'kwota_brutto',
                                                          'data_zam', 'data_dost', 'data_fv', 'nr_fv', 'roz', 'uwagi')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 16 or col_num == 17 or col_num == 18:
                font_style = xlwt.XFStyle()
                font_style.num_format_str = 'yyyy-mm-dd'
            else:
                font_style = xlwt.XFStyle()

            # ws.write(row_num, col_num, row[col_num], font_style)
            ws.write(row_num, col_num, row[col_num])

    wb.save(response)
    return response