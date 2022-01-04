from django.shortcuts import render, redirect, get_object_or_404
from .models import  FirmaKasa, RaportKasowy, KwKp, Waluta
from .forms import  FirmaKasaForm, KwKpForm
from datetime import datetime
from datetime import timedelta
from TaskAPI.functions import get_user_label, trans_month
from RK.functions import upgradeLeft, calcAll, intstr_month
from django.http import HttpResponse
from django.contrib.auth.models import Group
from reportlab.platypus import TableStyle, Paragraph, SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet



def smrk_pdf(mc, idk):
    kasa = FirmaKasa.objects.get(id=idk)

    drk =  KwKp.objects.filter(kasa=idk, data__month=mc)
    idrk_r =  KwKp.objects.filter(kasa=idk, data__month=mc).count()

    ils = idrk_r
    rok=''
    for d in drk:
        rok = d.data.strftime('%Y')


    ls = []   # liczba stron
    pns = 22  # pozycje na stronie
    oss = 0   # uzupełniająca liczba pozycji dla ostatniej strony
    if ils > pns:
        while ils > 0:
            if ils >= pns:
                ls.append(pns)
                ils = ils - pns
            else:
                ls.append(ils)
                oss = pns - ils
                ils = 0
    else:
        ls.append(ils)


    response = HttpResponse(content_type='application/pdf')


    titlefile = "SMRK-"+mc+"-"+rok+'.pdf'
    namefile = 'filename="'+titlefile+'"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=landscape(A4))
    p.setTitle(titlefile)
    width, height = landscape(A4)
    #pdfmetrics.registerFont(TTFont('Calibri-Italic', 'calibrii.ttf')) # 'Dejavu-Italic', 'DejaVuSerif-Italic.ttf'
    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))
    # Pierwsza strona
    # ls liczba stron oraz liczba wierszy
    lp = 1 #liczba porzadkowa
    strd = 0
    for lsd in ls:
        strd = strd + 1
        p.setStrokeColor(colors.grey)
        p.roundRect(40, (height - 80), (width - 60), 60, 5, stroke=1, fill=0)

        p.setFont("Dejavu", 8)
        p.drawString(50, (height - 40), kasa.nazwa)
        p.drawString(50, (height - 50), kasa.adres)
        p.drawString(50, (height - 60), kasa.miasto)
        p.drawString(50, (height - 70), kasa.nip)

        p.setFont("Dejavu-Bold", 15)
        p.drawString((width - 480), (height - 40), "SZCZEGÓŁOWY RAPORT KASOWY: SMRK/"+mc+"/"+rok)
        p.setFont("Dejavu-Bold", 9)
        p.drawString((width - 75), (height - 75), "Str. "+str(strd)+" z "+str(len(ls)))

        pdrk = RaportKasowy.objects.filter(kasa=idk, data__month=mc)
        ldrk = RaportKasowy.objects.filter(kasa=idk, data__month=mc).count()
        sp = 0
        sr = 0
        for d in pdrk:
            sp = sp + d.sum_przychod
            sr = sr + d.sum_rozchod

        stp = pdrk[0].stan_poprzedni
        i = ldrk - 1
        stk = pdrk[i].stan_obecny

        data = [('Kasa:',kasa.kasa ,'Suma przychód:',sp,'Stan początkowy:',stp),('Za miesiąc:',intstr_month(mc),'Suma Rozchód:',sr,'Stan końcowy:',stk)]
        f = Table(data, rowHeights=16, colWidths=85)
        f.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
            ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 8),
            ('ALIGN',(0, 0), (0, -1), 'RIGHT'),
            ('FONT', (2, 0), (2, -1), 'Dejavu-Bold', 8),
            ('ALIGN',(2, 0), (2, -1), 'RIGHT'),
            ('FONT', (4, 0), (4, -1), 'Dejavu-Bold', 8),
            ('ALIGN',(4, 0), (4, -1), 'RIGHT'),
        ]))

        f.wrapOn(p, 300, 300)
        f.drawOn(p, 250, height - 79)

        data=[]
        headings = ('LP.','DATA', 'DOKUMENT', 'DLA/OD KOGO', 'ZA CO', 'PRZYCHÓD', 'ROZCHÓD')

        sw = 0 #pomocniczy licznik wierszy na stronie
        while sw<ls[strd -1]:
            d = drk[lp-1]
            o_s = d.opis
            if len(o_s) > 62:
                o_s = o_s[:62]
            data.append([str(lp), d.data.strftime('%d.%m.%Y'), d.rodzaj+'/'+str(d.numer)+'_'+d.data.strftime('%d/%m/%Y'), d.nazwa, o_s, d.przychod, d.rozchod]) # +' '+d.adres+' '+d.miasto
            lp = lp + 1
            sw = sw + 1



        idrk = ls[0] * 20 + 20 + 92 #!!!
        f = Table([headings] + data, rowHeights=20, colWidths=[25, 60, 100, 120, 325, 75, 75])
        f.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
            ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (1, 1), (2, -1), 'CENTER'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.15, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0),colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('BOX', (0, 0), (-1, 0), 0.2, colors.gray),
            ]))

        f.wrapOn(p, 300, 300)

        if strd==len(ls):
            idrk_p = idrk - (oss*20)
            f.drawOn(p, 42, height - idrk_p)
        else:
            f.drawOn(p, 42, height - idrk)

        if strd<len(ls):
            p.showPage()

    p.showPage()
    p.save()
    return response

def mrk_pdf(mc, idk):
    kasa = FirmaKasa.objects.get(id=idk)

    drk =  RaportKasowy.objects.filter(kasa=idk, data__month=mc)
    idrk_r =  RaportKasowy.objects.filter(kasa=idk, data__month=mc).count()
    idrk = idrk_r * 20 + 20 + 92

    response = HttpResponse(content_type='application/pdf')
    for d in drk:
        rok = d.data.strftime('%Y')

    titlefile = "MRK-"+mc+"-"+rok+'.pdf'
    namefile = 'filename="'+titlefile+'"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=A4)
    p.setTitle(titlefile)
    width, height = A4
    #pdfmetrics.registerFont(TTFont('Dejavu-Italic', 'DejaVuSerif-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    p.setStrokeColor(colors.grey)
    p.roundRect(40, 760, 530, 60, 5, stroke=1, fill=0)
    #p.roundRect(40, 40, 530, 60, 5, stroke=1, fill=0)

    p.setFont("Dejavu", 8)
    p.drawString(50, (height - 40), kasa.nazwa)
    p.drawString(50, (height - 50), kasa.adres)
    p.drawString(50, (height - 60), kasa.miasto)
    p.drawString(50, (height - 70), kasa.nip)

    p.setFont("Dejavu-Bold", 15)
    p.drawString(280, (height - 40), "RAPORT KASOWY: MRK/"+mc+"/"+rok)
    p.setFont("Dejavu-Bold", 9)
    p.drawString(430, (height - 70), "Kasa:")
    p.drawString(280, (height - 70), "Za miesiąc: ")
    p.setFont("Dejavu", 9)
    p.drawString(460, (height - 70), kasa.kasa)
    p.drawString(340, (height - 70), intstr_month(mc))

    data=[]
    headings = ('SYMBOL', 'KW', 'KP', 'SUMA PRZYCHÓD', 'SUMA ROZCHÓD', 'STAN POPRZEDNI', 'STAN OBECNY')
    for d in drk:
        data.append([d.data.strftime('%d/%m/%Y'), d.kw, d.kp, d.sum_przychod, d.sum_rozchod, d.stan_poprzedni, d.stan_obecny])

    f = Table([headings] + data, rowHeights=20) # colWidths=60,
    f.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (1, 1), (2, -1), 'CENTER'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0),colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BOX', (0, 0), (-1, 0), 0.2, colors.gray),
        ]))

    f.wrapOn(p, 300, 300)
    f.drawOn(p, 42, height - idrk)

    data = [

        ('Podpis', 'KASA'),
        ('',''),
        ('',''),
        ]

    f = Table(data, rowHeights=18, colWidths=70) # colWidths=60,
    f.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 8),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0),colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, -1), colors.lightgrey),
        ('SPAN', (0, 1), (0, -1)),
        ('SPAN', (1, 0), (1, -1)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BOX', (0, 0), (-1, 0), 0.2, colors.gray),
        ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 40, 40)

    sp = 0
    sr = 0
    for d in drk:
        sp = sp + d.sum_przychod
        sr = sr + d.sum_rozchod

    data = [

        ('SUMA PRZYCHÓD', 'SUMA ROZCHÓD'),
        (sp, sr),
        ('', ''),

        ]

    f = Table(data, rowHeights=18) # colWidths=60,
    f.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Dejavu-Bold', 8),
        ('FONT', (0, 1), (-1, -1), 'Dejavu-Bold', 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0),colors.lightgrey),
        #('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        #('SPAN', (0, 0), (0, -1)),
        ('SPAN', (0, 1), (0, -1)),
        ('SPAN', (1, 1), (1, -1)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BOX', (0, 0), (-1, 0), 0.2, colors.gray),
        ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 385, 40)


    stp = drk[0].stan_poprzedni  #.object.all().get().first()
    i = idrk_r - 1
    stk = drk[i].stan_obecny
    data = [

        ('STAN POCZATKOWY', 'STAN KOŃCOWY'),
        (stp, stk),
        ('', ''),

    ]

    f = Table(data, rowHeights=18)  # colWidths=60,
    f.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Dejavu-Bold', 8),
        ('FONT', (0, 1), (-1, -1), 'Dejavu-Bold', 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        # ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        # ('SPAN', (0, 0), (0, -1)),
        ('SPAN', (0, 1), (0, -1)),
        ('SPAN', (1, 1), (1, -1)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BOX', (0, 0), (-1, 0), 0.2, colors.gray),
    ]))
    f.wrapOn(p, 300, 300)
    f.drawOn(p, 185, 40)





    p.showPage()
    p.save()
    return response

def drk_pdf(dt, idk): # 16.06.2019
    kasa = FirmaKasa.objects.get(id=idk)

    sdata = dt.split('-')
    rok = sdata[0]
    miesiac = sdata[1]
    dzien = sdata[2]

    drk    = KwKp.objects.filter(kasa=idk, data__day=dzien, data__month=miesiac, data__year=rok)

    d_rk = RaportKasowy.objects.filter(kasa=idk, data__day=dzien, data__month=miesiac, data__year=rok)

    idrk_r = KwKp.objects.filter(kasa=idk, data__day=dzien, data__month=miesiac, data__year=rok).count()
    idrk   = idrk_r * 20 + 20 + 92

    response = HttpResponse(content_type='application/pdf')

    titlefile = "DRK-"+dt+'.pdf'
    namefile = 'filename="'+titlefile+'"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=landscape(A4))
    p.setTitle(titlefile)
    height,  width = A4
    #pdfmetrics.registerFont(TTFont('Dejavu-Italic', 'DejaVuSerif-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    p.setStrokeColor(colors.grey)
    p.roundRect(40, (height - 80), (width - 60), 60, 5, stroke=1, fill=0)


    p.setFont("Dejavu", 8)
    p.drawString(50, (height - 40), kasa.nazwa)
    p.drawString(50, (height - 50), kasa.adres)
    p.drawString(50, (height - 60), kasa.miasto)
    p.drawString(50, (height - 70), kasa.nip)

    p.setFont("Dejavu-Bold", 15)
    p.drawString(500, (height - 40), "RAPORT KASOWY: DRK/"+dzien+"/"+miesiac+"/"+rok)
    p.setFont("Dejavu-Bold", 9)

    data=[]
    headings = ('NR', 'Kto', 'Opis', 'PRZYCHÓD', 'ROZCHÓD')
    for d in drk:
        n_r = d.rodzaj+"/"+str(d.numer)
        o_s = d.opis
        if len(o_s)>75:
            o_s = o_s[:75]
        data.append([n_r, d.nazwa, o_s, d.przychod, d.rozchod])

    f = Table([headings] + data, rowHeights=20, colWidths=[50,150,420,80,80]) # colWidths=60,
    f.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (1, 1), (2, -1), 'CENTER'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0),colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BOX', (0, 0), (-1, 0), 0.2, colors.gray),
        ]))

    f.wrapOn(p, 300, 300)
    f.drawOn(p, 42, height - idrk)

    sr  = d_rk[0].sum_rozchod
    sp  = d_rk[0].sum_przychod
    stp = d_rk[0].stan_poprzedni
    stk = d_rk[0].stan_obecny

    data = [('Kasa:', kasa.kasa, 'Suma przychód:', sp, 'Stan początkowy:', stp),
            ('Data:', dt, 'Suma Rozchód:', sr, 'Stan końcowy:', stk)]
    f = Table(data, rowHeights=16, colWidths=85)
    f.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 9),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.white),
        ('FONT', (0, 0), (0, -1), 'Dejavu-Bold', 8),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('FONT', (2, 0), (2, -1), 'Dejavu-Bold', 8),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('FONT', (4, 0), (4, -1), 'Dejavu-Bold', 8),
        ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
    ]))

    f.wrapOn(p, 300, 300)
    f.drawOn(p, 310, height - 79)

    p.showPage()
    p.save()
    return response

def kwkp_pdf(request, pk, idk):

    wersja = 'SDA KWKP - wersja: 01.02 (07.07.2019)'

    doc = KwKp.objects.get(id=pk)
    kasa = FirmaKasa.objects.get(id=idk)
    kasjer = get_user_label(request)

    opis = doc.opis.split(" ")
    opis1 = ''
    opis2 = ''
    opis3 = ''
    flaga = 0
    for o in opis:
        if flaga==0:
            if len(opis1)<70:
                opis1 = opis1 + " " + o
            else:
                flaga = flaga + 1;
        if flaga==1:
            if len(opis2) < 70:
                opis2 = opis2 + " " + o
            else:
                flaga = flaga + 1;
        if flaga==2:
            if len(opis3) < 70:
                opis3 = opis3 + " " + o
            else:
                flaga = flaga + 1;


    response = HttpResponse(content_type='application/pdf')
    titlefile = doc.rodzaj+str(doc.numer)+'-'+doc.data.strftime('%d%m%Y')+'.pdf'
    namefile = 'filename="'+titlefile+'"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=A4)
    p.setTitle(titlefile)
    width, height = A4
    #pdfmetrics.registerFont(TTFont('Dejavu-Italic', 'DejaVuSerif-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    p.setFont("Dejavu", 12)
    p.drawString(50, (height - 60), kasa.nazwa)
    p.drawString(50, (height - 80), kasa.adres)
    p.drawString(50, (height - 100), kasa.miasto)
    p.drawString(50, (height - 120), kasa.nip)
    p.setFont("Dejavu-Bold", 15)
    if doc.rodzaj=='KW':
        p.drawString(360, (height - 60), "KW - DOWÓD WYPŁATY")
    else:
        p.drawString(360, (height - 60), "KP - DOWÓD WPŁATY")
    p.setFont("Dejavu", 10)
    p.drawString(400, (height - 80), "Pokwitowanie - Orginał")
    p.setFont("Dejavu-Bold", 12)
    p.drawString(400, (height - 120), "Nr "+doc.rodzaj+'/'+str(doc.numer)+'_'+doc.data.strftime('%d/%m/%Y'))

    p.setFont("Dejavu-Bold", 12)
    p.drawString(50, (height - 160), "Komu:")
    p.setFont("Dejavu", 12)
    p.drawString(50, (height - 180), doc.nazwa)
    p.drawString(50, (height - 200), doc.adres)
    p.drawString(50, (height - 220), doc.miasto)
    p.drawString(50, (height - 240), "")
    p.setFont("Dejavu-Bold", 12)
    p.drawString(50, (height - 230), "Za co:")
    p.setFont("Dejavu", 12)

    p.drawString(50, (height - 250), opis1)
    p.drawString(50, (height - 270), opis2)
    p.drawString(50, (height - 290), opis3)

    p.setFont("Dejavu", 12)
    p.drawString(410, (height - 200), kasa.kasa)
    p.drawString(200, (height - 370), kasjer)
    p.drawString(200, (height - 790), kasjer)
    p.setFont("Dejavu-Bold", 12)

    p.drawString(280, (height - 320), "SUMA:")
    p.drawString(430, (height - 320), str(doc.rozchod + doc.przychod))
    p.setFont("Dejavu", 8)
    if doc.rodzaj == 'KW':
        p.drawString(400, (height - 345), "Kwotę powyższą otrzymał/a")
        p.drawString(200, (height - 345), "Kwotę powyższą wydał/a")
    else:
        p.drawString(400, (height - 345), "Kwotę powyższą wydał/a")
        p.drawString(200, (height - 345), "Kwotę powyższą otrzymał/a")

    p.setFont("Dejavu", 12)
    p.drawString(50, (height - 480), kasa.nazwa)
    p.drawString(50, (height - 500), kasa.adres)
    p.drawString(50, (height - 520), kasa.miasto)
    p.drawString(50, (height - 540), kasa.nip)
    p.setFont("Dejavu-Bold", 15)
    if doc.rodzaj=='KW':
        p.drawString(360, (height - 480), "KW - DOWÓD WYPŁATY")
    else:
        p.drawString(360, (height - 480), "KP - DOWÓD WPŁATY")
    p.setFont("Dejavu", 10)
    p.drawString(400, (height - 500), "Pokwitowanie - Kopia")
    p.setFont("Dejavu-Bold", 12)
    p.drawString(400, (height - 540), "Nr "+doc.rodzaj+'/'+str(doc.numer)+'_'+doc.data.strftime('%d/%m/%Y'))

    p.setFont("Dejavu-Bold", 12)
    p.drawString(50, (height - 580), "Komu:")
    p.setFont("Dejavu", 12)
    p.drawString(50, (height - 600), doc.nazwa)
    p.drawString(50, (height - 620), doc.adres)
    p.drawString(50, (height - 640), doc.miasto)
    p.drawString(50, (height - 660), "")
    p.setFont("Dejavu-Bold", 12)
    p.drawString(50, (height - 650), "Za co:")
    p.setFont("Dejavu", 12)
    p.drawString(50, (height - 670), opis1)
    p.drawString(50, (height - 690), opis2)
    p.drawString(50, (height - 710), opis3)
    p.setFont("Dejavu", 12)
    p.drawString(410, (height - 620), kasa.kasa)
    p.setFont("Dejavu-Bold", 12)

    p.drawString(280, (height - 740), "SUMA:")
    p.drawString(430, (height - 740), str(doc.rozchod + doc.przychod))
    p.setFont("Dejavu", 8)
    if doc.rodzaj == 'KW':
        p.drawString(400, (height - 765), "Kwotę powyższą otrzymał/a")
        p.drawString(200, (height - 765), "Kwotę powyższą wydał/a")
    else:
        p.drawString(400, (height - 765), "Kwotę powyższą wydał/a")
        p.drawString(200, (height - 765), "Kwotę powyższą otrzymał/a")

    p.setFont("Dejavu", 7)
    p.drawString(420, (height - 810), wersja)
    p.drawString(420, (height - 390), wersja)




    p.setStrokeColor(colors.grey)

    p.roundRect(40, 460, 530, 350, 5, stroke=1, fill=0)
    p.roundRect(40, 40, 530, 350, 5, stroke=1, fill=0)
    p.line(40,700, 570,700)
    p.line(350, 810, 350, 700)
    p.line(40, 630, 570, 630)
    p.line(40, 540, 570, 540)
    p.line(350, 540, 350, 460)
    p.line(150, 510, 150, 460)
    p.line(350, 660, 350, 630)
    p.line(350, 660, 570, 660)
    p.line(150, 510, 570, 510)

    p.line(40,280, 570,280)
    p.line(350, 390, 350, 280)
    p.line(40, 210, 570, 210)
    p.line(40, 120, 570, 120)

    p.line(350, 120, 350, 40)
    p.line(150, 90, 150, 40)
    p.line(350, 240, 350, 210)
    p.line(150, 90, 570, 90)
    p.line(350, 240, 570, 240)

    p.showPage()
    p.save()
    return response
