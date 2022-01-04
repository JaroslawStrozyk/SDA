from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from simple_search import search_filter
from .models import Delegacja
from .forms  import DelegacjaForm, EDelegacjaForm
from django.conf import settings


def delegacja_lista(request):
    if request.user.is_authenticated:
        lista_delegacje = Delegacja.objects.all().order_by('zrobione','-data_od')
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

        paginator = Paginator(lista_delegacje, 30)
        strona = request.GET.get('page')
        delegacje = paginator.get_page(strona)

        return render(request, 'DELEGATIONS/delegacja.html', {'delegacje': delegacje, 'name_log': name_log, 'about': about})
    else:
        return redirect('error')



def delegacja_add(request):
    if request.method == "POST":
        delf = DelegacjaForm(request.POST)
        if delf.is_valid():
            post = delf.save(commit=False)
            post.zrobione = False
            post.save()
            return redirect('login')
    else:
        delf = DelegacjaForm()
    return render(request, 'DELEGATIONS/delegacja_add.html', {'form':delf,})


def delegacja_edit(request, pk):
    if request.user.is_authenticated:
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

        delz = get_object_or_404(Delegacja, pk=pk)
        if request.method == "POST":
            delf = EDelegacjaForm(request.POST or None, instance=delz)
            if delf.is_valid():
                post = delf.save(commit=False)
                post.save()
                return redirect('delegacja_lista')
        else:
            delf = EDelegacjaForm(instance=delz)
        return render(request, 'DELEGATIONS/delegacja_edit.html', {'form':delf,'name_log': name_log, 'about': about})


    else:
        return redirect('error')


def delegacja_search(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            query = request.GET['SZUKAJ']
            name_log = request.user.first_name + " " + request.user.last_name
            about = settings.INFO_PROGRAM

            if query == '' or query == ' ':
                return redirect('delegacja_lista')
            search_fields = ['imie', 'nazwisko', 'targi']
            f = search_filter(search_fields, query)
            delegacje = Delegacja.objects.filter(f)


            return render(request, 'DELEGATIONS/delegacja_filtr.html',{'delegacje': delegacje,'wybrany': query,'name_log': name_log, 'about': about})
        else:
            return redirect('delegacja_lista')
    else:
        return redirect('error')