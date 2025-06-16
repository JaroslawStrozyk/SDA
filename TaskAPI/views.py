from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from COMP_REPO.functions import set_multi_calc, CalAllCost
from COMP_REPO.models import Sklad
from COMP_REPO_NEW.calc_func import AllSkladRecalculate
from TIMBER_WH.calc_data import rozlicz_rozchod, test_rozlicz_rozchod
from TIMBER_WH.functions import Cal_All_Poz
from TIMBER_WH.models import Rozchod
from TIMBER_WH.views import generuj_raport_konsola
from .cron import SDA_SDEtoGS, test_email
from .forms import PDFForm
from .functions import get_user_label
from .models import  URok, Ustawienia
from django.conf import settings
from django.contrib.auth.decorators import login_required
import datetime
from WORKER.functions import test_rok
from django.http import JsonResponse, HttpResponse
from .models import Katalog, Plik
from .pdf import out_pdf_doc


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()]) + '.'
    return name_log, inicjaly


def start(request):
    return render(request, 'SDA/login.html', )

# class CustomLogoutView(LogoutView):
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)


def upgrade_sklad():
    for s in Sklad.objects.all():
        if len(s.faktura) > 0:
            s.blokada = True
            print(">>>", s.id, 'True')
        else:
            s.blokada = False
            print(">>>", s.id, 'False')
        s.save()


def refresh(request):
    AllSkladRecalculate()
    # test_email()
    #SDA_SDEtoGS(2025, 'TEST')
    #Cal_All_Poz()
    #test_rozlicz_rozchod()

    #generuj_raport_konsola()
    #CalAllCost()
    #set_multi_calc()
    #Cal_All_States()
    return redirect('desktop')


@login_required(login_url='error')
def task(request):
    name_log, inicjaly = test_osoba(request)
    lata, rok, brok, bmc = test_rok(request)

    # Przełaczanie widoków
    lan = False
    hip = False
    hip1 = False
    usl = False
    mag = False
    tel = False
    rka = False
    fak = False
    ube = False
    dlg = False
    dow = False
    sam = False
    zam = False
    zal = False
    kod = False
    gog = False
    emp = False
    emp1 = False
    tmb = False
    mag_int = False
    przech = False
    logs = False
    monit = False

    gr = ''
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        gr = g.name

    if gr == 'administrator':
        lan = True
        hip = True
        hip1 = True
        usl = True
        mag = True
        tel = True
        rka = True
        fak = True
        ube = True
        dlg = True
        dow = True
        sam = True
        zam = True
        zal = True
        kod = True
        gog = True
        emp = True
        emp1 = True
        tmb = True
        mag_int = True
        przech = True
        logs = True
        monit = True
    elif gr == 'ksiegowosc':
        rka = True
        hip1 = True
        fak = True
        ube = True
        dlg = True
        dow = True
        zam = True
        zal = True
        kod = True
        gog = True
        emp = True
        emp1 = True
        sam = True
        tmb = True
        mag_int = True
        przech = True
    elif gr == 'ksiegowosc1':
        fak = True
        ube = True
        dlg = True
        zam = True
        zal = True
        kod = True
        sam = True
    elif gr == 'spedycja':
        dow = True
        zam = True
    elif gr == 'biuro':
        hip = True
        mag = True
        tel = True
        sam = True
        dow = True
        dlg = True
        zam = True
        zal = True
        kod = True
        tmb = True
        mag_int = True
        przech = True
    elif gr == 'stolarnia':
        zal = True
        zam = True
    elif gr == 'produkcja':
        dlg = True
        tmb = True
        mag_int = True
        przech = True
    elif gr == 'kierownik':
        emp1 = True
        tmb = True
        mag_int = True
        dlg = True
        przech = True
    elif gr == 'kontrola':
        zam = True
        kod = True
        gog = True
        tmb = True
        mag_int = True
        przech = True
    elif gr == 'magazyn':
        tmb = True
        mag_int = True
        przech = True
        dlg = True
    elif gr == 'magazyn1':
        tmb = True
        mag_int = True
        przech = True
    elif gr == 'magazyn2':
        tmb = True
    elif gr == 'magazyn2a':
        mag_int = True
    elif gr == 'skład':
        przech = True

    if inicjaly == 'A.S.':
        przech = True



    ur = URok.objects.filter(nazwa=inicjaly)
    if len(ur) == 0:
        URok.objects.create(nazwa=inicjaly, rok=datetime.datetime.now().strftime("%Y"))

    about = settings.INFO_PROGRAM
    # print("!!!", about[0].get("WERSJA"))
    set = Ustawienia.objects.all().order_by('co')

    return render(request, 'SDA/dashboard.html',
                  {
                      'name_log': get_user_label(request),
                      'date_log': request.user.last_login,
                      'lan': lan,
                      'hip': hip,
                      'hip1': hip1,
                      'usl': usl,
                      'mgz': mag,
                      'tel': tel,
                      'rka': rka,
                      'fak': fak,
                      'ube': ube,
                      'dlg': dlg,
                      'dow': dow,
                      'sam': sam,
                      'zam': zam,
                      'zal': zal,
                      'kod': kod,
                      'gog': gog,
                      'emp': emp,
                      'emp1': emp1,
                      'tmb': tmb,
                      'mag_int': mag_int,
                      'przech': przech,
                      'logs': logs,
                      'monit': monit,
                      'about': about,
                      'set': set,
                      'bmc': bmc,
                      'brok': brok
                  })


# def doc_view(request):
#     return render(request, 'SDA/doc_view.html',{})


def error(request):
    return render(request, 'SDA/404.html', )


def log(request):
    if request.user.is_authenticated:
        name_log = get_user_label(request)
        lista_logi = '' # Log.objects.all().order_by('-data')

        paginator = Paginator(lista_logi, 50)
        strona = request.GET.get('page')
        logi = paginator.get_page(strona)

        return render(request, 'SDA/log.html', {'name_log': name_log, 'logi': logi})
    else:
        return redirect('error')


def katalogi_view(request):
    katalogi = Katalog.objects.all()
    return render(request, 'SDA/doc_view.html', {'katalogi': katalogi})


def pliki_view(request, katalog_id):
    pliki = Plik.objects.filter(katalog_id=katalog_id)
    pliki_data = {
        'pdf': [{'nazwa': plik.nazwa, 'dokument': plik.dokument.url} for plik in pliki if plik.dokument],
        'no_pdf': [{'id': plik.id, 'nazwa': plik.nazwa} for plik in pliki if not plik.dokument],
    }
    return JsonResponse(pliki_data, safe=False)

def pliki_pdf(request, id):
    plik = get_object_or_404(Plik, pk=id)

    # Oświadczenie
    if id in [4, 5]:
        mid = ''
        iin = ''
        pesel = ['', '', '', '', '', '', '', '', '', '', '']
        mc = ''
        kw = ''

        fl = plik.form

        if fl:
            if request.method == 'POST':
                form = PDFForm(request.POST)
                if form.is_valid():
                    mid = form.cleaned_data['mid']
                    iin = form.cleaned_data['iin']
                    pesel = list(form.cleaned_data['pesel'])
                    mc = form.cleaned_data['mc']
                    kw = form.cleaned_data['kw']
                else:
                    return render(request, 'SDA/doc_form.html', {'form': form})
            else:
                form = PDFForm()
                return render(request, 'SDA/doc_form.html', {'form': form})

        return out_pdf_doc(request, plik.nazwa, mid, iin, pesel, mc, kw, fl)


    else:
        return HttpResponse(f"Plik: [{plik.nazwa}] ID: [{plik.id}]")

