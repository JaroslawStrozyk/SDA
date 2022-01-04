from datetime import datetime
from .models import  FirmaKasa, RaportKasowy, KwKp



def upgradeLeft(idk):


    li_kw = KwKp.objects.filter(kasa=idk, data=datetime.now(), rodzaj='KW').count()
    li_kp = KwKp.objects.filter(kasa=idk, data=datetime.now(), rodzaj='KP').count()

    doc = KwKp.objects.filter(kasa=idk, data=datetime.now())
    sum_p = 0.00
    sum_r = 0.00
    for d in doc:
        sum_p = sum_p + d.przychod
        sum_r = sum_r + d.rozchod

    id_stan = RaportKasowy.objects.filter(kasa=idk).order_by('-id')[0].id

    trefresh = RaportKasowy.objects.get(id=id_stan)
    trefresh.sum_przychod = sum_p
    trefresh.sum_rozchod = sum_r
    st_ob = trefresh.stan_poprzedni + sum_p - sum_r
    trefresh.stan_obecny = st_ob
    trefresh.kw = li_kw
    trefresh.kp = li_kp
    trefresh.save()

    kasa_ref = FirmaKasa.objects.get(id=idk)
    kasa_ref.stan = st_ob
    kasa_ref.save()

    return id_stan

def calcAll(idk):

    kasa_ref = FirmaKasa.objects.get(id=idk)
    kasa_ref.stan = kasa_ref.bo
    kasa_ref.save()

    rapkas = RaportKasowy.objects.filter(kasa=idk).order_by('data')

    for rk in rapkas:
        li_kw = KwKp.objects.filter(kasa=idk, data=rk.data, rodzaj='KW').count()
        li_kp = KwKp.objects.filter(kasa=idk, data=rk.data, rodzaj='KP').count()
        doc = KwKp.objects.filter(kasa=idk, data=rk.data)
        sum_p = 0.00
        sum_r = 0.00
        for d in doc:
            sum_p = sum_p + d.przychod
            sum_r = sum_r + d.rozchod
        rk.kw = li_kw
        rk.kp = li_kp
        rk.sum_przychod = sum_p
        rk.sum_rozchod = sum_r
        rk.save()

    wmkw = 0
    wmkp = 0
    sw = True
    for rk in rapkas:
        if sw==True:
            so = FirmaKasa.objects.filter(id=idk)[0].stan
            rk.stan_poprzedni = so
            rk.stan_obecny = so
            sw = False
        wmkw = wmkw + rk.kw
        wmkp = wmkp + rk.kp
        rk.mkw = wmkw
        rk.mkp = wmkp
        rk.save()

    sw = False
    stan = 0
    for rk in rapkas:
        if sw==True:
            rk.stan_poprzedni = stan
        sw = True
        stan = rk.stan_poprzedni + rk.sum_przychod - rk.sum_rozchod
        rk.stan_obecny = stan
        rk.save()

    kasa_ref = FirmaKasa.objects.get(id=idk)
    kasa_ref.stan = stan
    kasa_ref.save()

def intstr_month(amc):
    pmc = ''
    if amc == '01' or amc=='1':
        pmc = 'Styczeń'
    if amc == '02' or amc=='2':
        pmc = 'Luty'
    if amc == '03' or amc=='3':
        pmc = 'Marzec'
    if amc == '04' or amc=='4':
        pmc = 'Kwiecień'
    if amc == '05' or amc=='5':
        pmc = 'Maj'
    if amc == '06' or amc=='6':
        pmc = 'Czerwiec'
    if amc == '07' or amc=='7':
        pmc = 'Lipiec'
    if amc == '08' or amc=='8':
        pmc = 'Sierpień'
    if amc == '09' or amc=='9':
        pmc = 'Wrzesień'
    if amc == '10':
        pmc = 'Październik'
    if amc == '11':
        pmc = 'Listopad'
    if amc == '12':
        pmc = 'Grudzień'
    return pmc