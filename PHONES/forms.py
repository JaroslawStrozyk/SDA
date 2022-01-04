from django import forms
from .models import Telefon
import datetime

YEARS= [x for x in range(2009,2032)]
        

class TelefonForm(forms.ModelForm):

    class Meta:
        model = Telefon
        fields = ('usr', 'model', 'imei', 'sim', 'msisdn', 'kod', 'konto', 'haslo', 'data', 'uwagi','arch', 'pz','doc','docz','zam','pesel', 'mag')

    data = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'},years=YEARS), initial=datetime.date.today, label="Data przekazania")
    pz = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'},years=YEARS),   initial=datetime.date.today, label="Data zdania")