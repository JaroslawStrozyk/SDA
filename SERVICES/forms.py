from django import forms
from .models import Usluga, Profil


class UslugaForm(forms.ModelForm):
    class Meta:
        model = Usluga
        fields = (
                  'nazwa_siec', 'usr', 'dostawca', 'hosting', 'uwagi' ,'zdj', 'okres', 'data_waznosci'
        )

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = (
                  'usluga', 'rodzaj_konta', 'konto', 'haslo', 'adres', 'uwagi'
        )