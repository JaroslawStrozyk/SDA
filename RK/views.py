from django.shortcuts import render, redirect, get_object_or_404
from .models import  FirmaKasa, RaportKasowy, KwKp, Waluta
from .forms import  FirmaKasaForm, KwKpForm
from datetime import datetime
from datetime import timedelta
from TaskAPI.functions import get_user_label, trans_month
from RK.functions import upgradeLeft, calcAll, intstr_month
from django.contrib.auth.models import Group
from .out_doc import smrk_pdf, mrk_pdf, drk_pdf, kwkp_pdf
from django.conf import settings

waluta = ''

def smrkpdf(request, mc, idk): # 16.06.2019
    return smrk_pdf(mc, idk)

def mrkpdf(request, mc, idk):
    return mrk_pdf(mc, idk)

def drkpdf(request, dt, idk): # 16.06.2019
    return drk_pdf(dt, idk)

def kwkppdf(request, pk, idk):
    return kwkp_pdf(request, pk, idk)

def rk_start(request):
    if request.user.is_authenticated:
        name_log  = get_user_label(request)

        tytul     = 'Raporty kasowe'
        kasa_name = 'Firmy & Kasy'
        firmy = FirmaKasa.objects.filter(rodzaj='KO').order_by('id')
        zfirmy = FirmaKasa.objects.filter(rodzaj='KZ').order_by('id')

        query_set = Group.objects.filter(user=request.user)
        for g in query_set:
            gr = g.name
            # grupy: 	administrator, ksiegowosc, zksiegowosc, spedycja, biuro

        zkasa = False

        if gr == 'administrator':
            zkasa = True

        if gr == 'zksiegowosc':
            zkasa = True

        waluty = Waluta.objects.all()

        return render(request,
                   'RK/rk.html', {
                       'name_log' : name_log,
                       'tytul'    : tytul,
                       'kasa_name': kasa_name,
                       'firmy'    : firmy,
                       'zfirmy'   : zfirmy,
                       'zkasa'    : zkasa,
                       'waluty'   : waluty,
                       'gr'       : gr,
                       'about': settings.INFO_PROGRAM
                   })
    else:
        return redirect('error')


def rk_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            firmy = FirmaKasaForm(request.POST)
            if firmy.is_valid():
                ps = firmy.save(commit=False)
                ps.save()
                return redirect('rk_start')
            else:
                return redirect('error')
        else:
            name_log = get_user_label(request)

            tytul = ''
            kasa_name = 'Dodaj firmę i kasę'
            firmy = FirmaKasaForm()

            return render(request,
                          'RK/rk_new.html', {
                              'name_log': name_log,
                              'tytul': tytul,
                              'kasa_name': kasa_name,
                              'firmy': firmy,
                              'about': settings.INFO_PROGRAM
                          })
    else:
        return redirect('error')


def rk_edit(request, pk):
    if request.user.is_authenticated:
        firmym = get_object_or_404(FirmaKasa, pk=pk)
        if request.method == "POST":
            firmy = FirmaKasaForm(request.POST or None, instance=firmym)
            if firmy.is_valid():
                ps = firmy.save(commit=False)
                ps.save()
                return redirect('rk_start')
            else:
                return redirect('error')
        else:
            name_log = get_user_label(request)

            tytul = ''
            kasa_name = 'Edytuj firmę i kasę'
            firmy = FirmaKasaForm(instance=firmym)

        return render(request,
                          'RK/rk_new.html', {
                              'name_log': name_log,
                              'tytul': tytul,
                              'kasa_name': kasa_name,
                              'firmy': firmy,
                              'about': settings.INFO_PROGRAM
                          })
    else:
        return redirect('error')


def updlrk(request, idk, dd, mm, rrrr):
    kwkp_dzis = KwKp.objects.filter(kasa=idk, data__month=mm, data_year=rrrr, data_day=dd)
    dd1 = str(int(dd)-1)
    #rapkas_poprz = RaportKasowy.objects.filter(kasa=idk, data__month=mm, data_year=rrrr, data_day=dd1)
    #RaportKasowy.objects.filter(kasa=idk).order_by('-data')[0].stan_obecny

    return redirect('lrk', idk=idk)


def uplrk(request, idk):
    #calcAll(idk)
    return redirect('lrk', idk=idk)


def lrk(request, idk): # 15.05
    if request.user.is_authenticated:

        waluta = FirmaKasa.objects.filter(id=idk)[0].bo
        waluta = waluta - waluta

        d = datetime.now()
        mc = d.strftime("%m")

        ilosc = RaportKasowy.objects.filter(kasa=idk, data__month=mc).count()
        if ilosc>0:
            ldata = RaportKasowy.objects.filter(kasa=idk).order_by('-data')[0].data
        else:
            ldata = datetime.now() - timedelta(days=1)
        cdata = datetime.now()

        if cdata.strftime('%Y-%m-%d') != ldata.strftime('%Y-%m-%d'): # Jeśli nie równe to trzeba założyc nowy raport
            ikw = 0
            ikp = 0
            if ilosc>0:
                so  = RaportKasowy.objects.filter(kasa=idk).order_by('-data')[0].stan_obecny
                ikw = RaportKasowy.objects.filter(kasa=idk).order_by('-data')[0].mkw
                ikp = RaportKasowy.objects.filter(kasa=idk).order_by('-data')[0].mkp
            else:
                so = FirmaKasa.objects.filter(id=idk)[0].stan

            ins = RaportKasowy(kasa_id=idk, stan_poprzedni=so, stan_obecny=so, mkw=ikw, mkp=ikp, sum_rozchod=waluta, sum_przychod=waluta)
            ins.save()

        rk = RaportKasowy.objects.filter(kasa=idk, data__month=mc).order_by('-data')
        tytul = FirmaKasa.objects.filter(id=idk)[0]
        id_kasa = idk
        naglowek = 'Lista dziennych raportów kasowych za miesiąc ' + trans_month(d.strftime("%B"))

        miesiac = []
        m_c = mc
        mc = int(mc)
        while mc > 0:
            ilosc = RaportKasowy.objects.filter(kasa=idk, data__month=str(mc)).count()
            if ilosc > 0:
                miesiac.append(mc)

            mc = mc - 1

        return render(request,
                  'RK/lrk.html', {
                      'name_log': get_user_label(request),
                      'tytul': tytul,
                      'naglowek': naglowek,
                      'rk': rk,
                      'id_kasa': id_kasa,
                      'miesiac': miesiac,
                      'm_c':  m_c,
                      'about': settings.INFO_PROGRAM
                  })
    else:
        return redirect('error')


def lrk_old(request, idk, mc):
    if request.user.is_authenticated:
        m_c = mc
        rk = RaportKasowy.objects.filter(kasa=idk, data__month=m_c).order_by('-data')
        tytul = FirmaKasa.objects.filter(id=idk)[0]
        id_kasa = idk

        naglowek = 'Lista dziennych raportów kasowych za miesiąc ' + intstr_month(m_c) #intstr_month(mc)

        d = datetime.now()
        mc = d.strftime("%m")
        miesiac = []
        #m_c = mc
        mc = int(mc)
        while mc > 0:
            ilosc = RaportKasowy.objects.filter(kasa=idk, data__month=str(mc)).count()
            if ilosc > 0:
                miesiac.append(mc)

            mc = mc - 1


        return render(request,
                  'RK/lrk_old.html', {
                      'name_log': get_user_label(request),
                      'tytul': tytul,
                      'naglowek': naglowek,
                      'rk': rk,
                      'id_kasa': id_kasa,
                      'miesiac': miesiac,
                      'm_c':  m_c,
                      'about': settings.INFO_PROGRAM
                  })
    else:
        return redirect('error')


def lrk_arch(request, idrk, idk):
    if request.user.is_authenticated:
        name_log = get_user_label(request)
        tytul = 'Lista raportów kasowych - Archiwum'
        naglowek = str(FirmaKasa.objects.filter(id=idk)[0])
        nazwa_rap = RaportKasowy.objects.get(id=idrk, kasa_id=idk)
        naglowek = naglowek + '   =>   RAPORT KASOWY: '+ str(nazwa_rap.data)
        id_kasa = idk
        rk = KwKp.objects.filter(data=nazwa_rap.data, kasa_id=idk).order_by('-data')
        return render(request,
                  'RK/lrk_arch.html', {
                      'name_log': name_log,
                      'tytul': tytul,
                      'naglowek': naglowek,
                      'rk': rk,
                      'idkas': id_kasa,
                      'about': settings.INFO_PROGRAM
                  })
    else:
        return redirect('error')


def kwkp(request, idk):
    if request.user.is_authenticated:

        name_log = get_user_label(request)
        tytul = 'Lista wpisów KP, KW'
        naglowek = 'Dokumenty: ' + FirmaKasa.objects.filter(id=idk)[0].nazwa +', '+ FirmaKasa.objects.filter(id=idk)[0].kasa

        idkas = idk

        id_stan = upgradeLeft(idk)

        stankasy = RaportKasowy.objects.filter(id=id_stan)
        doc = KwKp.objects.filter(kasa=idk, data=datetime.now())


        return render(request,
                      'RK/kwkp.html', {
                          'name_log': name_log,
                          'tytul': tytul,
                          'naglowek': naglowek,
                          'stankasy': stankasy,
                          'docr': doc,
                          'idkas':idkas,
                          'about': settings.INFO_PROGRAM
                      })
    else:
        return redirect('error')


def kwkp_new(request, idk): # 15.05
    if request.user.is_authenticated:

        waluta = FirmaKasa.objects.filter(id=idk)[0].bo
        waluta = waluta - waluta

        name_log = get_user_label(request)
        kasa_name = FirmaKasa.objects.filter(id=idk)[0]

        if request.method == "POST":
            kwkpf = KwKpForm(request.POST)
            if kwkpf.is_valid():
                post = kwkpf.save(commit=False)
                fk = FirmaKasa.objects.get(id=idk)
                post.kasa_id = fk.id

                id_stan = RaportKasowy.objects.filter(kasa=idk).order_by('-id')[0].id
                rrk = RaportKasowy.objects.get(id=id_stan)

                dd = request.POST['rodzaj']
                sw = float(request.POST['switch_0'])

                if dd=='KW':
                    post.rozchod = sw

                if dd=="KP":
                    post.przychod = sw

                num = 0
                if dd=='KW':
                        rrk.kw = rrk.kw + 1
                        num = rrk.mkw + 1
                        rrk.mkw = num
                if dd=='KP':
                        rrk.kp = rrk.kp + 1
                        num = rrk.mkp + 1
                        rrk.mkp = num
                post.numer = num
                post.save()
                rrk.save()
                return redirect('kwkp', idk=idk)
            else:
                return redirect('error')
        else:
            kwkpf = KwKpForm(initial={'przychod':waluta,'rozchod': waluta,'switch': waluta})
            return render(request,'RK/kwkp_add.html', {
                'kwkp': kwkpf,
                'name_log': name_log,
                'kasa_name': kasa_name,
                'idkas': idk,
                'about': settings.INFO_PROGRAM
            })
    else:
         return redirect('error')


def kwkp_edit(request, idk, pk):
    if request.user.is_authenticated:

        name_log = get_user_label(request)
        kasa_name = FirmaKasa.objects.filter(id=idk)[0]

        kwkpm = get_object_or_404(KwKp, pk=pk)

        if request.method == "POST":
            kwkpf = KwKpForm(request.POST, instance=kwkpm)
            if kwkpf.is_valid():
                post = kwkpf.save(commit=False)
                post.save()

                #calcAll(idk) # !!!
                return redirect('kwkp', idk=idk)
            else:
                return redirect('error')
        else:
            kwkpf = KwKpForm(instance=kwkpm)
            return render(request,
                          'RK/kwkp_edit.html', {
                          'kwkp': kwkpf,
                          'name_log': name_log,
                          'kasa_name': kasa_name,
                          'idkas': idk,
                          'about': settings.INFO_PROGRAM
                          })
    else:
        return redirect('error')

def kwkp_count (request, idk, mc, rok):

    return ''
