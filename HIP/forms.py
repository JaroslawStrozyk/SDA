from django import forms
from .models import Sprzet, Profil, Serwis
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

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = (
                  'sprzet', 'rodzaj_konta', 'kod', 'konto', 'haslo', 'adres', 'uwagi', 'fv', 'data_waznosci', 'auto_platnosc', 'karta'
        )

class SerwisForm(forms.ModelForm):
    class Meta:
        model = Serwis
        fields = (
                  'sprzet', 'data', 'problem', 'opis', 'uwagi'
        )