from django.shortcuts import render, redirect, get_object_or_404
from simple_search import search_filter

from MONIT.views import get_matrix, get_user
from .models import Sprzet, Profil, System, Serwis
from .forms import SprzetForm, ProfilForm, SerwisForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .out_doc import hippdfpp, hippdfpz
from django.conf import settings


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
def hip_start(request):
    tytul = 'Lista sprzętu.'
    sprzety = Sprzet.objects.filter(arch=False, mag=False).order_by('usr')
    systemy = System.objects.all()
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    return render(request, 'HIP/hip_main.html', {
        'sprzety': sprzety,
        'systemy': systemy,
        'name_log': name_log,
        'tytul_tabeli': tytul,
        'admini': test_admin(request),
        'about': about,
    })


@login_required(login_url='error')
def hip_new_s(request):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul = 'Nowy sprzęt.'

    if request.method == "POST":
        sprzetf = SprzetForm(request.POST or None, request.FILES or None)
        if sprzetf.is_valid():
            ps = sprzetf.save(commit=False)
            ps.save()
            return redirect('hip_start')
        else:
            return redirect('error')

    else:
        tst = System.objects.filter(id=1)
        sprzetf = SprzetForm(initial={'sprzet': tst})
    return render(request, 'HIP/hip_new_s.html', {
        'form': sprzetf,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'edycja': False,
        'hip_id_s': 0
    })


@login_required(login_url='error')
def hip_edit_s(request, pk):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul = 'Edycja sprzętu'

    sprzetm = get_object_or_404(Sprzet, pk=pk)
    if request.method == "POST":
        sprzetf = SprzetForm(request.POST or None, request.FILES or None, instance=sprzetm)
        if sprzetf.is_valid():
            ps = sprzetf.save(commit=False)
            ps.save()
            return redirect('hip_start')
        else:
            return redirect('error')

    else:
        sprzetf = SprzetForm(instance=sprzetm)
    return render(request, 'HIP/hip_new_s.html', {
        'form': sprzetf,
        'name_log': name_log,
        'about': about,
        'tytul': tytul,
        'edycja': True,
        'hip_id_s': pk
    })


@login_required(login_url='error')
def hip_delete_s(request, pk):
    Sprzet.objects.get(pk=pk).delete()
    return redirect('hip_start')


@login_required(login_url='error')
def hip_pdf_pp(request, pk):
    return hippdfpp(request, pk)


@login_required(login_url='error')
def hip_pdf_pz(request, pk):
    return hippdfpz(request, pk)


@login_required(login_url='error')
def hip_arch(request):
    tytul = 'Lista sprzętu skasownego, przekazanego lub skanibalizowanego.'
    sprzety = Sprzet.objects.filter(arch=True).order_by('usr')
    systemy = System.objects.all()
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    return render(request, 'HIP/hip_main.html', {
        'sprzety': sprzety,
        'systemy': systemy,
        'name_log': name_log,
        'tytul_tabeli': tytul,
        'admini': test_admin(request),
        'about': about
    })


@login_required(login_url='error')
def hip_mag(request):
    tytul = 'Lista sprzętu skasownego, przekazanego lub skanibalizowanego.'
    sprzety = Sprzet.objects.filter(mag=True, sprzedany=False).order_by('host', 'typ')
    systemy = System.objects.all()
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    return render(request, 'WAREHOUSE/mag_main.html', {
        'sprzety': sprzety,
        'systemy': systemy,
        'name_log': name_log,
        'tytul_tabeli': tytul,
        'admini': test_admin(request),
        'about': about
    })


@login_required(login_url='error')
def hip_edit_m(request, pk):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    tytul = 'Edycja sprzętu.'

    sprzetm = get_object_or_404(Sprzet, pk=pk)
    if request.method == "POST":
        sprzetf = SprzetForm(request.POST or None, request.FILES or None, instance=sprzetm)
        if sprzetf.is_valid():
            ps = sprzetf.save(commit=False)
            ps.save()
            return redirect('hip_mag')
        else:
            return redirect('error')
    else:
        sprzetf = SprzetForm(instance=sprzetm)
    return render(request, 'WAREHOUSE/hip_new_m.html', {
        'form': sprzetf,
        'name_log': name_log,
        'tytul': tytul,
        'about': about
    })


@login_required(login_url='error')
def hip_search(request):
    if request.method == "GET":
        query = request.GET['SZUKAJ']
        systemy = System.objects.all()
        name_log = request.user.first_name + " " + request.user.last_name
        about = settings.INFO_PROGRAM

        if query == '' or query == ' ':
            return redirect('hip_start')
        search_fields = ['nazwa_siec', 'usr', 'typ', 'host', 'adres_ip', 'snk' ]
        f = search_filter(search_fields, query)
        sprzety = Sprzet.objects.filter(f, sprzedany=False, mag=False)

        return render(request, 'HIP/hip_main.html', {
            'systemy': systemy,
            'wybrany': query,
            'name_log': name_log,
            'sprzety': sprzety,
            'admini': test_admin(request),
            'about': about
        })
    else:
        return redirect('hip_start')


@login_required(login_url='error')
def hip_filtr(request, pk):
    systemy = System.objects.all()
    sprzety = Sprzet.objects.filter(system_id=pk, arch=False, mag=False)
    wybrany = System.objects.filter(id=pk)[0]
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    return render(request, 'HIP/hip_main.html', {
        'sprzety': sprzety,
        'systemy': systemy,
        'wybrany': wybrany,
        'name_log': name_log,
        'admini': test_admin(request),
        'about': about
    })

@login_required(login_url='error')
def hip_filtr_s(request, pk):
    systemy = System.objects.all()
    sprzety = Sprzet.objects.filter(host=pk, arch=False, mag=False)
    wybrany = '' #System.objects.filter(id=pk)[0]
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    return render(request, 'HIP/hip_main.html', {
        'sprzety': sprzety,
        'systemy': systemy,
        'wybrany': wybrany,
        'name_log': name_log,
        'admini': test_admin(request),
        'about': about
    })



@login_required(login_url='error')
def hip_detail(request, pk):
    sprzet = Sprzet.objects.filter(id=pk)
    profile = Profil.objects.filter(sprzet_id=pk)
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    return render(request, 'HIP/hip_detail.html', {
        'name_log': name_log,
        'sprzety': sprzet,
        'profile': profile,
        'PK': pk,
        'about': about
    })


@login_required(login_url='error')
def hip_new_p(request, pk):
    tytul = 'Nowy profil'
    naglowek = 'Nowy profil'
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    # sprzet = Sprzet.objects.filter(id=pk)[0]
    if request.method == "POST":
        profilf = ProfilForm(request.POST or None, request.FILES or None)
        if profilf.is_valid():
            ps = profilf.save(commit=False)
            # ps.sprzet = sprzet.id
            ps.save()
            return redirect('hip_detail', pk=pk)
        else:
            return redirect('error')
    else:
        profilf = ProfilForm(initial={'sprzet': pk})
    return render(request, 'HIP/hip_new_p.html', {
        'form': profilf,
        'name_log': name_log,
        'tytul': tytul,
        'naglowek': naglowek,
        'PK': pk,
        'LP': 0,
        'about': about,
        'edycja': False
    })


@login_required(login_url='error')
def hip_edit_p(request, pk, lp):
    tytul = 'Edycja profilu'
    naglowek = 'Edycja profilu'
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    profilm = get_object_or_404(Profil, pk=lp, sprzet=pk)
    if request.method == "POST":
        profilf = ProfilForm(request.POST or None, request.FILES or None, instance=profilm)
        if profilf.is_valid():
            ps = profilf.save(commit=False)

            ps.save()
            return redirect('hip_detail', pk=pk)
        else:
            return redirect('error')
    else:
        profilf = ProfilForm(instance=profilm)
    return render(request, 'HIP/hip_new_p.html', {
        'form': profilf,
        'name_log': name_log,
        'tytul': tytul,
        'naglowek': naglowek,
        'PK': pk,
        'LP': lp,
        'about': about,
        'edycja': True
    })


@login_required(login_url='error')
def hip_delete_p(request, pk, ret):
    Profil.objects.get(pk=pk).delete()
    return redirect('hip_detail', pk=ret)


def hip_lista(request, pk):
    tytul = ''
    query = ''
    profil = ''
    search_fields = ['rodzaj_konta']
    sw_pr = True
    tab_usl = ''
    us = []

    if pk == '1':
        query = 'SDA'
        tytul = 'Lista kont programu SDA'

    if pk == '2':
        query = 'Google DOCS'
        tytul = 'Lista kont Google Docs'

    if pk == '3':
        tytul = 'Uprawnienia'

    if pk != '3':
        f = search_filter(search_fields, query)
        profil = Profil.objects.filter(f).order_by('sprzet__usr')
    else:
        sw_pr = False
        tab_usl = get_matrix()
        us = get_user()

    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    return render(request, 'HIP/hip_main_list.html', {
        'sw_pr': sw_pr,
        'profil': profil,
        'tytul_tabeli': tytul,
        'name_log': name_log,
        'admini': test_admin(request),
        'about': about,
        'tab_usl': tab_usl,
        'us': us
    })


def hip_konta(request, pk):
    search_fields = ['rodzaj_konta', 'adres']

    if pk == '1':
        query = 'VPN PPTP'
        tytul = 'VPN PPTP'

    if pk == '2':
        query = 'VPN OpenVPN'
        tytul = 'VPN OpenVPN'

    if pk == '3':
        query = 'AnyDesk'
        tytul = 'AnyDesk'

    if pk == '4':
        query = 'Teamviewer'
        tytul = 'Teamviewer'

    if pk == '5':
        query = 'RDP'
        tytul = 'RDP'

    if pk == '6':
        query = 'SMB'
        tytul = 'Samba'

    if pk == '7':
        query = 'AFP'
        tytul = 'AFP'

    if pk == '8':
        query = 'iCloud'
        tytul = 'iCloud'

    if pk == '9':
        query = 'Google'
        tytul = 'Google Docs'

    if pk == '10':
        query = 'VPN L2TP'
        tytul = 'VPN L2TP'

    if pk == '11':
        query = 'CRM'
        tytul = 'CRM'

    if pk == '12':
        query = 'poczta'
        tytul = 'Poczta'

    f = search_filter(search_fields, query)
    program = Profil.objects.filter(f)

    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    return render(request, 'HIP/hip_konta.html', {
        'program': program,
        'tytul': tytul,
        'name_log': name_log,
        'about': about
    })

@login_required(login_url='error')
def hip_serwis(request, pk):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    sprzet = Sprzet.objects.filter(id=pk)
    serwis = Serwis.objects.filter(sprzet=pk).order_by('-data', '-id')

    return render(request, 'HIP/hip_detail_ser.html', {
        'name_log': name_log,
        'sprzety': sprzet,
        'serwisy': serwis,
        'PK': pk,
        'about': about
    })


@login_required(login_url='error')
def hip_new_ser(request, pk):
    tytul = 'Nowy wpis sewisowy'
    naglowek = 'Nowy wpis serwisowy'
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM

    if request.method == "POST":
        serwisf = SerwisForm(request.POST or None, request.FILES or None)
        if serwisf.is_valid():
            ps = serwisf.save(commit=False)
            # ps.sprzet = sprzet.id
            ps.save()
            return redirect('hip_serwis', pk=pk)
        else:
            return redirect('error')
    else:
        serwisf = SerwisForm(initial={'sprzet': pk})
    return render(request, 'HIP/hip_new_ser.html', {
        'form': serwisf,
        'name_log': name_log,
        'tytul': tytul,
        'naglowek': naglowek,
        'PK': pk,
        'LP': 0,
        'about': about,
        'edycja': False
    })


@login_required(login_url='error')
def hip_edit_ser(request, pk, lp):
    tytul = 'Edycja pozycji serwisu'
    naglowek = 'Edycja pozycji serwisu'
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    serwism = get_object_or_404(Serwis, pk=lp, sprzet=pk)
    if request.method == "POST":
        serwisf = SerwisForm(request.POST or None, request.FILES or None, instance=serwism)
        if serwisf.is_valid():
            ps = serwisf.save(commit=False)

            ps.save()
            return redirect('hip_serwis', pk=pk)
        else:
            return redirect('error')
    else:
        serwisf = SerwisForm(instance=serwism)
    return render(request, 'HIP/hip_new_ser.html', {
        'form': serwisf,
        'name_log': name_log,
        'tytul': tytul,
        'naglowek': naglowek,
        'PK': pk,
        'LP': lp,
        'about': about,
        'edycja': True
    })
