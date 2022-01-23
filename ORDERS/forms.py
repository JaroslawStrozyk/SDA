from django import forms
from TaskAPI.models import Rok
from .models import NrSDE, NrMPK, Zamowienie
import datetime


YEARS= [x for x in range(2009,2032)]

def test_rok():
    tst  = Rok.objects.all().order_by('rok')
    rok  = 0
    for t in tst:
        if t.flg == 1:
            rok = t.rok
    return rok

class NrSDEForm(forms.ModelForm):
    class Meta:
        model = NrSDE
        fields = (
            'nazwa','klient', 'targi', 'opis', 'rks', 'mcs', 'pm',  'uwagi'
        )



class ZamowienieForm(forms.ModelForm):

    class Meta:
        model = Zamowienie
        fields = (
            'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_sde', 'nr_mpk',
            'nr_dok1', 'zal1', 'nr_dok2', 'zal2', 'nr_dok3', 'zal3', 'kwota_brutto', 'data_zam', 'data_dost',
            'data_fv', 'nr_fv', 'roz', 'uwagi'
        )



    def __init__(self, *args, **kwargs):
        rok = kwargs.pop('rok')
        super().__init__(*args, **kwargs)

        try:
            self.fields['nr_sde'].queryset = NrSDE.objects.all().order_by('nazwa') # filter(rok=rok)
        except:
            self.fields['nr_sde'].queryset = NrSDE.objects.none()

        try:
            self.fields['nr_mpk'].queryset = NrMPK.objects.filter(rok=rok).order_by('nazwa')
        except:
            self.fields['nr_pmk'].queryset = NrMPK.objects.none()






