from django import forms
from .models import Ubezpieczenie
import datetime


class UbezpieczenieForm(forms.ModelForm):

    class Meta:
        model = Ubezpieczenie
        fields = ('nazwa','dotyczy', 'opiekun', 'skn1', 'skn2', 'daod', 'dado', 'uwagi',)

    daod = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'}), label="Data od", initial=datetime.date.today)
    dado = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'}), label="Data do", initial=datetime.date.today)

