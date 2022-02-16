from django import forms
from .models import Pracownik, Pensja


class PracownikForm(forms.ModelForm):
    class Meta:
        model = Pracownik
        fields = (
            'imie', 'nazwisko', 'grupa', 'dzial', 'zatrudnienie',
            'wymiar', 'data_zat', 'staz', 'pensja_ust', 'stawka_nadgodz',
            'stawka_wyj', 'ppk', 'dystans', 'uwagi', 'pracuje'
        )


class PensjaForm(forms.ModelForm):
    class Meta:
        model = Pensja
        fields = (
        'przelew', 'ppk', 'dodatek', 'dodatek_opis', 'obciazenie', 'obciazenie_opis',
        'km_ilosc', 'nadgodz_ilosc', 'nadgodz_opis', 'del_ilosc_100', 'del_ilosc_50', 'premia',
        'zaliczka', 'komornik', 'uwagi'
        )

        # 'rok', 'miesiac','pracownik','wynagrodzenie', 'ppk', 'przelew', 'gotowka',
        # 'dodatek', 'dodatek_opis', 'obciazenie', 'obciazenie_opis', 'km_ilosc', 'km_wartosc',
        # 'nadgodz_ilosc', 'nadgodz', 'nadgodz_opis', 'del_ilosc_100', 'del_ilosc_50', 'del_ilosc_razem',
        # 'premia', 'razem', 'zaliczka', 'komornik', 'brutto_brutto', 'wyplata', 'sum_kosztow',
        # 'rozliczono', 'l4', 'uwagi'


# class PensjaRLForm(forms.ModelForm):
#     class Meta:
#         model = Pensja
#         fields = (
#             'pracownik', 'wyplata', 'rozliczono', 'l4'
#         )
#
#     def __init__(self, *args, **kwargs):
#         super(PensjaRLForm, self).__init__(*args, **kwargs)
#         if self.instance.id:
#             self.fields['pracownik'].widget.attrs['disabled'] = True
#             self.fields['wyplata'].widget.attrs['disabled'] = True