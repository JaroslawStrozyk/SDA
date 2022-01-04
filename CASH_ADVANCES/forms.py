from django import forms


from TaskAPI.models import Rok
from .models import Pozycja, Rozliczenie
from ORDERS.models import NrSDE, NrMPK
import datetime


YEARS= [x for x in range(2009,2032)]

def test_rok():
    tst  = Rok.objects.all().order_by('rok')
    rok  = 0
    for t in tst:
        if t.flg == 1:
            rok = t.rok
    return rok


def test_osoba(request):
    name_log = request.user.first_name + " " + request.user.last_name
    inicjaly = '.'.join([x[0] for x in name_log.split()])+'.'

    if inicjaly=='P.Z.' or inicjaly=='J.S.':
        rozliczenie = 1
    else:
        rozliczenie = 0
    return name_log, inicjaly, rozliczenie


class RozliczenieForm(forms.ModelForm):
    class Meta:
        model = Rozliczenie
        fields = (
            'data_zal',  'data_roz', 'kw', 'nazwisko',  'zal_kwota', 'zal_suma', 'saldo',
            'uwagi', 'roz','przek', 'uwagi'
        )




class PozycjaForm(forms.ModelForm):
    class Meta:
        model = Pozycja
        fields = (
            'nr_roz', 'kontrahent', 'nr_fv', 'kwota_netto', 'kwota_brutto', 'data_zam', 'data_zak', 'opis',
            'nr_sde', 'nr_mpk', 'uwagi'
        )

    # data_zak = forms.DateField(widget=forms.SelectDateWidget(
    #                            attrs={'style': 'display: inline-block;'},
    #                            years=YEARS
    #                      ),
    #                            label="Data zakupu",
    #                            initial=datetime.date.today
    #                      )


    def __init__(self, *args, **kwargs):
        self.per = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        rok = test_rok()

        try:
            self.fields['nr_sde'].queryset = NrSDE.objects.all().order_by('nazwa')
        except:
            self.fields['nr_sde'].queryset = NrSDE.objects.none()

        try:
            self.fields['nr_mpk'].queryset = NrMPK.objects.filter(rok=rok).order_by('nazwa')
        except:
            self.fields['nr_pmk'].queryset = NrMPK.objects.none()

        try:
            if self.per == None:
                self.fields['nr_roz'].queryset = Rozliczenie.objects.filter(rok=rok, roz=False, przek=False).order_by('-id')
            else:
                self.fields['nr_roz'].queryset = Rozliczenie.objects.filter(rok=rok, inicjaly=self.per, roz=False, przek=False).order_by('-id')
        except:
            self.fields['nr_roz'].queryset = Rozliczenie.objects.none()

