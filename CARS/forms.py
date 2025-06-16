from django import forms
from .models import Auto
import datetime


YEARS =[x for x in range(2009,2032)]

class AutoForm(forms.ModelForm):

    class Meta:
        model = Auto
        fields = (
                  'rodzaj','typ', 'rej', 'imie_n', 'opis', 'img1', 'img2', 'sprzedany', 'pt',
                  'us', 'ps', 'uwagi', 'nul', 'drl', 'dzl', 'rul', 'arch', 'koniecl', 'deleg_auto'
        )
        #pt = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'My placeholder'}))



