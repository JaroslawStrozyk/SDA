from django.shortcuts import render, redirect, get_object_or_404
from .models import Auto
from .forms  import AutoForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
import xlwt
from django.http import HttpResponse


@login_required(login_url='error')
def auta(request):
    auto = Auto.objects.filter(rodzaj='AUTO', arch=False).order_by('typ')
    wozki = Auto.objects.filter(rodzaj='WUWI', arch=False).order_by('typ')
    inne = Auto.objects.filter(rodzaj='INNY', arch=False).order_by('typ')
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    return render(request, 'CARS/auto.html',{
        'auta'    : auto,
        'wozki'   : wozki,
        'inny'    : inne,
        'name_log': name_log,
        'about': about,
        'arch' : False
    })


@login_required(login_url='error')
def auta_arch(request):
    auto = Auto.objects.filter(rodzaj='AUTO', arch=True).order_by('typ')
    wozki = Auto.objects.filter(rodzaj='WUWI', arch=True).order_by('typ')
    inne = Auto.objects.filter(rodzaj='INNY', arch=True).order_by('typ')
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    return render(request, 'CARS/auto.html',{
        'auta'    : auto,
        'wozki'   : wozki,
        'inny'    : inne,
        'name_log': name_log,
        'about': about,
        'arch' : True
    })


@login_required(login_url='error')
def auto_add(request):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    if request.method == "POST":
        autof = AutoForm(request.POST or None, request.FILES or None)
        if autof.is_valid():
            ps = autof.save(commit=False)
            ps.save()
            return redirect('auta_start')
        else:
            return redirect('error')
    else:
        autof = AutoForm()
    return  render(request, 'CARS/auto_add.html',{
        'form': autof,
        'name_log':name_log,
        'tytul_okna': "Nowy wpis",
        'edycja':False,
        'pojazd_id':0,
        'about': about
    })


@login_required(login_url='error')
def auto_edit(request, pk):
    autom = get_object_or_404(Auto, pk=pk)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    if request.method == "POST":
        autof = AutoForm(request.POST or None, request.FILES or None, instance=autom)
        if autof.is_valid():
            autof.save()
                #ps = autof.save(commit=False)
                #ps.save()
            return redirect('auta_start')
        else:
            return redirect('error')
    else:
        autof = AutoForm(instance=autom)
    return  render(request, 'CARS/auto_add.html',{
        'form': autof,
        'name_log':name_log,
        'tytul_okna': "Edycja wpisu",
        'edycja':True,
        'pojazd_id':pk,
        'about': about
    })


@login_required(login_url='error')
def auto_delete(request, pk):
    Auto.objects.get(pk=pk).delete()
    return redirect('auta_start')


def auto_export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="auta_wózki_inne.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Auta')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Typ sprzętu', 'Nr rejestracyjny', 'Imię i Nazwisko', 'Opis', 'Data ubezpie.', 'Data przeglądu', 'Nr leasingu', 'Data rozp.', 'Data zakoń.', 'Rata', 'WAL', 'Uwagi',]
    col_width = [30,20,30,30,15,15,20,15,15,15,5,100]
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    #font_style = xlwt.XFStyle()

    rows = Auto.objects.filter(arch=False, rodzaj='AUTO').values_list('typ', 'rej', 'imie_n', 'opis', 'us', 'ps', 'nul', 'drl', 'dzl', 'rul', 'rul_currency', 'uwagi')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if (col_num == 4)or(col_num == 5)or(col_num == 7)or(col_num == 8):
                font_style = xlwt.XFStyle()
                font_style.num_format_str = 'dd.mm.yyyy'
            else:
                font_style = xlwt.XFStyle()
            ws.write(row_num, col_num, row[col_num], font_style)

    ws = wb.add_sheet('Wózki Widłowe')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Typ sprzętu', 'Nr rejestracyjny', 'Imię i Nazwisko', 'Opis', 'Data ubezpie.', 'Data przeglądu', 'Nr leasingu', 'Data rozp.', 'Data zakoń.', 'Rata', 'WAL', 'Uwagi',]
    col_width = [30,20,30,30,15,15,20,15,15,15,5,100]
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    #font_style = xlwt.XFStyle()

    rows = Auto.objects.filter(arch=False, rodzaj='WUWI').values_list('typ', 'rej', 'imie_n', 'opis', 'us', 'ps', 'nul', 'drl', 'dzl', 'rul', 'rul_currency', 'uwagi')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if (col_num == 4)or(col_num == 5)or(col_num == 7)or(col_num == 8):
                font_style = xlwt.XFStyle()
                font_style.num_format_str = 'dd.mm.yyyy'
            else:
                font_style = xlwt.XFStyle()
            ws.write(row_num, col_num, row[col_num], font_style)

    ws = wb.add_sheet('Inne wyposażenie')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Typ sprzętu', 'Nr rejestracyjny', 'Imię i Nazwisko', 'Opis', 'Data ubezpie.', 'Data przeglądu', 'Nr leasingu', 'Data rozp.', 'Data zakoń.', 'Rata', 'WAL', 'Uwagi',]
    col_width = [30,20,30,30,15,15,20,15,15,15,5,100]
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    #font_style = xlwt.XFStyle()

    rows = Auto.objects.filter(arch=False, rodzaj='INNE').values_list('typ', 'rej', 'imie_n', 'opis', 'us', 'ps', 'nul', 'drl', 'dzl', 'rul', 'rul_currency', 'uwagi')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if (col_num == 4)or(col_num == 5)or(col_num == 7)or(col_num == 8):
                font_style = xlwt.XFStyle()
                font_style.num_format_str = 'dd.mm.yyyy'
            else:
                font_style = xlwt.XFStyle()
            ws.write(row_num, col_num, row[col_num], font_style)

    ws = wb.add_sheet('Archiwum')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Typ sprzętu', 'Nr rej./ser.', 'Imię i Nazwisko', 'Opis', 'Data ubezpie.', 'Data przeglądu', 'Nr leasingu', 'Data rozp.', 'Data zakoń.', 'Rata', 'WAL', 'Uwagi',]
    col_width = [30,20,30,30,15,15,20,15,15,15,5,100]
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width[col_num] * 256
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    #font_style = xlwt.XFStyle()

    rows = Auto.objects.filter(arch=True).values_list('typ', 'rej', 'imie_n', 'opis', 'us', 'ps', 'nul', 'drl', 'dzl', 'rul', 'uwagi')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if (col_num == 4)or(col_num == 5)or(col_num == 7)or(col_num == 8):
                font_style = xlwt.XFStyle()
                font_style.num_format_str = 'dd.mm.yyyy'
            else:
                font_style = xlwt.XFStyle()
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
