from django import forms
from decimal import Decimal, InvalidOperation
from moneyed import Money, PLN

class PDFForm(forms.Form):
    mid = forms.CharField(label='Miejscowość i data', max_length=100, required=False)
    iin = forms.CharField(label='Imie i Nazwisko', max_length=100, required=False)
    pesel = forms.CharField(label='PESEL', max_length=11, required=False)
    mc = forms.ChoiceField(label='Miesiąc', choices=[
        ('styczeń', 'Styczeń'), ('luty', 'Luty'), ('marzec', 'Marzec'),
        ('kwiecień', 'Kwiecień'), ('maj', 'Maj'), ('czerwiec', 'Czerwiec'),
        ('lipiec', 'Lipiec'), ('sierpień', 'Sierpień'), ('wrzesień', 'Wrzesień'),
        ('październik', 'Październik'), ('listopad', 'Listopad'), ('grudzień', 'Grudzień')
    ], required=False)
    kw = forms.CharField(label='Kwota (PLN)', required=False)

    def clean_pesel(self):
        pesel = self.cleaned_data.get('pesel')
        if pesel and len(pesel) == 11 and pesel.isdigit():
            return list(pesel)
        elif not pesel:
            return ['', '', '', '', '', '', '', '', '', '', '']
        else:
            raise forms.ValidationError("PESEL musi składać się z dokładnie 11 cyfr. Jest:" + str(len(pesel)))

    def clean_kw(self):
        kw = self.cleaned_data.get('kw')
        if kw:
            try:
                kw = Decimal(kw)
                if kw < 0:
                    raise forms.ValidationError("Kwota nie może być ujemna.")
                kw = Money(kw, PLN)
            except InvalidOperation:
                raise forms.ValidationError("Podaj poprawną wartość liczbową.")
        return kw
