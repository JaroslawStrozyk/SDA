
from django import forms
from TaskAPI.models import Rok
from .models import NrSDE, NrMPK, Zamowienie

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab

from datetime import date


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
            'nazwa','klient', 'targi', 'stoisko', 'opis', 'rks', 'mcs', 'pm',  'uwagi', 'pow_stoisko', 'pow_pietra'
        )


class ZamowienieForm(forms.ModelForm):
    flaga = 0
    flaga_s = 0
    flaga_m = 0
    rok_t = 0

    class Meta:
        model = Zamowienie
        fields = (
            'opis', 'kontrahent', 'wartosc_zam', 'nr_zam', 'sposob_plat', 'rodzaj_plat', 'nr_sde', 'nr_mpk',
            'nr_dok1', 'zal1', 'zal1_bi', 'nr_dok2', 'zal2', 'zal2_bi', 'nr_dok3', 'zal3', 'zal3_bi', 'kwota_brutto',
            'data_zam', 'data_dost', 'data_fv', 'nr_fv', 'roz', 'uwagi', 'flaga_sz', 'nip', 'nip_ind'
        )


    def __init__(self, *args, **kwargs):
        rok = kwargs.pop('rok')
        super().__init__(*args, **kwargs)

        self.rok_t = rok

        try:
            self.fields['nr_sde'].queryset = NrSDE.objects.all().order_by('nazwa') # filter(rok=rok)
        except:
            self.fields['nr_sde'].queryset = NrSDE.objects.none()

        try:
            self.fields['nr_mpk'].queryset = NrMPK.objects.filter(rok=rok).order_by('nazwa') #rok__gte=2022
        except:
            self.fields['nr_pmk'].queryset = NrMPK.objects.none()


    def clean_nr_sde(self):
        n_sde = self.cleaned_data.get('nr_sde')

        if n_sde == None:
            self.flaga_s = 0
        else:
            self.flaga_s = 1

        return n_sde


    def clean_nr_mpk(self):
        n_mpk = self.cleaned_data.get('nr_mpk')

        if n_mpk == None:
            self.flaga_m = 0
        else:
            self.flaga_m = 1

        if self.rok_t > 2022:

            if self.flaga_s==0 and self.flaga_m==0:
                raise forms.ValidationError('Pola "Nr SDE" i/lub "Nr MPK" nie moga być puste!!! Wybierz coś!')
            elif self.flaga_s==1 and self.flaga_m==0:
                raise forms.ValidationError('Wybrałeś "Nr SDE" więc musisz do tego dobrać "Nr MPK" [402-11... lub 403-16...]!!!')

        return n_mpk


    def clean_data_fv(self):
        d_fv = self.cleaned_data.get('data_fv')
        rok = self.rok_t

        if isinstance(d_fv, date):
            d_rok = d_fv.year
        else:
            d_rok = 0

        if d_rok != 0:
            if d_rok != rok:
                raise forms.ValidationError('Błędna data FV. Zmień "Bieżacy Rok" aby ją wprowadzić...')

        return d_fv




class ZamowienieFormM(forms.ModelForm):
    flaga = 0
    flaga_s = 0
    flaga_m = 0
    rok_t = 0

    class Meta:
        model = Zamowienie
        fields = (
            'opis', 'kontrahent', 'wartosc_zam', 'sposob_plat', 'rodzaj_plat', 'nr_sde', 'nr_mpk',
            'nr_dok1', 'zal1', 'zal1_bi', 'nr_dok2', 'zal2', 'zal2_bi', 'nr_dok3', 'zal3', 'zal3_bi', 'kwota_brutto',
            'data_fv', 'nr_fv', 'roz', 'uwagi', 'flaga_sz', 'nip', 'nip_ind'
        )
        # 'nr_zam', 'data_zam', 'data_dost',


    def __init__(self, *args, **kwargs):
        rok = kwargs.pop('rok')
        super().__init__(*args, **kwargs)

        self.rok_t = rok

        try:
            self.fields['nr_sde'].queryset = NrSDE.objects.all().order_by('nazwa') # filter(rok=rok)
        except:
            self.fields['nr_sde'].queryset = NrSDE.objects.none()

        try:
            self.fields['nr_mpk'].queryset = NrMPK.objects.filter(rok=rok, lsde=True).order_by('nazwa') #rok__gte=2022
        except:
            self.fields['nr_pmk'].queryset = NrMPK.objects.none()


    def clean_nr_sde(self):
        n_sde = self.cleaned_data.get('nr_sde')

        if n_sde == None:
            self.flaga_s = 0
        else:
            self.flaga_s = 1

        return n_sde


    def clean_nr_mpk(self):
        n_mpk = self.cleaned_data.get('nr_mpk')

        if n_mpk == None:
            self.flaga_m = 0
        else:
            self.flaga_m = 1

        if self.rok_t > 2022:

            if self.flaga_s==0 and self.flaga_m==0:
                raise forms.ValidationError('Pola "Nr SDE" i/lub "Nr MPK" nie moga być puste!!! Wybierz coś!')
            elif self.flaga_s==1 and self.flaga_m==0:
                raise forms.ValidationError('Wybrałeś "Nr SDE" więc musisz do tego dobrać "Nr MPK" [402-11... lub 403-16...]!!!')


        return n_mpk





