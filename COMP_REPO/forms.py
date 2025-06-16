from django import forms
from .models import Sklad, Firma
from ORDERS.models import NrSDE
from moneyed import Money, EUR
from django.core.exceptions import ValidationError


class SkladForm(forms.ModelForm):
    class Meta:
        model = Sklad
        fields = (
            'magazyn', 'nr_sde','przech_nazwa','przech_nrpalet', 'przech_zdjecie', 'przech_zdjecie2', 'przech_zdjecie3',
            'przech_zdjecie4', 'przech_sze', 'przech_gl', 'wydano_ilosc', 'wydano_data', 'zwroco_ilosc', 'zwroco_data',
            'zwroco_uwagi', 'czas_od', 'czas_do', 'uszkodz_zdjecie1', 'uszkodz_zdjecie2', 'uszkodz_zdjecie3',
            'uszkodz_zdjecie4', 'faktura', 'zwolnione', 'stawka', 'blokada', 'multi_uzycie', 'multi_uzycie_id',
            'multi_uzycie_st', 'firma', 'dok_pdf1', 'dok_pdf2', 'dok_pdf3', 'dok_pdf4', 'fv_pdf1', 'uwagi', 'do_skasowania'
        )

    def __init__(self, *args, **kwargs):
        d_e = kwargs.pop('d_e', False)
        stawka = kwargs.pop('stawka', None)
        mag = kwargs.pop('mag', None)
        bz = kwargs.pop('bz', False)
        super().__init__(*args, **kwargs)

        if self.instance and bz: # (self.instance.blokada and self.blokada_zapisu):
            self.fields['czas_od'].disabled = True
            self.fields['czas_do'].disabled = True
        else:
            self.fields['czas_od'].disabled = False
            self.fields['czas_do'].disabled = False

        # Ustaw domyślną wartość dla pola 'magazyn', jeśli 'mag' jest podane
        if mag:
            self.fields['magazyn'].initial = mag
        else:
            self.fields['magazyn'].initial = Sklad.CHOISES_PLACE[0][0]


        if Money('00.00', EUR) == self.instance.stawka:
            self.instance.stawka = stawka
            self.fields['stawka'].initial = stawka

        try:
            self.fields['nr_sde'].queryset = NrSDE.objects.filter(rokk__gte=2021).order_by('nazwa') #rok__gte=2022   filter(rokk=rok)
        except:
            self.fields['nr_sde'].queryset = NrSDE.objects.none()

        self.fields['multi_uzycie_id'].widget.attrs['readonly'] = True

        if d_e:
            #self.fields['firma'].queryset = Firma.objects.none()
            self.fields['firma'].queryset = Firma.objects.all()  # Wczytaj wszystkie firmy
            #self.fields['firma'].empty_label = "----"  # Wyświetl pustą wartość jako opcję domyślną
            self.fields['firma'].initial = None

        ########################################################################################

    def clean_firma(self):
        firma = self.cleaned_data.get('firma')
        multi_uzycie = self.cleaned_data.get('multi_uzycie')
        if not firma and multi_uzycie:
            raise ValidationError("To pole jest wymagane.")
        return firma
    def clean_nr_sde(self):
        nr_sde = self.cleaned_data.get('nr_sde')
        if not nr_sde:
            raise ValidationError("To pole jest wymagane.")
        return nr_sde

    def clean_przech_gl(self):
        przech_gl = self.cleaned_data.get('przech_gl')
        if przech_gl <= 0:
            raise ValidationError("Wartość musi być większa od zera.")
        return przech_gl

    def clean_przech_sze(self):
        przech_sze = self.cleaned_data.get('przech_sze')
        if przech_sze <= 0:
            raise ValidationError("Wartość musi być większa od zera.")
        return przech_sze

#    def clean_czas_do(self):
#        czas_do = self.cleaned_data.get('czas_do')
#        czas_od = self.cleaned_data.get('czas_od')
#        if czas_od > czas_do:
#            raise ValidationError("Końcowy czas nie może być mniejszy od początkowego!")
#        return czas_do

    def clean_czas_do(self):
        czas_do = self.cleaned_data.get('czas_do')
        czas_od = self.cleaned_data.get('czas_od')

        # Jeśli oba są None, nie podnosimy błędu
        if czas_od is None and czas_do is None:
            return czas_do

        # Jeśli czas_od jest None, ale czas_do ma wartość, dodajemy błąd do pola 'czas_od'
        if czas_od is None and czas_do is not None:
            self.add_error('czas_od', "Pole 'Od daty' nie może być puste, gdy 'Do daty' ma wartość.")
            return czas_do

        # Jeśli czas_do jest None, ale czas_od ma wartość, wszystko jest w porządku
        if czas_do is None:
            return czas_do

        # Sprawdzamy, czy czas_od > czas_do
        if czas_od > czas_do:
            raise ValidationError("Końcowy czas nie może być mniejszy od początkowego!")

        return czas_do
