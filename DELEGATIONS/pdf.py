from django.http import HttpResponse
from .models import Delegacja, Pozycja
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





def delegacja_pdf_pw(request, pk):
    delegacja = Delegacja.objects.get(id=pk)

    response = HttpResponse(content_type='application/pdf')
    titlefile = "Polecenie wyjazdu " +delegacja.osoba.naz_imie + " "+ delegacja.data_od.strftime("%Y-%m-%d") + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    height, width = A4
    #print("height:", height, "width:", width)

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))
    #pdfmetrics.registerFont(TTFont('Times-Italic', 'DejaVuSerif-Italic.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, (40), (730), width=100, height=85)

    p.setFont("Dejavu-Bold", 11)
    p.drawString(45, 720, "POLECENIE WYJAZDU SŁUŻBOWEGO: "+ str(delegacja.numer))


    data = [('','\nSTWIERDZENIE POBYTU SŁUŻBOWEGO')]
    f = Table(data, rowHeights=70, colWidths=[320,200])
    f.setStyle(TableStyle([
        # ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, 0), 'Dejavu', 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0,0), (-1, -1), 'TOP')
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 741)

    p.setFont("Dejavu", 8)
    p.drawString(365, 770, "(podać daty przybycia i wyjazdu oraz liczbę")
    p.drawString(365, 760, "noclegów bezpłatnych lub tańszych niż ryczałt).")
    p.drawString(365, 750, "Adnotacje te zaopatrzyć pieczęcią i podpisem.")

    data = [('','')]
    f = Table(data, rowHeights=210, colWidths=[320,200])
    f.setStyle(TableStyle([
        # ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, 0), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0,0), (-1, -1), 'TOP')
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 531)

    data = [('Z DNIA: ',    delegacja.dataz.strftime("%Y-%m-%d")),
            ('DLA: ',       delegacja.osoba.naz_imie),
            ('DO: ',        delegacja.targi),
            ('KRAJ: ',      delegacja.lok_targi),
            ('NA CZAS: ',   delegacja.data_od.strftime("%Y-%m-%d")+" - "+delegacja.data_do.strftime("%Y-%m-%d")),
            ('W CELU: ',    delegacja.cel_wyj),
            ('TRANSPORT: ', delegacja.transport)
            ]
    f = Table(data, rowHeights=16, colWidths=[85, 220])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (1, 0), (1, -1), 'Dejavu-Bold', 10),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.brown),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('VALIGN', (0,0), (-1, -1), 'MIDDLE')
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 42, 595)

    data = [
        ('..............................................', '..............................................'),
        ('data', 'podpis zlecającego wyjazd')
    ]
    f = Table(data, rowHeights=16, colWidths=155)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10)
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 45, 540)


    p.setFont("Dejavu", 10)
    p.drawString(45, 500, "Kwituję odbiór zaliczek na poczet kosztów wyjazdu i zobowiązuję rozliczyc się z nich w terminie")
    p.drawString(45, 484, "14 dni po zakończonej podróży upoważniając jednocześnie pracodawcę do potrącenia kwoty ")
    p.drawString(45, 468, "nierozliczonej zaliczki z najbliższej wypłaty wynagrodzenia.")


    data = [
        ('')
    ]
    f = Table(data, rowHeights=64, colWidths=520)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 456)


    data = [
        ('Kwoty zaliczki:',)
    ]
    f = Table(data, rowHeights=32, colWidths=520)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 410)


    data = [
        ('PLN', 'EURO', 'FUNTY', 'DOLARY', 'FRANK', 'KARTA'),
        (delegacja.kasa_pln, delegacja.kasa_euro, delegacja.kasa_funt, delegacja.kasa_dolar, delegacja.kasa_inna, delegacja.kasa_karta)
    ]
    f = Table(data, rowHeights=32, colWidths=87)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.brown),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 39, 346)

    data = [
        ('',)
    ]
    f = Table(data, rowHeights=64, colWidths=520)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 282)

    data = [
        ('..............................................', '..............................................'),
        ('data', 'podpis delegowanego')
    ]
    f = Table(data, rowHeights=16, colWidths=155)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10)
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 240, 288)

    data = [
        ('',)
    ]
    f = Table(data, rowHeights=64, colWidths=520)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 218)

    data = [
        ('..............................................', '..............................................'),
        ('data', 'podpis zatwierdzającego')
    ]
    f = Table(data, rowHeights=16, colWidths=155)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10)
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 240, 224)

    data = [
        ('',)
    ]
    f = Table(data, rowHeights=164, colWidths=520)
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.15, colors.gray),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 40)

    p.setFont("Dejavu", 10)
    p.drawString(45, 190, "Uwagi i adnotacje:")


    p.showPage()
    p.save()
    return response


def delegacja_pdf_out(request, pk):

    delegacja = Delegacja.objects.get(id=pk)
    pozycje1 = Pozycja.objects.filter(delegacja=pk, waluta='PLN')
    pozycje2 = Pozycja.objects.filter(delegacja=pk, waluta='EUR')
    pozycje3 = Pozycja.objects.filter(delegacja=pk, waluta='GBP')
    pozycje4 = Pozycja.objects.filter(delegacja=pk, waluta='USD')
    pozycje5 = Pozycja.objects.filter(delegacja=pk, waluta='CHF')

    if delegacja.lok_targi != 'Polska':
        fl = True
    else:
        fl = False

    nazwisko_imie =  delegacja.osoba.naz_imie
    data_od = delegacja.data_od.strftime("%Y-%m-%d")
    nr_dok = str(delegacja.numer)
    data_rozliczenia = delegacja.data_rozl.strftime("%Y-%m-%d")
    lok_kraj = delegacja.lok_targi
    dc_rozpo = delegacja.dc_rozpo.strftime("%Y-%m-%d %H:%M")
    dc_zakon = delegacja.dc_zakon.strftime("%Y-%m-%d %H:%M")
    if fl:
        przekr_gran = delegacja.przekr_gran.strftime("%Y-%m-%d %H:%M")
        powrot_krak = delegacja.powrot_kraj.strftime("%Y-%m-%d %H:%M")
    else:
        przekr_gran = ''
        powrot_krak = ''
    miej_doc = delegacja.targi
    cel_wyj = delegacja.cel_wyj
    transport = delegacja.transport
    del_opis = delegacja.czas_opis
    g_euro = delegacja.kasa_euro
    g_funt = delegacja.kasa_funt
    g_dolar = delegacja.kasa_dolar
    g_zloty = str(delegacja.kasa_pln)
    g_frank = delegacja.kasa_inna
    if fl:
        dieta_zagr = "("+str(delegacja.dieta_za_zl)+") "+str(delegacja.dieta_za)
    else:
        dieta_zagr = ''

    if fl:
        dieta_kr = ''  # 15zł
    else:
        dieta_kr = delegacja.dieta_kr

    nocleg_ilosc = str(delegacja.nocleg_ilosc_za)+"/"+str(delegacja.nocleg_ilosc_kr)
    nocleg_kr    = delegacja.nocleg_kr
    if fl:
        nocleg_zagr  = "("+str(delegacja.nocleg_za_zl)+") "+str(delegacja.nocleg_za)
    else:
        nocleg_zagr = ''
    sniadanie = delegacja.sniadanie
    obiad = delegacja.obiad
    kolacja = delegacja.kolacja
    sam_pr_kr = delegacja.prv_paliwo_kr
    sam_pr_za = ''
    sam_sl_kr = '' # delegacja.koszt_paliwo_kr
    if fl:
        sam_sl_za = delegacja.dane_auta # "("+str(delegacja.koszt_paliwo_za_pl)+") "+str(delegacja.koszt_paliwo_za)
    else:
        sam_sl_za = delegacja.dane_auta

    if fl:
        laczne_koszty_val = delegacja.lacznie_koszty_wal
        pobr_zal_val = delegacja.pobr_zal_wal
        suma_val = delegacja.suma_koniec
    else:
        laczne_koszty_val = ''
        pobr_zal_val = ''
        suma_val = ''
    laczne_koszty_pl = delegacja.lacznie_koszty_pln
    pobr_zal_pl = delegacja.pobr_zal_pln
    suma_pl = delegacja.suma_koniec_pl

    if fl:
        przeliczenie1 = str(delegacja.kursz)+" ["+str(delegacja.kurs_dataz)+"]"
    else:
        przeliczenie1 = ''

    if fl:
        przeliczenie2 = str(delegacja.kurs)+" ["+str(delegacja.kurs_data)+"]"
    else:
        przeliczenie2 = ''



    # Sekcja podsumowanie
    d_k = delegacja.dieta_kr
    dz_2 = delegacja.dieta_za_2
    dz_3 = delegacja.dieta_za_3
    dz_4 = delegacja.dieta_za_4
    dz_5 = delegacja.dieta_za_5
    wyd1 = delegacja.sum_wydatki1
    wyd2 = delegacja.sum_wydatki2
    wyd3 = delegacja.sum_wydatki3
    wyd4 = delegacja.sum_wydatki4
    wyd5 = delegacja.sum_wydatki5
    pod1 = delegacja.podsumowanie1
    pod2 = delegacja.podsumowanie2
    pod3 = delegacja.podsumowanie3
    pod4 = delegacja.podsumowanie4
    pod5 = delegacja.podsumowanie5
    da_z = delegacja.kurs_dataz
    da_r = delegacja.kurs_data
    kuz2 = delegacja.kursz2
    kuz3 = delegacja.kursz3
    kuz4 = delegacja.kursz4
    kuz5 = delegacja.kursz5
    ku2 = delegacja.kurs2
    ku3 = delegacja.kurs3
    ku4 = delegacja.kurs4
    ku5 = delegacja.kurs5
    zal1 = delegacja.zaliczka1
    zal2 = delegacja.zaliczka2
    zal3 = delegacja.zaliczka3
    zal4 = delegacja.zaliczka4
    zal5 = delegacja.zaliczka5
    wd1 = delegacja.wd1
    wd2 = delegacja.wd2
    wd3 = delegacja.wd3
    wd4 = delegacja.wd4
    wd5 = delegacja.wd5
    sum0 = delegacja.suma0
    sum1 = delegacja.suma1
    sum2 = delegacja.suma2
    sum3 = delegacja.suma3
    sum4 = delegacja.suma4
    sum5 = delegacja.suma5


    try:
        sde1 = delegacja.kod_sde_targi1.nazwa
    except:
        sde1 = ''

    try:
        sde2 = delegacja.kod_sde_targi2.nazwa
    except:
        sde2 = ''



    # dokument

    response = HttpResponse(content_type='application/pdf')
    titlefile = "Rozliczenie wyjazdu " + nazwisko_imie + " "+ data_od + '.pdf'
    namefile = 'filename="' + titlefile + '"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.setTitle(titlefile)
    height, width = A4
    # print("height:", height, "width:", width)

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))
    #pdfmetrics.registerFont(TTFont('Times-Italic', 'DejaVuSerif-Italic.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 20, 760, width=80, height=65)
    p.setFont("Dejavu-Bold", 16)
    p.drawString(100, 800, "ROZLICZENIE WYJAZDU SŁUŻBOWEGO: " + nr_dok)
    p.setFont("Dejavu", 10)

    if fl:
        tytul = "Delegacja zagraniczna z dnia:"
    else:
        tytul = "Delegacja krajowa z dnia:"

    p.drawString(100, 770, tytul)
    p.drawString(390, 770, "Rozliczona dnia:")
    p.setFont("Dejavu-Bold", 10)
    p.drawString(255, 770, data_od)
    p.drawString(475, 770, data_rozliczenia)


    data = [
        ('Osoba:',nazwisko_imie,'Miejsce Rozpoczęcia:','Firma'),
        ('Data/Czas rozpoczęcia:',dc_rozpo,'Data/Czas zakończenia:',dc_zakon),
        ('Przekr. granicy:', przekr_gran,'Powrót do Kraju:', powrot_krak),
            ]
    f = Table(data, rowHeights=20, colWidths=[133,132,133,132])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (1, 0), (1, -1), 'Dejavu-Bold', 10),
        ('FONT', (3, 0), (3, -1), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('VALIGN', (0,0), (-1, -1), 'TOP')
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 680)

    data = [
        ('Kraj:',lok_kraj, 'Miejsce doce.:', miej_doc),
        ('Cel:', cel_wyj, 'Transport:', transport),
            ]
    f = Table(data, rowHeights=20, colWidths=[40,210,80,200])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (1, 0), (1, -1), 'Dejavu-Bold', 10),
        ('FONT', (3, 0), (3, -1), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('VALIGN', (0,0), (-1, -1), 'TOP'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 640)

    data = [('SDE 1', sde1, 'SDE 2',sde2)]
    f = Table(data, rowHeights=20, colWidths=[40,225,40,225])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (1, 0), (1, 0), 'Dejavu-Bold', 10),
        ('FONT', (3, 0), (3, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, 0), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 617)



    data = [(del_opis,'')]
    f = Table(data, rowHeights=20, colWidths=[530,0])
    f.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.gray),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0,0), (-1, -1), 'MIDDLE')
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 596)


    data = [
        ('','','MIEDZYNARODOWE', '', 'KRAJ'),
            ]
    f = Table(data, rowHeights=20, colWidths=[204, 3, 240, 3, 80])
    f.setStyle(TableStyle([
        ('GRID', (2, 0), (2, 0), 0.1, colors.gray),
        ('GRID', (4, 0), (4, 0), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (1, 0), (-1, 0), 'MIDDLE'),
        ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (2, 0), (2, 0), colors.lightgrey),
        ('BACKGROUND', (4, 0), (4, 0), colors.lightgrey),

    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 576)


    data = [
        ('','', 'EURO', 'FUNT', 'DOLAR', '', 'ZŁOTY'),
        ('Pobrana zaliczka:','', g_euro, g_funt, g_dolar, '', g_zloty)
            ]
    f = Table(data, rowHeights=20, colWidths=[204, 3, 80, 80, 80, 3, 80])
    f.setStyle(TableStyle([
        ('GRID', (0, 1), (0, -1), 0.1, colors.gray),
        ('GRID', (2, 0), (4, -1), 0.1, colors.gray),
        ('GRID', (6, 0), (6, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
        ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (4, 0), colors.lightgrey),
        ('BACKGROUND', (6, 0), (6, 0), colors.lightgrey),


    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 534)

    data = [
        ('Dieta:','', dieta_zagr, '', dieta_kr)
            ]
    f = Table(data, rowHeights=20, colWidths=[204, 3, 240, 3, 80])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (0, -1), 0.1, colors.gray),
        ('GRID', (2, 0), (2, -1), 0.1, colors.gray),
        ('GRID', (4, 0), (4, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),

    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 512)

    data = [
        ('Transport: samochód','', sam_pr_za, '', sam_pr_kr)
            ]
    f = Table(data, rowHeights=20, colWidths=[204, 3, 240, 3, 80])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (0, -1), 0.1, colors.gray),
        ('GRID', (2, 0), (2, -1), 0.1, colors.gray),
        ('GRID', (4, 0), (4, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),

    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 490)

    data = [
        ('Transport: samochód służbowy','', sam_sl_za, '', sam_sl_kr)
            ]
    f = Table(data, rowHeights=20, colWidths=[204, 3, 240, 3, 80])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (0, -1), 0.1, colors.gray),
        ('GRID', (2, 0), (2, -1), 0.1, colors.gray),
        ('GRID', (4, 0), (4, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),

    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 468) # 494


    data = [
        ('Posiłki:', '', 'Śniadanie', sniadanie, 'Obiad', obiad, 'Kolacja', kolacja)
            ]
    f = Table(data, rowHeights=20, colWidths=[204,3, 54, 54, 54, 54, 54, 53])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (0, -1), 0.1, colors.gray),
        ('GRID', (2, 0), (7, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (0, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('ALIGN', (2, 0), (2, 0), 'CENTER'),
        ('ALIGN', (3, 0), (3, 0), 'CENTER'),
        ('ALIGN', (5, 0), (5, 0), 'CENTER'),
        ('ALIGN', (7, 0), (7, 0), 'CENTER'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 446) # 448 468

    #
    # PODSUMOWANIE
    #

    data = [
        ('ZESTAWIENIE',),
            ]
    f = Table(data, rowHeights=20, colWidths=[530])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 416)


    data = [
        ('Pozycja', 'PLN', 'EUR', 'GBP', 'USD', 'CHF'),
        ('Pobr. zaliczki', g_zloty, g_euro, g_funt, g_dolar, g_frank),
        ('Dieta', d_k.amount, dz_2.amount, dz_3.amount, dz_4.amount, dz_5.amount),
        ('Wydatki', wyd1.amount, wyd2.amount, wyd3.amount, wyd4.amount, wyd5.amount),
        ('Podsumowanie', pod1.amount, pod2.amount, pod3.amount, pod4.amount, pod5.amount),
    ]

    f = Table(data, rowHeights=20, colWidths=[155, 75, 75, 75, 75, 75])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONT', (0, -1), (-1, -1), 'Dejavu-Bold', 10),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.brown),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 316)

    data = [
        ('Pobranie zaliczki - kurs', da_z, kuz2.amount, kuz3.amount, kuz4.amount, kuz5.amount),
        ('Rozliczenie - kurs', da_r, ku2.amount, ku3.amount, ku4.amount, ku5.amount),
    ]

    f = Table(data, rowHeights=20, colWidths=[155, 75, 75, 75, 75, 75])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONT', (1, 0), (1, -1), 'Dejavu', 8),
        ('ALIGN', (1, 0), (1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.green),
        ('TEXTCOLOR', (2, 0), (-1, -1), colors.grey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 273)

    data = [
        ('Zaliczki [PLN]', zal1.amount, zal2.amount, zal3.amount, zal4.amount, zal5.amount),
        ('Wydatki + diety [PLN]', wd1.amount, wd2.amount, wd3.amount, wd4.amount, wd5.amount),
        ('Suma [PLN]', sum1.amount, sum2.amount, sum3.amount, sum4.amount, sum5.amount),
    ]

    f = Table(data, rowHeights=20, colWidths=[155, 75, 75, 75, 75, 75])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONT', (0, -1), (-1, -1), 'Dejavu-Bold', 10),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.blue),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 210)


    data = [
        (sum0,),
            ]
    f = Table(data, rowHeights=20, colWidths=[100])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 440, 187)


    data = [
        ('Kwituję wpłatę / wypłatę ', 'Kwituję zwrot / odbiór'),
        ('(data) (podpis )', '(data) (podpis delegowanego)'),

            ]
    f = Table(data, rowHeights=[20, 50], colWidths=[265,265])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 1), (1, 1), 'Dejavu', 8),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.gray),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 87)


    data = [
        ('Uwagi: ',),
        ]
    f = Table(data, rowHeights=[50], colWidths=[530])
    f.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 34)


    #p.showPage()


    #!!!!!

    if (pozycje1.count()>0) or (pozycje2.count()>0) or (pozycje3.count()>0) or (pozycje4.count()>0) or (pozycje5.count()>0):
        pass
    else:
        p.showPage()


    if pozycje1.count()>0:
        p.showPage()
        im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
        p.drawInlineImage(im, 20, 760, width=80, height=65)
        p.setFont("Dejavu-Bold", 17)
        p.drawString(100, 800, "ROZLICZENIE WYJAZDU SŁUŻBOWEGO NR " + nr_dok)
        p.setFont("Dejavu", 10)

        if fl:
            tytul = "Delegacja zagraniczna z dnia:"
        else:
            tytul = "Delegacja krajowa z dnia:"

        p.drawString(100, 770, tytul)
        p.drawString(390, 770, "Rozliczona dnia:")
        p.setFont("Dejavu-Bold", 10)
        p.drawString(255, 770, data_od)
        p.drawString(475, 770, data_rozliczenia)

        p.setFont("Dejavu-Bold", 16)
        p.drawString(150, 720, "POZYCJE WYDATKÓW [PLN]")
        p.setFont("Dejavu", 10)

        data = [('Opis', 'Waluta', 'PLN'), ]

        licznik = 0
        for poz in pozycje1:
            if fl:
                kw = poz.kwota_waluta
            else:
                kw = ''
            row = (poz.pozycja, kw, poz.kwota_pln)
            licznik += 1
            data.append(row)
        f = Table(data, rowHeights=20, colWidths=[370, 80, 80])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
            # ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 670 - (licznik * 20))


        data = [
            ('Kwituję wpłatę / wypłatę ', 'Kwituję zwrot / odbiór'),
            ('(data) (podpis )', '(data) (podpis delegowanego)'),

                ]
        f = Table(data, rowHeights=[20, 50], colWidths=[265,265])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONT', (0, 1), (1, 1), 'Dejavu', 8),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.gray),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 87)

        data = [
            ('Uwagi: ',),
            ]
        f = Table(data, rowHeights=[50], colWidths=[530])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 34)


    if pozycje2.count()>0:
        p.showPage()
        im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
        p.drawInlineImage(im, 20, 760, width=80, height=65)
        p.setFont("Dejavu-Bold", 17)
        p.drawString(100, 800, "ROZLICZENIE WYJAZDU SŁUŻBOWEGO NR " + nr_dok)
        p.setFont("Dejavu", 10)

        if fl:
            tytul = "Delegacja zagraniczna z dnia:"
        else:
            tytul = "Delegacja krajowa z dnia:"

        p.drawString(100, 770, tytul)
        p.drawString(390, 770, "Rozliczona dnia:")
        p.setFont("Dejavu-Bold", 10)
        p.drawString(255, 770, data_od)
        p.drawString(475, 770, data_rozliczenia)

        p.setFont("Dejavu-Bold", 16)
        p.drawString(150, 720, "POZYCJE WYDATKÓW [EUR]")
        p.setFont("Dejavu", 10)

        data = [('Opis', 'Waluta', 'PLN'), ]

        licznik = 0
        for poz in pozycje2:
            if fl:
                kw = poz.kwota_waluta
            else:
                kw = ''
            row = (poz.pozycja, kw, poz.kwota_pln)
            licznik += 1
            data.append(row)
        f = Table(data, rowHeights=20, colWidths=[370, 80, 80])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
            # ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 670 - (licznik * 20))


        data = [
            ('Kwituję wpłatę / wypłatę ', 'Kwituję zwrot / odbiór'),
            ('(data) (podpis )', '(data) (podpis delegowanego)'),

                ]
        f = Table(data, rowHeights=[20, 50], colWidths=[265,265])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONT', (0, 1), (1, 1), 'Dejavu', 8),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.gray),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 87)

        data = [
            ('Uwagi: ',),
            ]
        f = Table(data, rowHeights=[50], colWidths=[530])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 34)


    if pozycje3.count()>0:
        p.showPage()
        im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
        p.drawInlineImage(im, 20, 760, width=80, height=65)
        p.setFont("Dejavu-Bold", 17)
        p.drawString(100, 800, "ROZLICZENIE WYJAZDU SŁUŻBOWEGO NR " + nr_dok)
        p.setFont("Dejavu", 10)

        if fl:
            tytul = "Delegacja zagraniczna z dnia:"
        else:
            tytul = "Delegacja krajowa z dnia:"

        p.drawString(100, 770, tytul)
        p.drawString(390, 770, "Rozliczona dnia:")
        p.setFont("Dejavu-Bold", 10)
        p.drawString(255, 770, data_od)
        p.drawString(475, 770, data_rozliczenia)

        p.setFont("Dejavu-Bold", 16)
        p.drawString(150, 720, "POZYCJE WYDATKÓW [GBP]")
        p.setFont("Dejavu", 10)

        data = [('Opis', 'Waluta', 'PLN'), ]

        licznik = 0
        for poz in pozycje3:
            if fl:
                kw = poz.kwota_waluta
            else:
                kw = ''
            row = (poz.pozycja, kw, poz.kwota_pln)
            licznik += 1
            data.append(row)

        f = Table(data, rowHeights=20, colWidths=[370, 80, 80])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
            # ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 670 - (licznik * 20))


        data = [
            ('Kwituję wpłatę / wypłatę ', 'Kwituję zwrot / odbiór'),
            ('(data) (podpis )', '(data) (podpis delegowanego)'),

                ]
        f = Table(data, rowHeights=[20, 50], colWidths=[265,265])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONT', (0, 1), (1, 1), 'Dejavu', 8),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.gray),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 87)

        data = [
            ('Uwagi: ',),
            ]
        f = Table(data, rowHeights=[50], colWidths=[530])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 34)


    if pozycje4.count()>0:
        p.showPage()
        im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
        p.drawInlineImage(im, 20, 760, width=80, height=65)
        p.setFont("Dejavu-Bold", 17)
        p.drawString(100, 800, "ROZLICZENIE WYJAZDU SŁUŻBOWEGO NR " + nr_dok)
        p.setFont("Dejavu", 10)

        if fl:
            tytul = "Delegacja zagraniczna z dnia:"
        else:
            tytul = "Delegacja krajowa z dnia:"

        p.drawString(100, 770, tytul)
        p.drawString(390, 770, "Rozliczona dnia:")
        p.setFont("Dejavu-Bold", 10)
        p.drawString(255, 770, data_od)
        p.drawString(475, 770, data_rozliczenia)

        p.setFont("Dejavu-Bold", 16)
        p.drawString(150, 720, "POZYCJE WYDATKÓW [USD]")
        p.setFont("Dejavu", 10)

        data = [('Opis', 'Waluta', 'PLN'), ]

        licznik = 0
        for poz in pozycje4:
            if fl:
                kw = poz.kwota_waluta
            else:
                kw = ''
            row = (poz.pozycja, kw, poz.kwota_pln)
            licznik += 1
            data.append(row)
        f = Table(data, rowHeights=20, colWidths=[370, 80, 80])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
            # ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 670 - (licznik * 20))


        data = [
            ('Kwituję wpłatę / wypłatę ', 'Kwituję zwrot / odbiór'),
            ('(data) (podpis )', '(data) (podpis delegowanego)'),

                ]
        f = Table(data, rowHeights=[20, 50], colWidths=[265,265])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONT', (0, 1), (1, 1), 'Dejavu', 8),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.gray),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 87)

        data = [
            ('Uwagi: ',),
            ]
        f = Table(data, rowHeights=[50], colWidths=[530])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 34)



    if pozycje5.count()>0:
        p.showPage()
        im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
        p.drawInlineImage(im, 20, 760, width=80, height=65)
        p.setFont("Dejavu-Bold", 17)
        p.drawString(100, 800, "ROZLICZENIE WYJAZDU SŁUŻBOWEGO NR " + nr_dok)
        p.setFont("Dejavu", 10)

        if fl:
            tytul = "Delegacja zagraniczna z dnia:"
        else:
            tytul = "Delegacja krajowa z dnia:"

        p.drawString(100, 770, tytul)
        p.drawString(390, 770, "Rozliczona dnia:")
        p.setFont("Dejavu-Bold", 10)
        p.drawString(255, 770, data_od)
        p.drawString(475, 770, data_rozliczenia)

        p.setFont("Dejavu-Bold", 16)
        p.drawString(150, 720, "POZYCJE WYDATKÓW [CHF]")
        p.setFont("Dejavu", 10)

        data = [('Opis', 'Waluta', 'PLN'), ]

        licznik = 0
        for poz in pozycje5:
            if fl:
                kw = poz.kwota_waluta
            else:
                kw = ''
            row = (poz.pozycja, kw, poz.kwota_pln)
            licznik += 1
            data.append(row)
        f = Table(data, rowHeights=20, colWidths=[370, 80, 80])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
            # ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 670 - (licznik * 20))


        data = [
            ('Kwituję wpłatę / wypłatę ', 'Kwituję zwrot / odbiór'),
            ('(data) (podpis )', '(data) (podpis delegowanego)'),

                ]
        f = Table(data, rowHeights=[20, 50], colWidths=[265,265])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONT', (0, 1), (1, 1), 'Dejavu', 8),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.gray),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 87)

        data = [
            ('Uwagi: ',),
            ]
        f = Table(data, rowHeights=[50], colWidths=[530])
        f.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        f.wrapOn(p, 300, 300)
        f.drawOn(p, 40, 34)





    # print("PLN", pozycje1.count())
    # print("EUR", pozycje2.count())
    # print("GBP", pozycje3.count())
    # print("USD", pozycje4.count())
    # print("CHF", pozycje5.count())

    #p.showPage()

    p.save()
    return response



