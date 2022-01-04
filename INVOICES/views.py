from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from simple_search import search_filter
from .models import Faktura
from django.conf import settings
from .forms  import FakturaForm, EFakturaForm

import datetime

def faktura_start(request):
    if request.user.is_authenticated:
        lista_faktury = Faktura.objects.all().order_by('zrobione','-data')
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

        paginator = Paginator(lista_faktury, 30)
        strona = request.GET.get('page')
        faktury = paginator.get_page(strona)

        return render(request, 'INVOICES/faktura.html', {'faktury': faktury, 'name_log': name_log, 'about': about})
    else:
        return redirect('error')


def faktura_add(request):
    if request.method == "POST":
        delf = FakturaForm(request.POST)
        if delf.is_valid():
            post = delf.save(commit=False)
            post.zrobione = False
            post.sig_source = False
            post.save()
            return redirect('login')
    else:
        delf = FakturaForm()
    return render(request, 'INVOICES/faktura_add.html', {'form':delf,})


def faktura_edit(request, pk):
    if request.user.is_authenticated:
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

        delfa = get_object_or_404(Faktura, pk=pk)
        if request.method == "POST":
            delf = EFakturaForm(request.POST or None, instance=delfa)
            if delf.is_valid():
                post = delf.save(commit=False)
                post.sig_source = True
                post.save()
                return redirect('faktura_start')
        else:
            delf = EFakturaForm(instance=delfa)
        return render(request, 'INVOICES/faktura_edit.html', {'form':delf,'name_log': name_log, 'about': about})
    else:
        return redirect('error')


def faktura_search(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            query = request.GET['SZUKAJ']
            name_log = request.user.first_name + " " + request.user.last_name
            about = settings.INFO_PROGRAM

            if query == '' or query == ' ':
                return redirect('faktura_start')
            search_fields = ['imie', 'nazwisko', 'targi']
            f = search_filter(search_fields, query)
            delegacje = Faktura.objects.filter(f)


            return render(request, 'INVOICES/faktura_filtr.html',{'delegacje': delegacje,'wybrany': query,'name_log': name_log, 'about': about})
        else:
            return redirect('faktura_start')
    else:
        return redirect('error')

