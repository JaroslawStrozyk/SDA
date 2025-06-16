from django import forms

from INVOICES.models import Osoba
from ORDERS.models import NrSDE
from .models import Delegacja, Pozycja, Dieta
from djmoney.models.fields import MoneyField
from CARS.models import Auto


class DelegacjaForm(forms.ModelForm):

    class Meta:
        model = Delegacja
        fields = (
            'osoba', 'targi', 'lok_targi', 'data_od', 'data_do', 'cel_wyj', 'transport', 'kasa_pln', 'kasa_euro',
            'kasa_funt', 'kasa_dolar', 'kasa_inna', 'kasa_karta', 'confirm', 'dane_auta'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dane_auta'].queryset = Auto.objects.filter(deleg_auto=True).order_by('rej')
        self.fields['osoba'].queryset = Osoba.objects.filter(delega=True).order_by('naz_imie')

    def clean_osoba(self):
        osoba = self.cleaned_data.get('osoba')
        if osoba == None:
            raise forms.ValidationError('Pole nie może być puste !!!')
        return osoba



class EDelegacjaForm(forms.ModelForm):

    class Meta:
        model = Delegacja
        fields = ('osoba', 'targi', 'data_od', 'data_do', 'kasa_pln', 'kasa_euro', 'kasa_funt', 'kasa_dolar',
                  'kasa_inna', 'kasa_karta','zrobione', 'lok_targi','cel_wyj', 'transport', 'dataz', 'numer', 'pobrane_pw'
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['osoba'].queryset = Osoba.objects.filter(delega=True).order_by('naz_imie')


class RDelegacjaForm(forms.ModelForm):

    class Meta:
        model = Delegacja
        fields = (
            'dc_rozpo', 'dc_zakon', 'przekr_gran', 'powrot_kraj', 'transport', 'sniadanie',
            'obiad', 'kolacja', 'silnik_poj','data_rozl', 'nocleg_ilosc_kr', 'nocleg_ilosc_za', 'dane_auta',
            'data_pobr_zal', 'kod_sde_targi1', 'kod_sde_targi2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dane_auta'].queryset = Auto.objects.filter(deleg_auto=True).order_by('rej')
        self.fields['kod_sde_targi1'].queryset = NrSDE.objects.filter(rokk__gte=2022).order_by('nazwa')
        self.fields['kod_sde_targi2'].queryset = NrSDE.objects.filter(rokk__gte=2022).order_by('nazwa')



class PozycjaForm(forms.ModelForm):

    class Meta:
        model = Pozycja
        fields = (
            'delegacja', 'pozycja', 'kwota_waluta', 'waluta'
        )


class DietaForm(forms.ModelForm):

    class Meta:
        model = Dieta
        fields = (
            'panstwo', 'dieta', 'nocleg'
        )
