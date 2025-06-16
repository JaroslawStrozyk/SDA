from django.forms import ModelForm, HiddenInput
from django import forms
from .models import Faktura, Osoba
from django.core.validators import ValidationError

import datetime

class FakturaForm(ModelForm):

    class Meta:
        model = Faktura
        fields =('osoba', 'dla_kogo', 'rfaktura','termin','targi','stoisko','kwota','zaco','spec','uwagi','confirm')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['osoba'].queryset = Osoba.objects.filter(invoice=True).order_by('naz_imie')

    def clean_osoba(self):
        osoba = self.cleaned_data.get('osoba')
        if osoba == None:
            raise forms.ValidationError('Pole nie może być puste !!!')
        return osoba



class EFakturaForm(ModelForm):

    class Meta:
        model = Faktura
        fields =('data','osoba','dla_kogo', 'rfaktura','termin','targi','stoisko','kwota','zaco','spec','uwagi','zrobione')


