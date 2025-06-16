from django import forms
from .models import Plyta, Rozchod, Przychod, Zwrot
from ORDERS.models import NrSDE
from datetime import date


class PlytaForm(forms.ModelForm):

    class Meta:
        model = Plyta
        fields = ('magazyn','nazwa', 'opis', 'limit', 'inw_stan', 'inw_data') # 'stan', , 'cena'

    def __init__(self, *args, **kwargs):
        mag = kwargs.pop('mag')
        super().__init__(*args, **kwargs)

        if mag == 'mag1':
            self.initial['magazyn'] = "MAGAZYN1"

        if mag == 'mag2':
            self.initial['magazyn'] = "MAGAZYN2"

        if mag == 'mag3':
            self.initial['magazyn'] = "MAGAZYN3"

        if mag == 'mag4':
            self.initial['magazyn'] = "MAGAZYN4"

        if mag == 'mag5':
            self.initial['magazyn'] = "MAGAZYN5"


class PrzychodForm(forms.ModelForm):

    class Meta:
        model = Przychod
        fields = ('zrodlo', 'data', 'ilosc', 'jm', 'cena_j', 'inwentura', 'bo')


class PrzychodPzForm(forms.ModelForm):

    class Meta:
        model = Przychod
        fields = ('plyta', 'zrodlo', 'data', 'ilosc', 'jm', 'cena_j', 'inwentura', 'bo')

        def __init__(self, *args, **kwargs):
            MAG = kwargs.pop('mag')
            ROD = kwargs.pop('rod')
            super().__init__(*args, **kwargs)

            print(">>>", MAG, ROD)

            try:
                self.fields['plyta'].queryset = Plyta.objects.filter(magazyn=MAG, rodzaj=ROD).order_by('nazwa')
            except:
                self.fields['plyta'].queryset = Plyta.objects.none()


class RozchodForm(forms.ModelForm):
    stan = '0.0'

    class Meta:
        model = Rozchod
        fields = ('cel', 'data', 'nr_sde', 'ilosc', 'jm')

    def __init__(self, *args, **kwargs):
        rok = kwargs.pop('rok')
        self.stan = kwargs.pop('stan')
        super().__init__(*args, **kwargs)

        try:
            self.fields['nr_sde'].queryset = NrSDE.objects.filter(rokk__gte=2022).order_by('nazwa') #rok__gte=2022   filter(rokk=rok)
        except:
            self.fields['nr_sde'].queryset = NrSDE.objects.none()


    def clean_ilosc(self):
        ilosc = float(self.cleaned_data.get('ilosc'))
        stan  = float(self.stan)

        if self.instance and self.instance.pk:
            initial_ilosc = float(self.instance.ilosc)
            if ilosc <= initial_ilosc:
                return ilosc

        if ilosc > stan:
            raise forms.ValidationError("Ilość jest większa niż aktualny stan !!!")

        return ilosc


#    def clean_data(self):
#        data = self.cleaned_data.get('data')
#        kdata = date(2023, 7, 1)
#
#        if kdata > data:
#            raise forms.ValidationError("Data musi być większa od 30.06.2023!!!")
#
#        return data




class ZwrotForm(forms.ModelForm):

    class Meta:
        model = Zwrot
        fields = ('cel', 'data', 'nr_sde', 'ilosc', 'jm')

    def __init__(self, *args, **kwargs):
        rok = kwargs.pop('rok')
        super().__init__(*args, **kwargs)

        try:
            self.fields['nr_sde'].queryset = NrSDE.objects.filter(rokk__gte=2022).order_by('nazwa') #rok__gte=2022 filter(rokk=rok) all()
        except:
            self.fields['nr_sde'].queryset = NrSDE.objects.none()
