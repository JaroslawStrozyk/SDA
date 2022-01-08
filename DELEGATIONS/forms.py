from django import forms
from .models import Delegacja
import datetime

class DelegacjaForm(forms.ModelForm):

    class Meta:
        model = Delegacja
        fields = ('naz_imie', 'targi', 'data_od', 'data_do', 'kasa_pln', 'kasa_euro', 'kasa_funt', 'kasa_inna', 'kasa_karta', 'confirm')

    #data_od = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block;'}), initial=datetime.date.today)
    #data_do = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block;'}), initial=datetime.date.today)


class EDelegacjaForm(forms.ModelForm):

    class Meta:
        model = Delegacja
        fields = ('imie', 'nazwisko', 'targi', 'data_od', 'data_do', 'kasa_pln', 'kasa_euro', 'kasa_funt', 'kasa_inna', 'kasa_karta','zrobione')