from django.db import models
from djmoney.models.fields import MoneyField
from ORDERS.models import NrSDE
from django.utils import timezone
from moneyed import Money, PLN, EUR, CURRENCIES
from django.db.models.signals import post_save
from django.dispatch import receiver


class Firma(models.Model):
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa firmy", blank=True, default='')
    aktywna = models.BooleanField(default=True, verbose_name="Firma aktywna")
    data_utworzenia = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmy"


def get_default_firma():
    firma = Firma.objects.filter(aktywna=True).first()
    if firma:
        return firma.id
    return None


class OkresPrzechowywania(models.Model):
    """
    Model reprezentujący okres przechowywania elementów dla danej firmy.
    Pozwala na grupowanie elementów w różnych okresach rozliczeniowych.
    """
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE, verbose_name="Firma")
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa okresu", blank=True)
    data_od = models.DateField(verbose_name="Od daty")
    data_do = models.DateField(verbose_name="Do daty")
    stawka = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Stawka")
    zwolnione = models.BooleanField(default=False, verbose_name="Zwolnione")
    zamkniety = models.BooleanField(default=False, verbose_name="Okres zamknięty")
    faktura = models.CharField(max_length=100, verbose_name="Numer faktury", blank=True, default='')
    fv_pdf  = models.FileField(upload_to='magazyn_fv', verbose_name="Faktura", blank=True)
    suma_kosztow = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Suma kosztów w okresie")
    suma_powierzchni = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Suma powierzchni [m²]")
    data_utworzenia = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    data_modyfikacji = models.DateTimeField(auto_now=True, verbose_name="Data modyfikacji")
    stan = models.IntegerField(default=0, verbose_name="Stan okresu")

    def __str__(self):
        return f"{self.firma.nazwa} - {self.nazwa} ({self.data_od} do {self.data_do})"

    def save(self, *args, **kwargs):
        # Sprawdzamy, czy to nowy obiekt czy edycja istniejącego
        is_new = self.pk is None

        # Jeśli to edycja, pobieramy poprzedni stan obiektu
        old_instance = None
        if not is_new:
            try:
                old_instance = OkresPrzechowywania.objects.get(pk=self.pk)
            except OkresPrzechowywania.DoesNotExist:
                pass

        # Automatyczne tworzenie nazwy okresu, jeśli nie została podana
        if not self.nazwa:
            self.nazwa = f"Okres {self.data_od.strftime('%d.%m.%Y')} - {self.data_do.strftime('%d.%m.%Y')}"

        # Zapisujemy obiekt
        super().save(*args, **kwargs)

        # Sprawdzamy, czy nastąpiła zmiana wartości pola zwolnione
        if old_instance and old_instance.zwolnione != self.zwolnione:
            # Pobieramy wszystkie powiązane wpisy z tabeli Sklad
            powiazane_sklady = Sklad.objects.filter(okres=self)

            # Zmiana z False na True (zwolnienie)
            if self.zwolnione:
                from django.db import connection
                with connection.cursor() as cursor:
                    for sklad in powiazane_sklady:
                        # Pobierz obecną wartość suma i walutę
                        cursor.execute(
                            'SELECT suma, suma_currency FROM public."COMP_REPO_NEW_sklad" WHERE id = %s',
                            [sklad.pk]
                        )
                        result = cursor.fetchone()
                        if result and result[0] is not None:
                            suma_value, currency = result

                            # Aktualizuj suma_zw i wyzeruj suma
                            cursor.execute(
                                'UPDATE public."COMP_REPO_NEW_sklad" SET suma_zw = %s, suma_zw_currency = %s, suma = 0, zwolnione = TRUE WHERE id = %s',
                                [suma_value, currency, sklad.pk]
                            )
                        else:
                            # Jeśli suma jest NULL, po prostu ustaw zwolnione na TRUE
                            cursor.execute(
                                'UPDATE public."COMP_REPO_NEW_sklad" SET zwolnione = TRUE WHERE id = %s',
                                [sklad.pk]
                            )

            # Zmiana z True na False (cofnięcie zwolnienia)
            else:
                from django.db import connection
                with connection.cursor() as cursor:
                    for sklad in powiazane_sklady:
                        # Pobierz obecną wartość suma_zw i walutę
                        cursor.execute(
                            'SELECT suma_zw, suma_zw_currency FROM public."COMP_REPO_NEW_sklad" WHERE id = %s',
                            [sklad.pk]
                        )
                        result = cursor.fetchone()
                        if result and result[0] is not None:
                            suma_zw_value, currency = result

                            # Aktualizuj suma i wyzeruj suma_zw
                            cursor.execute(
                                'UPDATE public."COMP_REPO_NEW_sklad" SET suma = %s, suma_currency = %s, suma_zw = 0, zwolnione = FALSE WHERE id = %s',
                                [suma_zw_value, currency, sklad.pk]
                            )
                        else:
                            # Jeśli suma_zw jest NULL, po prostu ustaw zwolnione na FALSE
                            cursor.execute(
                                'UPDATE public."COMP_REPO_NEW_sklad" SET zwolnione = FALSE WHERE id = %s',
                                [sklad.pk]
                            )

        # Jeśli okres jest zapisywany po raz pierwszy, skopiuj elementy z poprzedniego okresu
        if is_new:
            # Znajdź poprzedni okres dla tej firmy
            poprzedni_okres = OkresPrzechowywania.objects.filter(
                firma=self.firma,
                data_do__lt=self.data_od
            ).order_by('-data_do').first()

            if poprzedni_okres:
                # Pobierz elementy z poprzedniego okresu
                elementy_do_skopiowania = Sklad.objects.filter(
                    okres=poprzedni_okres,
                    status_pracy=1   #status=1  # Tylko aktywne elementy
                )

                # Skopiuj elementy do nowego okresu
                for element in elementy_do_skopiowania:
                    # Tworzymy nowy element bez kopiowania ID
                    element.pk = None
                    element.okres = self
                    element.czas_od = self.data_od
                    element.czas_do = self.data_do
                    element.liczyc = True  # Pierwszy wpis do obliczeń
                    # Ustawiamy pole zwolnione zgodnie z wartością w OkresPrzechowywania
                    element.zwolnione = self.zwolnione
                    element.save()


    class Meta:
        verbose_name = "Okres przechowywania"
        verbose_name_plural = "Okresy przechowywania"
        ordering = ['-data_od']


class ElementKatalogowy(models.Model):
    """
    Model reprezentujący elementy katalogowe, które mogą być wielokrotnie używane.
    """
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE, verbose_name="Firma")
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa elementu")
    opis = models.TextField(blank=True, verbose_name="Opis elementu")
    szerokosc = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Szerokość [m]")
    glebokosc = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Głębokość [m]")
    wysokosc = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Wysokość [m]")
    powierzchnia = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Powierzchnia [m²]")
    # Zdjęcia
    przech_zdjecie = models.FileField(upload_to='magazyn', verbose_name="Zdjęcie 1", blank=True)
    przech_zdjecie2 = models.FileField(upload_to='magazyn', verbose_name="Zdjęcie 2", blank=True)
    przech_zdjecie3 = models.FileField(upload_to='magazyn', verbose_name="Zdjęcie 3", blank=True)
    przech_zdjecie4 = models.FileField(upload_to='magazyn', verbose_name="Zdjęcie 4", blank=True)
    uszkodz_zdjecie1 = models.FileField(upload_to='magazyn', verbose_name="Uszkodzenie 1", blank=True)
    uszkodz_zdjecie2 = models.FileField(upload_to='magazyn', verbose_name="Uszkodzenie 2", blank=True)
    uszkodz_zdjecie3 = models.FileField(upload_to='magazyn', verbose_name="Uszkodzenie 3", blank=True)
    uszkodz_zdjecie4 = models.FileField(upload_to='magazyn', verbose_name="Uszkodzenie 4", blank=True)

    data_utworzenia = models.DateTimeField(auto_now_add=True)
    aktywny = models.BooleanField(default=True, verbose_name="Element na liście")
    wydany = models.BooleanField(default=False, verbose_name="Element wydany")
    licznik = models.IntegerField(default=0, verbose_name="Licznik użyć")
    zwolnione = models.BooleanField(default=False, verbose_name="Zwolnione")

    def save(self, *args, **kwargs):
        # Automatyczne obliczanie powierzchni
        self.powierzchnia = self.szerokosc * self.glebokosc
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nazwa} ({self.firma.nazwa}) {self.opis}"

    class Meta:
        verbose_name = "Element katalogowy"
        verbose_name_plural = "Elementy katalogowe"
        ordering = ['firma', 'nazwa']


class HistoriaPalety(models.Model):
    """
    Model do śledzenia historii zmian numerów palet dla elementów składowania.
    """
    sklad = models.ForeignKey('Sklad', on_delete=models.CASCADE, related_name='historia_palet')
    numer_palety = models.CharField(max_length=100, verbose_name="Numer palety")
    data_zmiany = models.DateTimeField(auto_now_add=True, verbose_name="Data zmiany")
    zmieniajacy = models.CharField(max_length=100, verbose_name="Osoba zmieniająca", blank=True)

    def __str__(self):
        return f"Paleta {self.numer_palety} dla {self.sklad.przech_nazwa} ({self.data_zmiany})"

    class Meta:
        verbose_name = "Historia palety"
        verbose_name_plural = "Historie palet"
        ordering = ['-data_zmiany']


class Sklad(models.Model):
    """
    Główny model przechowywanych elementów z rozszerzoną funkcjonalnością.
    """

    CHOISES_PLACE = (
        ('Wysogotowo', 'Wysogotowo'),
        ('Podolany', 'Podolany'),
        ('Jarocin', 'Jarocin')
    )

    # Relacje
    firma = models.ForeignKey('Firma', verbose_name="Firma", on_delete=models.CASCADE, default=get_default_firma)
    nr_sde = models.ForeignKey(NrSDE, verbose_name="Stoisko", max_length=100, on_delete=models.SET_NULL, null=True, blank=True, related_name='skladowane_elementy')
    okres = models.ForeignKey('OkresPrzechowywania', on_delete=models.CASCADE, verbose_name="Okres przechowywania", null=True, blank=True)
    element_katalogowy = models.ForeignKey('ElementKatalogowy', on_delete=models.SET_NULL, verbose_name="Element z katalogu", null=True, blank=True)

    # Dane podstawowe
    magazyn = models.CharField(max_length=50, verbose_name="Miejsce składowania", choices=CHOISES_PLACE, default='Podolany')
    magazyn_opis = models.CharField(max_length=100, verbose_name="Opis miejsca składowania", blank=True, default='')
    przech_nazwa = models.CharField(max_length=100, verbose_name="Nazwa towaru", blank=True, default='')
    przech_nrpalet = models.CharField(max_length=100, verbose_name="Numer palety", blank=True, default='')

    # Wymiary i powierzchnia
    przech_sze = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Szerokość [m]")
    przech_gl = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Głębokość [m]")
    przech_wys = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Wysokość [m]")
    przech_pow = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Powierzchnia przechowywania [m²]")

    # Dane wydania/zwrotu
    wydano_ilosc = models.IntegerField(default=0, verbose_name="Ile wydano")
    wydano_data = models.DateField(verbose_name="Data wydania", null=True, blank=True)
    zwroco_ilosc = models.IntegerField(default=0, verbose_name="Ile zwrócono")
    zwroco_data = models.DateField(verbose_name="Data powrotu", null=True, blank=True)
    zwroco_uwagi = models.TextField(blank=True, verbose_name="Zwroty - Uwagi")

    # Okres przechowywania
    czas_od = models.DateField(verbose_name="Od daty", null=True, blank=True)
    czas_do = models.DateField(verbose_name="Do daty", null=True, blank=True)
    ilosc_dni = models.IntegerField(default=0, verbose_name="Liczba dni")

    # Koszty
    stawka = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Stawka")
    koszt_przech = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Koszty przechowywania")
    suma = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Suma Kosztów")
    suma_pow = models.DecimalField(max_digits=11, decimal_places=1, default=0.0, verbose_name="Całkowita powierzchnia [m²]")
    suma_zw = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Suma Zwolnień")
    suma_np = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Suma nie przypisanych")
    suma_1m = MoneyField(decimal_places=2, default=0, default_currency='EUR', max_digits=11, verbose_name="Suma za 1 m-c")


    # Flagi statusu
    zwolnione = models.BooleanField(default=False, verbose_name="Zwolnione")
    blokada_zapisu = models.BooleanField(default=False, verbose_name="Blokada zapisu")
    flaga_op = models.IntegerField(default=0, verbose_name="Flaga operacji")
    status_pracy = models.IntegerField(default=0, verbose_name="Status Pracy")

    # Dokumenty
    dok_pdf1 = models.FileField(upload_to='magazyn', verbose_name="Lista do przechowywania1", blank=True)
    dok_pdf2 = models.FileField(upload_to='magazyn', verbose_name="Lista do przechowywania2", blank=True)
    dok_pdf3 = models.FileField(upload_to='magazyn', verbose_name="Lista do przechowywania3", blank=True)
    dok_pdf4 = models.FileField(upload_to='magazyn', verbose_name="Lista do przechowywania4", blank=True)
    fv_pdf1 = models.FileField(upload_to='magazyn', verbose_name="Faktura", blank=True)

    # Dodatkowe informacje
    uwagi = models.TextField(blank=True, verbose_name="Adnotacje")
    liczyc = models.BooleanField(default=False, verbose_name="Pierwszy wpis do obliczeń")


    def __str__(self):
        return str(self.nr_sde)

    def save(self, *args, **kwargs):
        # Sprawdzenie czy to nowy obiekt
        is_new = self.pk is None

        # Pobierz stary obiekt do porównania
        old_instance = None
        if not is_new:
            try:
                old_instance = Sklad.objects.get(pk=self.pk)
            except Sklad.DoesNotExist:
                pass

        # Gdy wybrano okres przechowywania, przepisz daty z okresu, jeśli nie są ustawione
        if self.okres:
            if not self.czas_od or (is_new and self.okres.data_od != self.czas_od):
                self.czas_od = self.okres.data_od
            if not self.czas_do or (is_new and self.okres.data_do != self.czas_do):
                self.czas_do = self.okres.data_do

            # Sprawdź, czy stawka z okresu zmieniła się
            should_update_rate = False
            if old_instance and old_instance.okres and old_instance.okres.id == self.okres.id:
                # Sprawdź, czy stawka w okresie została zmieniona od ostatniego zapisu
                if old_instance.stawka.amount != self.okres.stawka.amount:
                    should_update_rate = True

            # Przepisz stawkę z okresu, jeśli nie jest ustawiona lub powinna być zaktualizowana
            if not self.stawka.amount or should_update_rate:
                self.stawka = self.okres.stawka

            # Synchronizuj pole zwolnione z okresem, jeśli jest nowy rekord lub zmieniono okres
            if is_new or (old_instance and old_instance.okres != self.okres):
                self.zwolnione = self.okres.zwolnione

        # Obliczanie powierzchni przechowywania
        if self.przech_sze and self.przech_gl:
            self.przech_pow = self.przech_sze * self.przech_gl

        # Obliczanie liczby dni przechowywania
        if self.czas_od and self.czas_do:
            delta = self.czas_do - self.czas_od
            self.ilosc_dni = delta.days + 1  # Włącznie z początkiem i końcem

        # Jeśli wybrano element katalogowy, wypełnij wymiary i dane
        if self.element_katalogowy:
            # Wypełnij dane tylko jeśli pola są puste lub to nowy wpis
            if not self.przech_nazwa or is_new:
                self.przech_nazwa = self.element_katalogowy.nazwa
            if not self.przech_sze or self.przech_sze == 0 or is_new:
                self.przech_sze = self.element_katalogowy.szerokosc
            if not self.przech_gl or self.przech_gl == 0 or is_new:
                self.przech_gl = self.element_katalogowy.glebokosc
            if not self.przech_wys or self.przech_wys == 0 or is_new:
                self.przech_wys = self.element_katalogowy.wysokosc
            if not self.przech_pow or self.przech_pow == 0 or is_new:
                self.przech_pow = self.element_katalogowy.powierzchnia

            # Sprawdź, czy ten element katalogowy był już używany w tym okresie
            if is_new and self.okres:
                existing_elements = Sklad.objects.filter(
                    element_katalogowy=self.element_katalogowy,
                    okres=self.okres
                ).exists()

                # Jeśli to pierwszy wpis tego elementu w tym okresie, ustaw liczyc=True
                if not existing_elements:
                    self.liczyc = True
                else:
                    self.liczyc = False

        # Określ, czy koszty powinny być przeliczone (nowy obiekt, zmiana stawki, zmiana wymiarów, zmiana dat)
        recalculate_costs = is_new  # Zawsze przeliczamy dla nowych obiektów

        if old_instance:
            # Sprawdź czy któreś z pól wpływających na koszt uległo zmianie
            if (old_instance.stawka.amount != self.stawka.amount or
                    old_instance.przech_pow != self.przech_pow or
                    old_instance.czas_od != self.czas_od or
                    old_instance.czas_do != self.czas_do or
                    old_instance.ilosc_dni != self.ilosc_dni):
                recalculate_costs = True

        # Obliczanie kosztów przechowywania w zależności od scenariusza
        if self.okres and self.czas_od and self.czas_do and self.stawka.amount and recalculate_costs:
            # SCENARIUSZ 1: Ręczne dodanie elementu (zawsze liczymy koszt)
            if not self.element_katalogowy:
                if self.przech_pow and self.ilosc_dni:
                    self.koszt_przech = (self.przech_pow * (self.stawka.amount / 30) * self.ilosc_dni)
                    self.liczyc = True
                else:
                    self.liczyc = False

            # SCENARIUSZ 2: Wybór z elementu katalogowego (liczymy tylko jeśli liczyc=True)
            elif self.element_katalogowy and self.liczyc:
                if self.przech_pow and self.ilosc_dni:
                    self.koszt_przech = (self.przech_pow * (self.stawka.amount / 30) * self.ilosc_dni)

            # Dla elementów katalogowych z liczyc=False, koszt=0
            elif self.element_katalogowy and not self.liczyc:
                self.koszt_przech = 0
        elif not self.okres or not self.czas_od or not self.czas_do or not self.stawka.amount:
            # Brak okresu lub dat lub stawki = koszt zerowy
            self.koszt_przech = 0

        # Jeśli zwolnione=True, to ustawiamy koszt_przech=0 i liczyc=False
        if self.zwolnione:
            self.koszt_przech = 0
            self.liczyc = False

        # NOWY KOD: Ustawienie pól suma i suma_zw w zależności od pola zwolnione
        currency = self.koszt_przech.currency if hasattr(self.koszt_przech, 'currency') else 'EUR'

        if self.zwolnione:
            # Dla zwolnionych, suma_zw przechowuje koszt_przech (lub wartość przeniesioną z suma), a suma jest zerowa
            if old_instance and not old_instance.zwolnione and hasattr(old_instance.suma, 'amount'):
                # Jeśli zmiana z False na True, przenieś wartość z suma do suma_zw
                self.suma_zw = old_instance.suma
            else:
                # W przeciwnym razie, użyj koszt_przech
                self.suma_zw = self.koszt_przech

            # Zawsze zeruj suma dla zwolnionych
            self.suma = Money(0, currency)
        else:
            # Dla niezwolnionych, suma przechowuje koszt_przech (lub wartość przeniesioną z suma_zw), a suma_zw jest zerowa
            if old_instance and old_instance.zwolnione and hasattr(old_instance.suma_zw, 'amount'):
                # Jeśli zmiana z True na False, przenieś wartość z suma_zw do suma
                self.suma = old_instance.suma_zw
            else:
                # W przeciwnym razie, użyj koszt_przech
                self.suma = self.koszt_przech

            # Zawsze zeruj suma_zw dla niezwolnionych
            self.suma_zw = Money(0, currency)

        # Zapisz obiekt
        super().save(*args, **kwargs)

        # Dodaj wpis do historii palet, jeśli numer palety się zmienił
        if old_instance and old_instance.przech_nrpalet != self.przech_nrpalet:
            HistoriaPalety.objects.create(
                sklad=self,
                numer_palety=self.przech_nrpalet,
                zmieniajacy="test"  # self.zmodyfikowany_przez
            )
        elif is_new and self.przech_nrpalet:
            HistoriaPalety.objects.create(
                sklad=self,
                numer_palety=self.przech_nrpalet,
                zmieniajacy="test"  # self.utworzony_przez
            )


    class Meta:
        verbose_name = "Sklad"
        verbose_name_plural = "Sklady"
        ordering = ['firma', 'nr_sde', 'przech_nazwa']

