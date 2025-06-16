from django.shortcuts import render, redirect, get_object_or_404
from .models import Telefon
from .forms import TelefonForm
from .out_doc import phonepp, phonepz
from django.contrib.auth.decorators import login_required

import xlwt
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime



@login_required(login_url='error')
def phone(request):
    telefon = Telefon.objects.filter(arch=False, mag=False).order_by('usr')
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    return render(request, 'PHONES/phone.html', {
        'telefony': telefon,
        'name_log': name_log,
        'naglowek': 'Lista telefonów.',
        'about': about,
        'mag' : False
    })


@login_required(login_url='error')
def phone_arch(request):
    telefon = Telefon.objects.filter(arch=True).order_by('usr')
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    return render(request, 'PHONES/phone.html', {
        'telefony': telefon,
        'name_log': name_log,
        'naglowek': 'Lista telefonów.',
        'about': about,
        'mag' : True
    })


@login_required(login_url='error')
def phone_mag(request):
    telefon = Telefon.objects.filter(mag=True).order_by('usr')
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    return render(request, 'PHONES/phone.html', {
        'telefony': telefon,
        'name_log': name_log,
        'naglowek': 'Lista telefonów w magazynie.',
        'about': about,
        'mag': True
    })



@login_required(login_url='error')
def phone_add(request):
    tytul = "Dodaj telefon"
    if request.method == "POST":
        telf = TelefonForm(request.POST or None, request.FILES or None)
        if telf.is_valid():
            post = telf.save(commit=False)
            post.save()
            return redirect('phone_start')
    else:
        telf = TelefonForm()
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM
    return render(request, 'PHONES/phone_add.html', {
        'name_log': name_log,
        'tytul': tytul,
        'form': telf,
        'edycja': False,
        'phone_id': 0,
        'about': about
    })


@login_required(login_url='error')
def phone_addc(request, pk):
    tytul = "Przekazanie telefonu"
    if request.method == "POST":
        telf = TelefonForm(request.POST or None, request.FILES or None)
        if telf.is_valid():
            post = telf.save(commit=False)
            post.save()
            return redirect('phone_start')
    else:
        tel = Telefon.objects.get(id=pk)

        telf = TelefonForm(initial={
            'usr': "klon_"+tel.usr,
            'model': tel.model,
            'imei': tel.imei,
            'sim': tel.sim,
            'msisdn': tel.msisdn,
            'kod': tel.kod,
            'arch': False,
            'mag': False
        })

        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

    return render(request, 'PHONES/phone_add.html', {
        'name_log': name_log,
        'tytul': tytul,
        'form': telf,
        'edycja': False,
        'phone_id': 0,
        'about': about
    })


@login_required(login_url='error')
def phone_edit(request, pk):
    telm = get_object_or_404(Telefon, pk=pk)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    if request.method == "POST":
        telf = TelefonForm(request.POST or None, request.FILES or None, instance=telm)
        if telf.is_valid():
            ps = telf.save(commit=False)
            ps.save()
            return redirect('phone_start')
        else:
            return redirect('error')
    else:
        telf = TelefonForm(instance=telm)
    return  render(request, 'PHONES/phone_add.html', {
        'name_log': name_log,
        'tytul': "Edycja telefonu",
        'form': telf,
        'edycja': True,
        'phone_id': pk,
        'about': about
    })


@login_required(login_url='error')
def phone_delete(request, pk):
    Telefon.objects.get(pk=pk).delete()
    return redirect('phone_start')


@login_required(login_url='error')
def phone_pp(request, pk):
    return phonepp(request, pk)

@login_required(login_url='error')
def phone_pz(request, pk):
    return phonepz(request, pk)

def phone_export(request):

    dt = datetime.now().strftime("%d%m%Y_%H%M%S") # '17062022_161200'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="SDA - Telefony '+ dt +'.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Telefony')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Użytkownik', 'Model telefonu', 'IMEI', 'SIM', 'MSISDN', 'Kod blokady', 'Konto', 'Hasło', 'Data przekazania', 'Uwagi',]
    col_width = [30,20,30,10,30,20,50,50,20,100]
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    #font_style = xlwt.XFStyle()

    rows = Telefon.objects.filter(mag=False, arch=False).values_list('usr', 'model', 'imei', 'sim', 'msisdn', 'kod', 'konto', 'haslo', 'data', 'uwagi')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 8:
                font_style = xlwt.XFStyle()
                font_style.num_format_str = 'dd.mm.yyyy'
            else:
                font_style = xlwt.XFStyle()
            ws.write(row_num, col_num, row[col_num], font_style)



    ws = wb.add_sheet('Magazyn')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Użytkownik', 'Model telefonu', 'IMEI', 'SIM', 'MSISDN', 'Kod blokady', 'Konto', 'Hasło', 'Data przekazania', 'Uwagi',]
    col_width = [30, 20, 30, 10, 30, 20, 50, 50, 20, 100]

    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Telefon.objects.filter(mag=True, arch=False).values_list('usr', 'model', 'imei', 'sim', 'msisdn', 'kod', 'konto', 'haslo', 'data', 'uwagi')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 8:
                font_style = xlwt.XFStyle()
                font_style.num_format_str = 'dd.mm.yyyy'
            else:
                font_style = xlwt.XFStyle()
            ws.write(row_num, col_num, row[col_num], font_style)



    # ws = wb.add_sheet('Archiwum')
    #
    # # Sheet header, first row
    # row_num = 0
    #
    # font_style = xlwt.XFStyle()
    # font_style.font.bold = True
    #
    # columns = ['Użytkownik', 'Model telefonu', 'IMEI', 'SIM', 'MSISDN', 'Kod blokady', 'Konto', 'Hasło',
    #            'Data przekazania', 'Uwagi', ]
    # col_width = [30, 20, 30, 10, 30, 20, 50, 50, 20, 100]
    # for col_num in range(len(columns)):
    #     ws.col(col_num).width = col_width[col_num] * 256
    #     ws.write(row_num, col_num, columns[col_num], font_style)
    #
    # # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()
    #
    # rows = Telefon.objects.filter(mag=False, arch=True).values_list('usr', 'model', 'imei', 'sim', 'msisdn', 'kod',
    #                                                                 'konto', 'haslo', 'data', 'uwagi')
    # for row in rows:
    #     row_num += 1
    #     for col_num in range(len(row)):
    #         if col_num == 8:
    #             font_style = xlwt.XFStyle()
    #             font_style.num_format_str = 'dd.mm.yyyy'
    #         else:
    #             font_style = xlwt.XFStyle()
    #         ws.write(row_num, col_num, row[col_num], font_style)



    wb.save(response)
    return response