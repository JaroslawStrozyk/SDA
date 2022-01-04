from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from simple_search import search_filter
from .models import Ubezpieczenie
from .forms  import UbezpieczenieForm
from django.conf import settings


def ub_start(request):
    if request.user.is_authenticated:
        ubp = Ubezpieczenie.objects.all().order_by('dado')
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

        return render(request, 'INSURANCE/ubp.html',{'ubp': ubp,  'name_log':name_log, 'about': about})
    else:
        return redirect('error')


def ub_add(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            ubf = UbezpieczenieForm(request.POST or None, request.FILES or None)
            if ubf.is_valid():
                post = ubf.save(commit=False)
                post.save()
                return redirect('ub_start')
        else:
            ubf = UbezpieczenieForm()
        tytul = "Nowe ubezpieczenie"
        mtytul = tytul
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

        return render(request, 'INSURANCE/ubp_add.html', {'ubf':ubf, 'name_log':name_log, 'tytul': tytul, 'mtytul':mtytul, 'about': about})
    else:
        return redirect('error')


def ub_edit(request, pk):
    if request.user.is_authenticated:

        ubfa = get_object_or_404(Ubezpieczenie, pk=pk)
        if request.method == "POST":
            ubf = UbezpieczenieForm(request.POST or None, request.FILES or None, instance=ubfa)
            if ubf.is_valid():
                post = ubf.save(commit=False)
                post.save()
                return redirect('ub_start')
        else:
            ubf = UbezpieczenieForm(instance=ubfa)
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

        tytul = "Edycja ubezpieczenia"
        mtytul = tytul
        return render(request, 'INSURANCE/ubp_add.html', {'ubf':ubf, 'name_log':name_log, 'tytul': tytul, 'mtytul':mtytul, 'about': about})
    else:
        return redirect('error')

