from django import forms
from .models import Sprzet, Profil
import datetime

YEARS= [x for x in range(2009,2032)]

class SprzetForm(forms.ModelForm):
    class Meta:
        model = Sprzet
        fields = (
                  'system', 'nazwa_siec', 'kik', 'usr', 'host', 'typ', 'adres_ip',
                  'domena', 'sw_gn', 'snk', 'uwagi', 'zdj', 'arch',
                  'gw', 'doc', 'docz', 'zam', 'pesel', 'pr', 'pz', 'mag', 'stan', 'opis', 'historia', 'wartosc', 'sprzedany'
        )



    gw = forms.DateField(widget=forms.SelectDateWidget(
                               attrs={'style': 'display: inline-block; width: 33%;'},
                               years=YEARS
                         ),
                               label="Termin Gwaracji",
                               initial=datetime.date.today
                         )

    pr = forms.DateField(widget=forms.SelectDateWidget(
                               attrs={'style': 'display: inline-block; width: 33%;'},
                               years=YEARS
                         ),
                               label="Data przyjęcia do użytku",
                               initial=datetime.date.today
                         )

    pz = forms.DateField(widget=forms.SelectDateWidget(
                               attrs={'style': 'display: inline-block; width: 33%;'},
                               years=YEARS
                         ),
                               label="Data zdania",
                               initial=datetime.date.today
                         )

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = (
                  'sprzet', 'rodzaj_konta', 'kod', 'konto', 'haslo', 'adres', 'uwagi', 'fv', 'data_waznosci', 'auto_platnosc', 'karta'
        )