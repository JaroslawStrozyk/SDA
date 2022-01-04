from django import forms
from .models import FirmaKasa, KwKp
from djmoney.models.fields import MoneyField
import datetime

class FirmaKasaForm(forms.ModelForm):

    class Meta:
        model = FirmaKasa
        fields = ('rodzaj','nazwa','adres','miasto','nip','kasa','konto','bo','stan','data_bo','uwagi')
    data_bo = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'}), initial=datetime.date.today)


class KwKpForm(forms.ModelForm):

    class Meta:
        model = KwKp
        fields = ('rodzaj','nazwa','adres','miasto','rozchod','przychod','data','opis','uwagi','switch')
    data = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'}), initial=datetime.date.today)