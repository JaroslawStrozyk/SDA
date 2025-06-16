#!/opt/SD/env/bin/python3
from peewee import *
from datetime import datetime

# Konfiguracja bazy danych
db = PostgresqlDatabase('sda', user='django', password='JAroslaw71!', host='127.0.0.1')


class BaseModel(Model):
    class Meta:
        database = db


class OrdersNrsde(BaseModel):
    rokk = IntegerField()
    rok = IntegerField()
    nazwa = CharField(max_length=255)
    klient = CharField(max_length=255)
    targi = CharField(max_length=255, null=True)
    stoisko = CharField(max_length=255, null=True)
    opis = TextField(null=True)
    pm = CharField(max_length=255, null=True)
    pow_stoisko = IntegerField()
    pow_pietra = IntegerField()
    uwagi = TextField()
    sum_cash = FloatField()
    sum_cash_currency = CharField(max_length=4)
    sum_direct = FloatField()
    sum_direct_currency = CharField(max_length=4)
    fv = CharField(max_length=255)
    c_miesiac = CharField(max_length=255)
    d_miesiac = CharField(max_length=255)
    mcs = CharField(max_length=50)
    rks = CharField(max_length=50)
    nazwa_id = CharField(max_length=50)
    sum_deleg = FloatField()
    sum_deleg_currency = CharField(max_length=4)
    sum_premie = FloatField()
    sum_premie_currency = CharField(max_length=4)
    sum_pre_del = FloatField()
    sum_pre_del_currency = CharField(max_length=4)
    deleg_sum = FloatField()
    deleg_sum_currency = CharField(max_length=4)
    magazyn_dre = FloatField()
    magazyn_dre_currency = CharField(max_length=4)
    magazyn_wewn = FloatField()
    magazyn_wewn_currency = CharField(max_length=4)
    mpk_402111 = FloatField()
    mpk_402111_currency = CharField(max_length=4)
    mpk_402112 = FloatField()
    mpk_402112_currency = CharField(max_length=4)
    mpk_403161 = FloatField()
    mpk_403161_currency = CharField(max_length=4)
    mpk_403162 = FloatField()
    mpk_403162_currency = CharField(max_length=4)
    mpk_403163 = FloatField()
    mpk_403163_currency = CharField(max_length=4)
    mpk_403164 = FloatField()
    mpk_403164_currency = CharField(max_length=4)
    mpk_403165 = FloatField()
    mpk_403165_currency = CharField(max_length=4)
    mpk_403166 = FloatField()
    mpk_403166_currency = CharField(max_length=4)
    mpk_403167 = FloatField()
    mpk_403167_currency = CharField(max_length=4)
    del_roznica = FloatField()
    del_roznica_currency = CharField(max_length=4)
    del_wyjazd = FloatField()
    del_wyjazd_currency = CharField(max_length=4)

    class Meta:
        table_name = 'ORDERS_nrsde'
        schema = 'public'


def db_insert(rokk, rok, nazwa, klient, targi, stoisko, opis, pm, pow_stoisko, pow_pietra):
    """
    Wstawia nowy rekord do bazy danych.

    Returns:
        bool: True jeśli operacja się powiodła, False w przeciwnym razie
    """
    try:
        db.connect()

        zamowienie = OrdersNrsde.create(
            rokk=rokk,
            rok=rok,
            nazwa=nazwa,
            klient=klient,
            targi=targi,
            stoisko=stoisko,
            opis=opis,
            pm=pm,
            pow_stoisko=pow_stoisko,
            pow_pietra=pow_pietra,
            uwagi="Pobrane: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sum_cash=0.00,
            sum_cash_currency='PLN',
            sum_direct=0.00,
            sum_direct_currency='PLN',
            fv='...',
            c_miesiac='...',
            d_miesiac='...',
            mcs='...',
            rks='...',
            nazwa_id='...',
            sum_deleg=0.00,
            sum_deleg_currency='PLN',
            sum_premie=0.00,
            sum_premie_currency='PLN',
            sum_pre_del=0.00,
            sum_pre_del_currency='PLN',
            deleg_sum=0.00,
            deleg_sum_currency='PLN',
            magazyn_dre=0.00,
            magazyn_dre_currency='PLN',
            magazyn_wewn=0.00,
            magazyn_wewn_currency='PLN',
            mpk_402111=0.00,
            mpk_402111_currency='PLN',
            mpk_402112=0.00,
            mpk_402112_currency='PLN',
            mpk_403161=0.00,
            mpk_403161_currency='PLN',
            mpk_403162=0.00,
            mpk_403162_currency='PLN',
            mpk_403163=0.00,
            mpk_403163_currency='PLN',
            mpk_403164=0.00,
            mpk_403164_currency='PLN',
            mpk_403165=0.00,
            mpk_403165_currency='PLN',
            mpk_403166=0.00,
            mpk_403166_currency='PLN',
            mpk_403167=0.00,
            mpk_403167_currency='PLN',
            del_roznica=0.00,
            del_roznica_currency='PLN',
            del_wyjazd=0.00,
            del_wyjazd_currency='PLN'
        )

        db.close()
        return True

    except Exception as e:
        try:
            db.close()
        except:
            pass
        raise e  # Przekaż błąd do wywołującego kodu


# db_insert(2025, 2025, '111_2025', 'klient.', 'targi.', 'stoisko1', 'Opis dotyczący stoiska /stoisko1/', 'J.S.', 0, 0)
