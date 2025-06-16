from django import forms
from .models import Ubezpieczenie, Termin
import datetime


class UbezpieczenieForm(forms.ModelForm):

    class Meta:
        model = Ubezpieczenie
        fields = (
            'firma', 'nazwa', 'dotyczy', 'suma', 'skladka', 'doc1', 'doc2',
            'data_od', 'data_do', 'raty', 'data_raty', 'uwagi'
        )


class TerminForm(forms.ModelForm):

    class Meta:
        model = Termin
        fields = (
            'firma', 'dotyczy', 'suma', 'skladka', 'doc1', 'doc2',
            'data_od', 'data_do',  'uwagi'
        )
