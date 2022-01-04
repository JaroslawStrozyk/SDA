from django.shortcuts import render, redirect
from simple_search import search_filter
from .models import Dowod
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required(login_url='error')
def dowod_start(request):
    dow = Dowod.objects.all().order_by('nazwisko')
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    tytul = "Dowody osobiste"
    przycisk = False
    return render(request, 'ID_CARDS/dowody.html',{
       'dowody': dow,
       'name_log':name_log,
       'tytul':tytul,
       'przycisk': przycisk,
       'about': about
    })


@login_required(login_url='error')
def dowod_search(request):
    if request.method == "GET":
        query = request.GET['SZUKAJ']

        if query == '' or query == ' ':
            return redirect('dowod_start')
        search_fields = ['imie', 'nazwisko']
        f = search_filter(search_fields, query)
        dow = Dowod.objects.filter(f)
        tytul = "Dowody osobiste [Filtr: "+ query+" ]"
        name_log = request.user.first_name + " " + request.user.last_name
        #about = settings.INFO_PROGRAM
        przycisk = True
        return render(request, 'ID_CARDS/dowody.html', {
            'dowody': dow,
            'name_log': name_log,
            'tytul': tytul,
            'przycisk': przycisk,
            #'about': about
        })
    else:
        return redirect('dowod_start')
