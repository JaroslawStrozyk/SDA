from django import forms

from ORDERS.models import NrSDE
from .models import Pracownik, Pensja, Premia_det, Stoisko


class PracownikForm(forms.ModelForm):
    class Meta:
        model = Pracownik
        fields = (
            'imie', 'nazwisko', 'grupa', 'dzial', 'zatrudnienie',
            'wymiar', 'data_zat', 'staz', 'pensja_ust', 'pensja_brutto', 'stawka_wyj_rob',
            'uwagi', 'pracuje', 'stawka_godz', 'lp_biuro'
        )


class Premia_detForm(forms.ModelForm):
    class Meta:
        model = Premia_det
        fields = (
            'projekt', 'pr_wielkosc', 'del_ilosc_st', 'del_ilosc_so', 'del_ilosc_we',
            'kw_sprzedazy', 'ind_pr_kwota', 'ind_pr_opis', 'akc'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['projekt'].queryset = NrSDE.objects.filter(rokk=2023).order_by('-nazwa_id') | NrSDE.objects.filter(rokk=2024).order_by('-nazwa_id') | NrSDE.objects.filter(rokk=2025).order_by('-nazwa_id')
        self.fields['pr_wielkosc'].queryset = Stoisko.objects.all().order_by('id')


class PensjaForm(forms.ModelForm):
    class Meta:
        model = Pensja
        fields = (
        'wynagrodzenie','przelew', 'ppk', 'obciazenie', 'obciazenie_opis', 'uwagi'
        )



class PensjaOForm(forms.ModelForm):
    class Meta:
        model = Pensja
        fields = (
            'osoba', 'obciazenie', 'obciazenie_opis'
        )

    def __init__(self, *args, **kwargs):
        super(PensjaOForm, self).__init__(*args, **kwargs)
        self.fields['osoba'].widget.attrs['readonly'] = True



class PensjaRForm(forms.ModelForm):
    class Meta:
        model = Pensja
        fields = (
        'del_ilosc_st', 'del_ilosc_we','del_ilosc_opis', 'premia', 'uwagi'
        )
