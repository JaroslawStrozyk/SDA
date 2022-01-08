from django.shortcuts import render, redirect, get_object_or_404
from simple_search import search_filter
from .models import Usluga, Profil
from .forms import UslugaForm, ProfilForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from TaskAPI.cron import ServiceDataTest
from django.conf import settings
from HIP.models import Profil as HProfil


def test_admin(request):
    gr = ''
    admini = False
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        gr = g.name
        # grupy: 	administrator, ksiegowosc, zksiegowosc, spedycja, biuro
    if gr == 'administrator':
        admini = True
    return admini


@login_required(login_url='error')
def ser_start(request):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul = 'Lista usług zewnętrznych.'
    tytul2 = 'Lista licencji czasowych.'

    usluga = Usluga.objects.all().order_by('usr')
    konta = HProfil.objects.all().exclude(data_waznosci=None).order_by('rodzaj_konta')

    ServiceDataTest()

    return render(request, 'SERVICES/ser_main.html', {
        'uslugi': usluga,
        'konta' : konta,
        'name_log': name_log,
        'tytul_tabeli':tytul,
        'tytul_tabeli2': tytul2,
        'admini': test_admin(request),
        'about': about,
    })


@login_required(login_url='error')
def ser_detail(request, pk):

    usluga = Usluga.objects.filter(id=pk)
    profile = Profil.objects.filter(usluga_id=pk)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    return render(request, 'SERVICES/ser_detail.html',{
        'name_log': name_log,
        'uslugi': usluga,
        'profile': profile,
        'PK':pk,
        'about': about
    })


@login_required(login_url='error')
def ser_edit_u(request, pk):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul_tab = 'Edycja usługi.'

    uslugam = get_object_or_404(Usluga, pk=pk)
    if request.method == "POST":
            uslugaf = UslugaForm(request.POST or None, request.FILES or None, instance=uslugam)
            if uslugaf.is_valid():
                ps = uslugaf.save(commit=False)
                if ps.zdj == '':
                    ps.zdj = 'images/brak.png'
                ps.save()
                return redirect('ser_start')
            else:
                return redirect('error')
    else:
            uslugaf = UslugaForm(instance=uslugam)
    return render(request, 'SERVICES/ser_new_u.html',{
        'form': uslugaf,
        'name_log': name_log,
        'about': about,
        'tytul_tab': tytul_tab,
        'edycja': True,
        'ser_id': pk,
    })


@login_required(login_url='error')
def ser_new_u(request):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul_tab = 'Nowa usługa.'

    if request.method == "POST":
            uslugaf = UslugaForm(request.POST or None, request.FILES or None)
            if uslugaf.is_valid():
                ps = uslugaf.save(commit=False)
                if ps.zdj == '':
                    ps.zdj = 'images/brak.png'
                ps.save()
                return redirect('ser_start')
            else:
                return redirect('error')
    else:
            uslugaf = UslugaForm()
    return render(request, 'SERVICES/ser_new_u.html',{
        'form': uslugaf,
        'name_log': name_log,
        'about': about,
        'tytul_tab': tytul_tab,
        'edycja': False,
        'ser_id': 0,
    })


@login_required(login_url='error')
def ser_delete(request, pk):
    Usluga.objects.get(pk=pk).delete()
    return redirect('ser_start')


@login_required(login_url='error')
def ser_new_p(request, pk):

    tytul = 'Nowy profil'
    naglowek = 'Nowy profil'
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    if request.method == "POST":
            profilf = ProfilForm(request.POST or None, request.FILES or None)
            if profilf.is_valid():
                ps = profilf.save(commit=False)
                #ps.sprzet = sprzet.id
                ps.save()
                return redirect('ser_detail', pk=pk)
            else:
                return redirect('error')
    else:
            profilf = ProfilForm(initial={'usluga': pk})
    return render(request, 'SERVICES/ser_new_p.html',{
        'form': profilf,
        'name_log': name_log,
        'tytul': tytul,
        'naglowek': naglowek,
        'PK':pk,
        'about': about,
        'edycja': False,
        'pro_id': 0,
    })


@login_required(login_url='error')
def ser_edit_p(request, pk, lp):

    tytul = 'Edycja profilu'
    naglowek = 'Edycja profilu'
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    profilm = get_object_or_404(Profil, pk=lp, usluga=pk)
    if request.method == "POST":
        profilf = ProfilForm(request.POST or None, request.FILES or None, instance=profilm)
        if profilf.is_valid():
            ps = profilf.save(commit=False)

            ps.save()
            return redirect('ser_detail', pk=pk)
        else:
            return redirect('error')
    else:
        profilf = ProfilForm(instance=profilm)
    return render(request, 'SERVICES/ser_new_p.html',{
        'form': profilf,
        'name_log': name_log,
        'tytul': tytul,
        'naglowek': naglowek,
        'PK': pk,
        'about': about,
        'edycja': True,
        'pro_id': lp,
    })

@login_required(login_url='error')
def pro_delete(request, pk, ret):
    Profil.objects.get(pk=pk).delete()
    return redirect('ser_detail', pk=ret)


@login_required(login_url='error')
def ser_search(request):

    if request.method == "GET":
        query = request.GET['SZUKAJ']
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

        if query == '' or query == ' ':
            return redirect('ser_start')
        search_fields = ['nazwa_siec', 'usr', 'dostawca', 'hosting', 'uwagi' ,'zdj']
        f = search_filter(search_fields, query)
        uslugi = Usluga.objects.filter(f)

        return render(request, 'SERVICES/ser_main.html',{
            'tytul_tabel': query,
            'name_log': name_log,
            'uslugi': uslugi,
            'admini': test_admin(request),
            'about': about
        })
    else:
        return redirect('ser_start')