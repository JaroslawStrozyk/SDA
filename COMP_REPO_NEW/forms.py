from django import forms
from .models import Sklad, Firma, ElementKatalogowy, OkresPrzechowywania
from ORDERS.models import NrSDE
from django.db.models import Case, When, Value, IntegerField

class SkladFormD(forms.ModelForm):
    class Meta:
        model = Sklad
        fields = (
            'dok_pdf1', 'dok_pdf2', 'dok_pdf3', 'dok_pdf4', 'fv_pdf1', 'uwagi'
          )


class SkladForm(forms.ModelForm):
    class Meta:
        model = Sklad
        fields = (
            'firma', 'nr_sde', 'okres', 'element_katalogowy', 'magazyn', 'magazyn_opis', 'przech_nazwa',
            'przech_nrpalet', 'wydano_ilosc', 'wydano_data', 'zwroco_ilosc', 'zwroco_data', 'zwroco_uwagi',
            'przech_sze', 'przech_gl'
        )

    def __init__(self, *args, **kwargs):
        stawka = kwargs.pop('stawka', None)
        firma_id = kwargs.pop('firma_id', None)
        super().__init__(*args, **kwargs)

        try:
            self.fields['nr_sde'].queryset = NrSDE.objects.filter(rokk__gte=2022).order_by('nazwa')
        except:
            self.fields['nr_sde'].queryset = NrSDE.objects.none()

        # Modyfikacja etykiet dla okresów
        okres_queryset = OkresPrzechowywania.objects.all()
        for okres in okres_queryset:
            okres.__str__ = lambda \
                self=okres: f"{self.nazwa} ({self.data_od.strftime('%d.%m.%Y')} - {self.data_do.strftime('%d.%m.%Y')})"
        self.fields['okres'].queryset = okres_queryset

        # Modyfikacja etykiet dla elementów katalogowych
        element_queryset = ElementKatalogowy.objects.all()
        for element in element_queryset:
            element.__str__ = lambda self=element: f"{self.nazwa} - {self.opis}"
        self.fields['element_katalogowy'].queryset = element_queryset

        # Jeśli przekazano ID firmy i jest większe niż 1, filtrujemy elementy
        if firma_id and int(firma_id) > 1:
            try:
                # Filtruj okresy
                okres_queryset = OkresPrzechowywania.objects.filter(firma_id=firma_id)
                for okres in okres_queryset:
                    okres.__str__ = lambda \
                        self=okres: f"{self.nazwa} ({self.data_od.strftime('%d.%m.%Y')} - {self.data_do.strftime('%d.%m.%Y')})"
                self.fields['okres'].queryset = okres_queryset

                # Filtruj elementy katalogowe
                element_queryset = ElementKatalogowy.objects.filter(firma_id=firma_id)
                for element in element_queryset:
                    element.__str__ = lambda self=element: f"{self.nazwa} - {self.opis}"
                self.fields['element_katalogowy'].queryset = element_queryset
            except:
                pass


# Zmodyfikowany fragment w forms.py
class SkladFormDet(forms.ModelForm):
    class Meta:
        model = Sklad
        fields = (
            'firma', 'nr_sde', 'okres', 'element_katalogowy', 'magazyn', 'magazyn_opis', 'przech_nazwa',
            'przech_nrpalet', 'wydano_ilosc', 'wydano_data', 'zwroco_ilosc', 'zwroco_data', 'zwroco_uwagi',
            'przech_sze', 'przech_gl'
        )

    def __init__(self, *args, **kwargs):
        firma_pk = kwargs.pop('firma_pk', None)
        sde_pk = kwargs.pop('sde_pk', None)
        firma_id = kwargs.pop('firma_id', None)

        super().__init__(*args, **kwargs)

        try:
            self.fields['nr_sde'].queryset = NrSDE.objects.filter(rokk__gte=2022).order_by('nazwa')
        except:
            self.fields['nr_sde'].queryset = NrSDE.objects.none()

        # Modyfikacja etykiet dla okresów
        okres_queryset = OkresPrzechowywania.objects.all()
        for okres in okres_queryset:
            okres.__str__ = lambda \
                    self=okres: f"{self.nazwa} ({self.data_od.strftime('%d.%m.%Y')} - {self.data_do.strftime('%d.%m.%Y')})"
        self.fields['okres'].queryset = okres_queryset

        # Modyfikacja etykiet dla elementów katalogowych
        element_queryset = ElementKatalogowy.objects.all()
        for element in element_queryset:
            element.__str__ = lambda self=element: f"{self.nazwa} - {self.opis}"
        self.fields['element_katalogowy'].queryset = element_queryset

        # Określamy firmę jako domyślną, jeśli firma_pk jest podane
        if firma_pk and int(firma_pk) > 0:
            try:
                firma = Firma.objects.get(pk=firma_pk)
                self.fields['firma'].initial = firma

                # Filtruj okresy dla wybranej firmy
                okres_queryset = OkresPrzechowywania.objects.filter(firma_id=firma_pk)
                for okres in okres_queryset:
                    okres.__str__ = lambda \
                            self=okres: f"{self.nazwa} ({self.data_od.strftime('%d.%m.%Y')} - {self.data_do.strftime('%d.%m.%Y')})"
                self.fields['okres'].queryset = okres_queryset

                # Filtruj elementy katalogowe dla wybranej firmy
                element_queryset = ElementKatalogowy.objects.filter(firma_id=firma_pk)
                for element in element_queryset:
                    element.__str__ = lambda self=element: f"{self.nazwa} - {self.opis}"
                self.fields['element_katalogowy'].queryset = element_queryset
            except:
                pass

        # Jeśli przekazano sde_pk, ustawiamy domyślną wartość dla nr_sde
        if sde_pk and int(sde_pk) > 0:
            try:
                nr_sde = NrSDE.objects.get(pk=sde_pk)
                self.fields['nr_sde'].initial = nr_sde
            except:
                pass

        # Jeśli przekazano ID firmy i jest większe niż 1, filtrujemy elementy
        # (zachowujemy poprzednią funkcjonalność)
        if firma_id and int(firma_id) > 1:
            try:
                # Filtruj okresy
                okres_queryset = OkresPrzechowywania.objects.filter(firma_id=firma_id)
                for okres in okres_queryset:
                    okres.__str__ = lambda \
                            self=okres: f"{self.nazwa} ({self.data_od.strftime('%d.%m.%Y')} - {self.data_do.strftime('%d.%m.%Y')})"
                self.fields['okres'].queryset = okres_queryset

                # Filtruj elementy katalogowe
                element_queryset = ElementKatalogowy.objects.filter(firma_id=firma_id)
                for element in element_queryset:
                    element.__str__ = lambda self=element: f"{self.nazwa} - {self.opis}"
                self.fields['element_katalogowy'].queryset = element_queryset
            except:
                pass


class EKForm(forms.ModelForm):
    class Meta:
        model = ElementKatalogowy
        fields = (
            'firma', 'nazwa', 'opis', 'szerokosc', 'glebokosc', 'przech_zdjecie',
            'przech_zdjecie2', 'przech_zdjecie3', 'przech_zdjecie4', 'uszkodz_zdjecie1',
            'uszkodz_zdjecie2', 'uszkodz_zdjecie3', 'uszkodz_zdjecie4', 'aktywny', 'zwolnione'
        )

    def __init__(self, *args, **kwargs):
        # Pobierz zmienną st z kwargs
        st = kwargs.pop('st', None)

        # Wywołaj inicjalizator klasy bazowej
        super(EKForm, self).__init__(*args, **kwargs)

        # Sortowanie z explicit priority - firma o id=1 zawsze pierwsza
        self.fields['firma'].queryset = Firma.objects.annotate(
            custom_order=Case(
                When(pk=1, then=Value(0)),  # Firma z pk=1 ma najwyższy priorytet (0)
                default=Value(1),  # Wszystkie inne firmy mają niższy priorytet (1)
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'nazwa')  # Najpierw wg priorytetu, potem wg nazwy

        # Sprawdź, czy to jest dodawanie nowego rekordu czy edycja istniejącego
        is_new_record = self.instance.pk is None

        # Jeśli to nowy rekord i st > 1 (oznacza wybraną firmę)
        if is_new_record and st and int(st) > 1:
            try:
                firma_id = int(st)
                firma = Firma.objects.get(pk=firma_id)
                self.initial['firma'] = firma.pk
            except Firma.DoesNotExist:
                pass


class OKForm(forms.ModelForm):
    class Meta:
        model = OkresPrzechowywania
        fields = (
            'firma', 'nazwa', 'data_od', 'data_do', 'stawka', 'faktura', 'fv_pdf', 'zwolnione', 'zamkniety'
        )
    def __init__(self, *args, **kwargs):
        # Pobierz zmienną st z kwargs
        st = kwargs.pop('st', None)

        # Wywołaj inicjalizator klasy bazowej
        super(OKForm, self).__init__(*args, **kwargs)

        # Sortowanie z explicit priority - firma o id=1 zawsze pierwsza
        self.fields['firma'].queryset = Firma.objects.annotate(
            custom_order=Case(
                When(pk=1, then=Value(0)),  # Firma z pk=1 ma najwyższy priorytet (0)
                default=Value(1),  # Wszystkie inne firmy mają niższy priorytet (1)
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'nazwa')  # Najpierw wg priorytetu, potem wg nazwy

        # Sprawdź, czy to jest dodawanie nowego rekordu czy edycja istniejącego
        is_new_record = self.instance.pk is None

        # Jeśli to nowy rekord i st > 1 (oznacza wybraną firmę)
        if is_new_record and st and int(st) > 1:
            try:
                firma_id = int(st)
                firma = Firma.objects.get(pk=firma_id)
                self.initial['firma'] = firma.pk
            except Firma.DoesNotExist:
                pass