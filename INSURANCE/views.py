from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from simple_search import search_filter
from .models import Ubezpieczenie, Termin
from .forms import UbezpieczenieForm, TerminForm
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required(login_url='error')
def ub_start(request):

    ubp  = Ubezpieczenie.objects.all().order_by('data_do')
    term = Termin.objects.all().order_by('data_do')
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    return render(request, 'INSURANCE/ubp.html',{
        'ubp'      : ubp,
        'term'     : term,
        'name_log' : name_log,
        'about'    : about
    })


@login_required(login_url='error')
def ub_add(request):
    tytul = "Nowe ubezpieczenie"
    mtytul = tytul
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    if request.method == "POST":
        ubf = UbezpieczenieForm(request.POST or None, request.FILES or None)
        if ubf.is_valid():
            post = ubf.save(commit=False)
            post.save()
            return redirect('ub_start')
    else:
        ubf = UbezpieczenieForm()

    return render(request, 'INSURANCE/ubp_add.html', {
        'ubf':ubf,
        'name_log':name_log,
        'tytul': tytul,
        'mtytul':mtytul,
        'about': about,
        'edycja': False,
        'ub_id': 0
    })


@login_required(login_url='error')
def ub_edit(request, pk):

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
    return render(request, 'INSURANCE/ubp_add.html', {
        'ubf':ubf,
        'name_log':name_log,
        'tytul': tytul,
        'mtytul':mtytul,
        'about': about,
        'edycja': True,
        'ub_id': pk
    })


@login_required(login_url='error')
def ub_delete(request, pk):
    Ubezpieczenie.objects.get(pk=pk).delete()
    return redirect('ub_start')


@login_required(login_url='error')
def ubt_add(request):
    tytul = "Nowy termin ubezpieczenia"
    mtytul = tytul
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    if request.method == "POST":
        ubf = TerminForm(request.POST or None, request.FILES or None)
        if ubf.is_valid():
            post = ubf.save(commit=False)
            post.save()
            return redirect('ub_start')
    else:
        ubf = TerminForm()

    return render(request, 'INSURANCE/ubpt_add.html', {
        'ubf':ubf,
        'name_log':name_log,
        'tytul': tytul,
        'mtytul':mtytul,
        'about': about,
        'edycja': False,
        'ub_id': 0
    })


@login_required(login_url='error')
def ubt_edit(request, pk):
    ubfa = get_object_or_404(Termin, pk=pk)
    if request.method == "POST":
        ubf = TerminForm(request.POST or None, request.FILES or None, instance=ubfa)
        if ubf.is_valid():
            post = ubf.save(commit=False)
            post.save()
            return redirect('ub_start')
    else:
        ubf = TerminForm(instance=ubfa)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    tytul = "Edycja terminu ubezpieczenia"
    mtytul = tytul
    return render(request, 'INSURANCE/ubpt_add.html', {
        'ubf':ubf,
        'name_log':name_log,
        'tytul': tytul,
        'mtytul':mtytul,
        'about': about,
        'edycja': True,
        'ub_id': pk
    })


@login_required(login_url='error')
def ubt_delete(request, pk):
    Termin.objects.get(pk=pk).delete()
    return redirect('ub_start')


