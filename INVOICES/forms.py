from django.forms import ModelForm, HiddenInput
from django import forms
from .models import Faktura

import datetime

class FakturaForm(ModelForm):

    class Meta:
        model = Faktura
        fields =('imie','nazwisko','rfaktura','termin','targi','stoisko','kwota','zaco','spec','uwagi')
    termin = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block;'}), label="Termin płatności", initial=datetime.date.today)


class EFakturaForm(ModelForm):

    class Meta:
        model = Faktura
        fields =('data','imie','nazwisko','rfaktura','termin','targi','stoisko','kwota','zaco','spec','uwagi','zrobione')
    termin = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block;'}), label="Termin płatności")

