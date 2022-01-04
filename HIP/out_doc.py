from django.shortcuts import render, redirect, get_object_or_404
from simple_search import search_filter
from .models import Sprzet, Profil, System
from .forms import SprzetForm, ProfilForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from PIL import Image
from reportlab.platypus import TableStyle, Paragraph, SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from django.conf import settings
import os

def hippdfpp(request, pk):
    sprzet = Sprzet.objects.get(id=pk)

    response = HttpResponse(content_type='application/pdf')

    titlefile = "PP-"+sprzet.usr+'.pdf'
    namefile = 'filename="'+titlefile+'"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=A4)
    p.setTitle(titlefile)
    width, height = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 40, (height - 140), width=150, height=127)

    p.setFont("Dejavu-Bold", 16)
    p.drawString((width/2 - 160), (height - 150), "PROTOKÓŁ ZDAWCZO – ODBIORCZY")
    p.drawString((width/2 - 100), (height - 170), "PRZEKAZANIA MIENIA")

    p.setFont("Dejavu", 10)
    txt = 'Sporządzony dnia '+str(sprzet.pr.strftime('%d.%m.%Y'))+' r.'
    p.drawString(((width/2) - 80), (height - 200), txt)

    txt = 'Stanowiący Załącznik nr.1 do Umowy o indywidualnej odpowiedzialności materialnej za powierzone'
    p.drawString(40, (height - 240), txt)
    txt = 'mienie.'
    p.drawString(40, (height - 255), txt)

    p.setFont("Dejavu-Bold", 10)
    txt = 'PRZEKAZUJĄCY:'
    p.drawString(40, (height - 275), txt)
    p.setFont("Dejavu", 10)
    txt = 'Smart Design Expo sp. z o.o., NIP:7811875078 Szparagowa 12, 62-081 Wysogotowo'
    p.drawString(80, (height - 290), txt)

    p.setFont("Dejavu-Bold", 10)
    txt = 'PRZYJMUJĄCY:'
    p.drawString(40, (height - 310), txt)

    txt = sprzet.usr
    p.drawString(140, (height - 325), txt)
    txt = sprzet.zam
    p.drawString(140, (height - 340), txt)
    txt = sprzet.pesel
    p.drawString(140, (height - 355), txt)

    p.setFont("Dejavu", 10)
    txt = 'OSOBA:'
    p.drawString(80, (height - 325), txt)
    txt = 'ADRES: '
    p.drawString(80, (height - 340), txt)
    txt = 'PESEL: '
    p.drawString(80, (height - 355), txt)

    txt = 'Przekazujący przekazuje a Przejmujący przyjmuje przedmioty opisane w pkt 2 niniejszego protokołu.'
    p.drawString(40, (height - 375), txt)

    txt = '1. Przedmioty przekazania stanowią:'
    p.drawString(40, (height - 400), txt)

    opis1 = sprzet.host+' typ: '+sprzet.typ+', nr ser.: '+sprzet.snk +' '
    opis2 = 'i oznaczeniu: '+sprzet.kik
    opis = opis1 + opis2
    if len(opis) > 79:
        opis = opis1 +'\n'+ opis2
    data=[('1', opis ,'1'),]

    headings = ('Lp.', 'Nazwa, rodzaj i cechy identyfikacyjne przedmiotu przekazania', 'Ilość')

    f = Table([headings] + data, rowHeights=[25, 45], colWidths=[30, 440, 40])
    f.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.grey),
        ]))

    f.wrapOn(p, 300, 300)
    f.drawOn(p, 42, 360)

    txt = '2. Strony nie zgłaszają uwag/Strony zgłaszają następujące uwagi*:'
    p.drawString(40, (height - 500), txt)
    txt = '..................................................................................................................................................................'
    p.drawString(40, (height - 520), txt)
    txt = '..................................................................................................................................................................'
    p.drawString(40, (height - 540), txt)
    txt = '..................................................................................................................................................................'
    p.drawString(40, (height - 560), txt)
    p.setFont("Dejavu", 8)
    txt = '(* niepotrzebne wykreślić, bez uwag lub określić stan, usterki, kompletność, wymienić istotne)'
    p.drawString(100, (height - 570), txt)
    p.setFont("Dejavu", 10)
    txt = '3. Protokół sporządzono w dwóch jednobrzmiących egzemplarzach po jednym dla każdej ze stron.'
    p.drawString(40, (height - 590), txt)
    txt = '.......................................................                                                  .........................................................'
    p.drawString(40, (height - 650), txt)
    p.setFont("Dejavu-Bold", 10)
    txt = 'PRZEKAZUJĄCY:'
    p.drawString(80, (height - 670), txt)
    txt = 'PRZYJMUJĄCY:'
    p.drawString(420, (height - 670), txt)
    p.setFillColor(HexColor('#aaaaaa'))
    p.setFont("Dejavu-Bold", 8)
    txt = '____________________________________________________________________________________________________________________________________'
    p.drawString(40, 50, txt)
    txt = 'Wysogotowo, ul. Szparagowa 12, 62-081 Przeźmierowo > office@smartdesign-expo.com > www.smartdesign-expo.com'
    p.drawString(40, 40, txt)
    p.showPage()
    p.save()
    return response

def hippdfpz(request, pk):
    sprzet = Sprzet.objects.get(id=pk)

    response = HttpResponse(content_type='application/pdf')

    titlefile = "PZ-"+sprzet.usr+'.pdf'
    namefile = 'filename="'+titlefile+'"'
    response['Content-Disposition'] = namefile

    p = canvas.Canvas(response, pagesize=A4)
    p.setTitle(titlefile)
    width, height = A4

    pdfmetrics.registerFont(TTFont('Dejavu-Bold', 'DejaVuSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Dejavu', 'DejaVuSerif.ttf'))

    im = Image.open(os.path.join(settings.STATIC_ROOT, 'img/sd.jpg'))
    p.drawInlineImage(im, 40, (height - 140), width=150, height=127)

    p.setFont("Dejavu-Bold", 16)
    p.drawString((width/2 - 160), (height - 150), "PROTOKÓŁ ZDAWCZO – ODBIORCZY")
    p.drawString((width/2 - 100), (height - 170), "PRZEKAZANIA MIENIA")

    p.setFont("Dejavu", 10)
    txt = 'Sporządzony dnia '+str(sprzet.pr.strftime('%d.%m.%Y'))+' r.'
    p.drawString(((width/2) - 80), (height - 200), txt)

    txt = 'Stanowiący Załącznik nr.1 do Umowy o indywidualnej odpowiedzialności materialnej za powierzone'
    p.drawString(40, (height - 240), txt)
    txt = 'mienie.'
    p.drawString(40, (height - 255), txt)

    p.setFont("Dejavu-Bold", 10)
    txt = 'PRZEKAZUJĄCY:'
    p.drawString(40, (height - 275), txt)
    p.setFont("Dejavu", 10)
    txt = 'Smart Design Expo sp. z o.o., NIP:7811875078 Szparagowa 12, 62-081 Wysogotowo'
    p.drawString(80, (height - 355), txt)

    p.setFont("Dejavu-Bold", 10)
    txt = 'PRZYJMUJĄCY:'
    p.drawString(40, (height - 340), txt)

    txt = sprzet.usr
    p.drawString(140, (height - 290), txt)
    txt = sprzet.zam
    p.drawString(140, (height - 305), txt)
    txt = sprzet.pesel
    p.drawString(140, (height - 320), txt)

    p.setFont("Dejavu", 10)
    txt = 'OSOBA:'
    p.drawString(80, (height - 290), txt)
    txt = 'ADRES: '
    p.drawString(80, (height - 305), txt)
    txt = 'PESEL: '
    p.drawString(80, (height - 320), txt)

    txt = 'Przekazujący przekazuje a Przejmujący przyjmuje przedmioty opisane w pkt 2 niniejszego protokołu.'
    p.drawString(40, (height - 375), txt)

    txt = '1. Przedmioty przekazania stanowią:'
    p.drawString(40, (height - 400), txt)

    opis1 = sprzet.host+' typ: '+sprzet.typ+', nr ser.: '+sprzet.snk +' '
    opis2 = 'i oznaczeniu: '+sprzet.kik
    opis = opis1 + opis2
    if len(opis) > 79:
        opis = opis1 +'\n'+ opis2
    data=[('1', opis ,'1'),]

    headings = ('Lp.', 'Nazwa, rodzaj i cechy identyfikacyjne przedmiotu przekazania', 'Ilość')

    f = Table([headings] + data, rowHeights=[25, 45], colWidths=[30, 440, 40])
    f.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Dejavu', 10),
        ('FONT', (0, 0), (-1, 0), 'Dejavu-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.grey),
        ]))

    f.wrapOn(p, 300, 300)
    f.drawOn(p, 42, 360)

    txt = '2. Strony nie zgłaszają uwag/Strony zgłaszają następujące uwagi*:'
    p.drawString(40, (height - 500), txt)
    txt = '..................................................................................................................................................................'
    p.drawString(40, (height - 520), txt)
    txt = '..................................................................................................................................................................'
    p.drawString(40, (height - 540), txt)
    txt = '..................................................................................................................................................................'
    p.drawString(40, (height - 560), txt)
    p.setFont("Dejavu", 8)
    txt = '(* niepotrzebne wykreślić, bez uwag lub określić stan, usterki, kompletność, wymienić istotne)'
    p.drawString(100, (height - 570), txt)
    p.setFont("Dejavu", 10)
    txt = '3. Protokół sporządzono w dwóch jednobrzmiących egzemplarzach po jednym dla każdej ze stron.'
    p.drawString(40, (height - 590), txt)
    txt = '.......................................................                                                  .........................................................'
    p.drawString(40, (height - 650), txt)
    p.setFont("Dejavu-Bold", 10)
    txt = 'PRZEKAZUJĄCY:'
    p.drawString(80, (height - 670), txt)
    txt = 'PRZYJMUJĄCY:'
    p.drawString(420, (height - 670), txt)
    p.setFillColor(HexColor('#aaaaaa'))
    p.setFont("Dejavu-Bold", 8)
    txt = '____________________________________________________________________________________________________________________________________'
    p.drawString(40, 50, txt)
    txt = 'Wysogotowo, ul. Szparagowa 12, 62-081 Przeźmierowo > office@smartdesign-expo.com > www.smartdesign-expo.com'
    p.drawString(40, 40, txt)
    p.showPage()
    p.save()
    return response