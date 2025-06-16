#!/opt/SD/env/bin/python3
#
#
#  wersja 2.0 z 2024.02.18
#

from datetime import datetime
import psycopg2
from moneyed import Money, PLN
import time

from pass_file import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DBAS



'''
######################################## 2022/2023/2024 ###################################################
'''
# Tabela: ORDERS, Wyjście: ID SDA, SUMA PLN i ROK dla PLN       # rokk>2021
SQL_PLN_SDA_ORD_a = 'SELECT nr_sde_id, sum(kwota_netto), max(rokk) FROM public.\"ORDERS_zamowienie\" WHERE nr_sde_id IS NOT NULL AND rokk>'
SQL_PLN_SDA_ORD_b = ' AND kwota_netto_currency=\'PLN\' GROUP BY nr_sde_id ORDER BY nr_sde_id ASC;'


# Tabela: ORDERS, Wyjście: ID SDA, SUMA PLN i ROK dla Innych walut # rokk>2021
SQL_NPL_SDA_ORD_a = 'SELECT nr_sde_id, sum(kwota_netto_pl), max(rokk) FROM public.\"ORDERS_zamowienie\" WHERE nr_sde_id IS NOT NULL AND rokk>'
SQL_NPL_SDA_ORD_b = ' AND kwota_netto_pl>0 GROUP BY nr_sde_id ORDER BY nr_sde_id ASC;'


# Tabela: ORDERS, Wyjście: ID MPK, SUMA PLN i ROK dla PLN
SQL_PLN_MPK_ORD = 'SELECT nr_mpk_id, sum(kwota_netto), max(rokk) FROM public.\"ORDERS_zamowienie\" WHERE nr_mpk_id IS NOT NULL AND nr_sde_id IS NULL AND kwota_netto_currency=\'PLN\' AND rok='

# Tabela: ORDERS, Wyjście: ID SDA, SUMA PLN i ROK dla Innych walut
SQL_NPL_MPK_ORD = 'SELECT nr_mpk_id, sum(kwota_netto_pl), max(rokk) FROM public.\"ORDERS_zamowienie\" WHERE nr_mpk_id IS NOT NULL AND nr_sde_id IS NULL AND kwota_netto_pl>0 AND rok='

SQL_MPK_ORD     = ' GROUP BY nr_mpk_id;'


# Tabela: ORDERS, Wyjście: ID SDA, ID MPK, SUMA PLN, SUMA INNE i ROK
SQL_PL_SDAMPK_ORD_a = 'SELECT nr_sde_id, nr_mpk_id, sum(kwota_netto), sum(kwota_netto_pl), max(rokk) FROM public.\"ORDERS_zamowienie\" WHERE nr_sde_id IS NOT NULL AND nr_mpk_id IS NOT NULL AND rokk>'
SQL_PL_SDAMPK_ORD_b = ' GROUP BY nr_sde_id, nr_mpk_id;'  #2022 rokk>2021  AND kwota_netto_currency=\'PLN\'


# Tabela: CASH_ADVANCIES, Wyjście: ID SDA, SUMA PLN i ROK dla PLN
SQL_PLN_SDA_CASH_a = 'SELECT nr_sde_id, sum(kwota_netto), max(rok) FROM public.\"CASH_ADVANCES_pozycja\" WHERE nr_sde_id IS NOT NULL AND rok>'
SQL_PLN_SDA_CASH_b = ' AND kwota_netto_currency=\'PLN\' GROUP BY nr_sde_id ORDER BY nr_sde_id ASC;'

# Tabela: CASH_ADVANCIES, Wyjście: ID SDA, SUMA PLN i ROK dla Innych walut
SQL_NPL_SDA_CASH_a = 'SELECT nr_sde_id, sum(kwota_netto_pl), max(rok) FROM public.\"CASH_ADVANCES_pozycja\" WHERE nr_sde_id IS NOT NULL AND rok>'
SQL_NPL_SDA_CASH_b = ' AND kwota_netto_pl>0 GROUP BY nr_sde_id ORDER BY nr_sde_id ASC;'

# Tabela: CASH_ADVANCIES, Wyjście: ID MPK, SUMA PLN i ROK dla PLN
SQL_PLN_MPK_CASH = 'SELECT nr_mpk_id, sum(kwota_netto), max(rok) FROM public.\"CASH_ADVANCES_pozycja\" WHERE nr_mpk_id IS NOT NULL AND kwota_netto_currency=\'PLN\' AND rok='

# Tabela: CASH_ADVANCIES, Wyjście: ID MPK, SUMA PLN i ROK dla Innych Walut
SQL_NPL_MPK_CASH = 'SELECT nr_mpk_id, sum(kwota_netto_pl), max(rok) FROM public.\"CASH_ADVANCES_pozycja\" WHERE nr_mpk_id IS NOT NULL AND kwota_netto_pl>0 AND rok='

SQL_MPK_CASH     = ' GROUP BY nr_mpk_id ORDER BY nr_mpk_id ASC;'

# Tabela wzorzec SDA
SQL_SDA_a = 'SELECT id, sum_direct, sum_cash FROM public.\"ORDERS_nrsde\" WHERE rokk>'
SQL_SDA_b = ' ORDER BY id ASC;' #, nazwa, rokk 2020

# Tabela wzorzec MPK
SQL_MPK  = 'SELECT id, sum_zam, sum_zal, suma FROM public."ORDERS_nrmpk" WHERE rok='
SQL_MPK_ = ' ORDER BY id ASC;'


# Wypełnianie tabeli miesiące (MPK)
SQL_MPK_GET  = 'SELECT id FROM public."ORDERS_nrmpk" WHERE rok='
SQL_MPK_GET_ = ' ORDER BY id ASC;'
SQL_MPK_PLN_MC_ORD = 'SELECT nr_mpk_id, kwota_netto, data_fv FROM public.\"ORDERS_zamowienie\"' \
                     ' WHERE nr_mpk_id IS NOT NULL AND kwota_netto_currency=\'PLN\' AND rok='
SQL_MPK_NPL_MC_ORD = 'SELECT nr_mpk_id, kwota_netto_pl, data_fv FROM public.\"ORDERS_zamowienie\"' \
                     ' WHERE nr_mpk_id IS NOT NULL AND kwota_netto_pl>0 AND rok='
SQL_MPK_PLN_MC_CASH = 'SELECT nr_mpk_id, kwota_netto, data_zak FROM public.\"CASH_ADVANCES_pozycja\"' \
                   'WHERE nr_mpk_id IS NOT NULL AND kwota_netto_currency=\'PLN\' AND rok='
SQL_MPK_NPL_MC_CASH = 'SELECT nr_mpk_id, kwota_netto_pl, data_zak FROM public.\"CASH_ADVANCES_pozycja\"' \
                   'WHERE nr_mpk_id IS NOT NULL AND kwota_netto_pl>0 AND rok='
SQL_PREM_MPK = 'SELECT'\
    ' (\"WORKER_premia_det\".del_ilosc_razem + \"WORKER_premia_det\".ind_pr_kwota + \"WORKER_premia_det\".pr_wartosc'\
    '+ \"WORKER_premia_det\".premia_proj) AS suma, \"WORKER_pensja\".miesiac, \"WORKER_pensja\".rok '\
    'FROM public.\"WORKER_premia_det\" INNER JOIN public.\"WORKER_pensja\" ON \"WORKER_premia_det\".pensja_id = \"WORKER_pensja\".id'\
    ' WHERE projekt_id IS NULL;'

SQL_MAGAZYN_DRE = 'SELECT kwota_currency, kwota, nr_sde_id, plyta_id, rokk FROM public.\"TIMBER_WH_rozchod\"'\
                  'WHERE nr_sde_id IS NOT NULL AND rokk='

SQL_MAGAZYN_WEW = 'SELECT kwota_currency, kwota, nr_sde_id, pozycja_id, rokk FROM public.\"INTER_WH_rozchod_poz\"'\
                  'WHERE nr_sde_id IS NOT NULL AND rokk='

# Sprawdza czy coś się zmieniło we flagach zmian
def TestChange(cur):
    cur.execute('SELECT id, zamowienie, pozycja, rozliczenie, licznik FROM public."TaskAPI_flagazmiany"')
    rows = cur.fetchall()

    # ZAMÓWIENIE, POZYCJA
    f = 0
    if rows[0][1] > 0:
        f += 1
    if rows[0][2] > 0:
        f += 1
    if rows[0][3] > 0:
        f += 1

    return f


# Ustawia flagę "Wyślij do Google" i kasuje pozostałe
def SendToGoogle(conn, cur):
    sql_delete_query = """UPDATE public.\"TaskAPI_flagazmiany\" SET do_google=1,  zamowienie=0, pozycja=0  WHERE id = 1"""
    cur.execute(sql_delete_query)
    conn.commit()


# Wybiera i sumuje pola dla SDA i MPK z tabel ORDERS I CASH...
# Rok potrzebny tylko dla wartości MPK
def Read_Calc_Table(cur, st, rok):
    sql  = ''
    rows = ''
    if   st == 'ord_sda_pln':
        sql = SQL_PLN_SDA_ORD_a + str(rok-3) + SQL_PLN_SDA_ORD_b
    elif st == 'ord_sda_npl':
        sql = SQL_NPL_SDA_ORD_a + str(rok-3) + SQL_NPL_SDA_ORD_b
    elif st == 'ord_mpk_pln':
        sql = SQL_PLN_MPK_ORD + str(rok) + SQL_MPK_ORD
    elif st == 'ord_mpk_npl':
        sql = SQL_NPL_MPK_ORD + str(rok) + SQL_MPK_ORD
    elif st == 'cash_sda_pln':
        sql = SQL_PLN_SDA_CASH_a + str(rok-3) + SQL_PLN_SDA_CASH_b
    elif st == 'cash_sda_npl':
        sql = SQL_NPL_SDA_CASH_a + str(rok-3) + SQL_NPL_SDA_CASH_b
    elif st == 'cash_mpk_pln':
        sql = SQL_PLN_MPK_CASH + str(rok) + SQL_MPK_CASH
    elif st == 'cash_mpk_npl':
        sql = SQL_NPL_MPK_CASH + str(rok) + SQL_MPK_CASH
    elif st == 'sql_sda':
        sql = SQL_SDA_a + str(rok-2) + SQL_SDA_b
    elif st == 'sql_mpk':
        sql = SQL_MPK + str(rok) + SQL_MPK_


    if sql != '':
        cur.execute(sql)
        rows = cur.fetchall()

    return rows


def CalcSDA(w_sda, ord_sda_pln, ord_sda_npl, cash_sda_pln, cash_sda_npl):
    tsda = []
    zero = Money('00.00', PLN).amount
    for id_sda in w_sda:
        ind = id_sda[0]

        # tymczasowa tabela
        row = [ind, zero, zero]

        # Suma SDA ORDERS dla PLN
        for d_pln in ord_sda_pln:
            if ind == d_pln[0]:
                row[1] = row[1] + d_pln[1]

        # Suma SDA ORDERS dla Innych
        for d_npl in ord_sda_npl:
            if ind == d_npl[0]:
                row[1] = row[1] + d_npl[1]

        # Suma SDA CASH dla PLN
        for d_pln in cash_sda_pln:
            if ind == d_pln[0]:
                row[2] = row[2] + d_pln[1]

        # Suma SDA CASH dla Innych
        for d_npl in cash_sda_npl:
            if ind == d_npl[0]:
                row[2] = row[2] + d_npl[1]

        tsda.append(row)

    return tsda


def CalcMPK(w_mpk, ord_mpk_pln, ord_mpk_npl, cash_mpk_pln, cash_mpk_npl):
    tmpk = []
    zero = Money('00.00', PLN).amount

    for id_mpk in w_mpk:
        ind = id_mpk[0]

        # tymczasowa tabela
        row = [ind, zero, zero, zero]

        for c_pln in ord_mpk_pln:
            if ind == c_pln[0]:
                row[1] = row[1] + c_pln[1]

        for c_pln in ord_mpk_npl:
            if ind == c_pln[0]:
                row[1] = row[1] + c_pln[1]

        for c_pln in cash_mpk_pln:
            if ind == c_pln[0]:
                row[2] = row[2] + c_pln[1]

        for c_pln in cash_mpk_npl:
            if ind == c_pln[0]:
                row[2] = row[2] + c_pln[1]

        row[3] = row[1] + row[2]

        tmpk.append(row)

    return tmpk


def SDA_MPKtoDB(cur, conn, calc_sda, calc_mpk):
    for d in calc_sda:
        dquery = 'UPDATE public.\"ORDERS_nrsde\" SET sum_direct='+str(d[1])+', sum_cash='+str(d[2])+' WHERE id='+str(d[0])
        cur.execute(dquery)
        conn.commit()

    for c in calc_mpk:
        cquery = 'UPDATE public.\"ORDERS_nrmpk\" SET sum_zam='+str(c[1])+', sum_zal='+str(c[2])+', suma='+str(c[3])+' WHERE id='+str(c[0])
        cur.execute(cquery)
        conn.commit()


def ReadMpkTable(cur, rok):

    tmpk = []
    zero = Money('00.00', PLN).amount

    sql = SQL_MPK_GET + str(rok) + SQL_MPK_GET_
    cur.execute(sql)
    rows = cur.fetchall()

    for id_mpk in rows:
        # id , st, lu, ma, kw, ma, cz, li, si, wr, pa, lp, gr, b_d
        row = [id_mpk[0], zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero]
        tmpk.append(row)

    return tmpk


def GetDataOrdCash(cur, rok, st):
    sql  = ''
    rows = ''
    if   st == 'mpk_ord_pln':
        sql = SQL_MPK_PLN_MC_ORD + str(rok) + ';'
    elif st == 'mpk_ord_npl':
        sql = SQL_MPK_NPL_MC_ORD + str(rok) + ';'
    elif st == 'mpk_cash_pln':
        sql = SQL_MPK_PLN_MC_CASH + str(rok) + ';'
    elif st == 'mpk_cash_npl':
        sql = SQL_MPK_NPL_MC_CASH + str(rok) + ';'
    elif st == 'prem_mpk':
        sql = SQL_PREM_MPK

    if sql != '':
        cur.execute(sql)
        rows = cur.fetchall()

    return rows


def CalcYear(w_mpk_mc, mpk_ord_pln, mpk_ord_npl, mpk_cash_pln, mpk_cash_npl, prem_mpk_pln, rok):

    for m_mpk in w_mpk_mc:
        ind = m_mpk[0]

        for i_pln in mpk_ord_pln:
            if ind == i_pln[0]:
                try:
                    d = datetime.strptime(str(i_pln[2]), '%Y-%m-%d')
                    m = int(d.strftime('%m'))
                except:
                    m = 13 # nie ma daty więc nie można przypisać miesiąca
                m_mpk[m] = m_mpk[m] + i_pln[1]

        for i_pln in mpk_ord_npl:
            if ind == i_pln[0]:
                try:
                    d = datetime.strptime(str(i_pln[2]), '%Y-%m-%d')
                    m = int(d.strftime('%m'))
                except:
                    m = 13 # nie ma daty więc nie można przypisać miesiąca
                m_mpk[m] = m_mpk[m] + i_pln[1]

        for i_pln in mpk_cash_pln:
            if ind == i_pln[0]:
                try:
                    d = datetime.strptime(str(i_pln[2]), '%Y-%m-%d')
                    m = int(d.strftime('%m'))
                except:
                    m = 13 # nie ma daty więc nie można przypisać miesiąca
                m_mpk[m] = m_mpk[m] + i_pln[1]

        for i_pln in mpk_cash_npl:
            if ind == i_pln[0]:
                try:
                    d = datetime.strptime(str(i_pln[2]), '%Y-%m-%d')
                    m = int(d.strftime('%m'))
                except:
                    m = 13 # nie ma daty więc nie można przypisać miesiąca
                m_mpk[m] = m_mpk[m] + i_pln[1]

    id_mpk = 170  # MPK 464
    for m_mpk in w_mpk_mc:
        ind = m_mpk[0]
        if ind == id_mpk:

            for i_pln in prem_mpk_pln:
                if i_pln[2] == rok:
                    wartosc = i_pln[0]
                    m = i_pln[1]
                    m_mpk[m] = m_mpk[m] + wartosc

    return w_mpk_mc


def DateToDB(cur, conn, calc_rok):

    for d in calc_rok:
            dquery = 'UPDATE public.\"ORDERS_nrmpk\" SET st='+str(d[1])+', lu='+str(d[2])+', ma='+str(d[3])+', kw='\
                     +str(d[4])+', mj='+str(d[5])+', cz='+str(d[6])+', lp='+str(d[7])+', si='+str(d[8])+', wr='\
                     +str(d[9])+', pa='+str(d[10])+', li='+str(d[11])+', gr='+str(d[12])+', b_d='+str(d[13])\
                     +' WHERE id='+str(d[0])
            cur.execute(dquery)
            conn.commit()


def Logi(i, s, kto):
    modul_id = 10
    shift = 1
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")

    komunikat_id = shift + int(i)

    try:
        conn = psycopg2.connect(user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT, database = DB_DBAS)
        cur = conn.cursor()
        sql = 'INSERT INTO public.\"LOG_log\"(data, godz, modul_id, komunikat_id, opis, kto) VALUES (\'' \
              + data + '\', \'' + godz + '\', ' + str(modul_id) + ', ' + str(komunikat_id) + ', \'' + s + '\', \''+str(kto)+'\');'
        cur.execute(sql)
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if (conn):
            cur.close()
            conn.close()


def Przelicz(conn, cur, rok):

    w_sda = Read_Calc_Table(cur, 'sql_sda', rok)
    ord_sda_pln = Read_Calc_Table(cur, 'ord_sda_pln', rok)
    ord_sda_npl = Read_Calc_Table(cur, 'ord_sda_npl', rok)
    cash_sda_pln = Read_Calc_Table(cur, 'cash_sda_pln', rok)
    cash_sda_npl = Read_Calc_Table(cur, 'cash_sda_npl', rok)


    w_mpk = Read_Calc_Table(cur, 'sql_mpk', rok)
    ord_mpk_pln = Read_Calc_Table(cur, 'ord_mpk_pln', rok)
    ord_mpk_npl = Read_Calc_Table(cur, 'ord_mpk_npl', rok)
    cash_mpk_pln = Read_Calc_Table(cur, 'cash_mpk_pln', rok)
    cash_mpk_npl = Read_Calc_Table(cur, 'cash_mpk_npl', rok)


    calc_sda = CalcSDA(w_sda, ord_sda_pln, ord_sda_npl, cash_sda_pln, cash_sda_npl)
    calc_mpk = CalcMPK(w_mpk, ord_mpk_pln, ord_mpk_npl, cash_mpk_pln, cash_mpk_npl)
    SDA_MPKtoDB(cur, conn, calc_sda, calc_mpk)

    # ROZKŁAD KOSZTÓW NA MIESIĄCE
    w_mpk_mc = ReadMpkTable(cur, rok)
    mpk_ord_pln = GetDataOrdCash(cur, rok, 'mpk_ord_pln')
    mpk_ord_npl = GetDataOrdCash(cur, rok, 'mpk_ord_npl')
    mpk_cash_pln = GetDataOrdCash(cur, rok, 'mpk_cash_pln')
    mpk_cash_npl = GetDataOrdCash(cur, rok, 'mpk_cash_npl')
    prem_mpk_pln = GetDataOrdCash(cur, rok, 'prem_mpk')


    calc_rok = CalcYear(w_mpk_mc, mpk_ord_pln, mpk_ord_npl, mpk_cash_pln, mpk_cash_npl, prem_mpk_pln, rok)
    DateToDB(cur, conn, calc_rok)


'''
Indeksy:
    |======|==============================|
    | 2023 | 210	"402-11-1" mpk_402111 |
    |      | 211	"402-11-2" mpk_402112 |
    |      | 240	"403-16-1" mpk_403161 |
    |      | 241	"403-16-2" mpk_403162 |
    |      | 242	"403-16-3" mpk_403163 |
    |      | 243	"403-16-4" mpk_403164 |
    |      | 244	"403-16-5" mpk_403165 |
    |      | 245	"403-16-6" mpk_403166 |
    |      | 246	"403-16-7" mpk_403167 |
    |======|==============================|
    | 2024 | 328	"402-11-1" mpk_402111 |
    |      | 329	"402-11-2" mpk_402112 |
    |      | 293	"403-16-1" mpk_403161 |
    |      | 310	"403-16-2" mpk_403162 |
    |      | 307	"403-16-3" mpk_403163 |
    |      | 308	"403-16-4" mpk_403164 |
    |      | 339	"403-16-5" mpk_403165 |
    |      | 309	"403-16-6" mpk_403166 |
    |      | 340	"403-16-7" mpk_403167 |
    |======|==============================|    

Tabela:
    sm[0] - id SDE
    sm[1] - id MPK
    sm[2] - kwota dla sumy polskiej
    sm[3] - kwota inna (po przeliczeniu na polskie)
    sm[4] - rok
'''
def PrzeliczSDEMPK(conn, cur, brok):

    SQL_PL_SDAMPK_ORD = SQL_PL_SDAMPK_ORD_a + str(brok-2) + SQL_PL_SDAMPK_ORD_b

    cur.execute(SQL_PL_SDAMPK_ORD)
    sdampk = cur.fetchall()
    dquery = ''
    for sm in sdampk:
        dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_402111=0, mpk_402112=0, mpk_403161=0, mpk_403162=0, mpk_403163=0, mpk_403164=0, mpk_403165=0, mpk_403166=0, mpk_403167=0  WHERE id=' + str(sm[0])
        if dquery != '':
            cur.execute(dquery)
            conn.commit()

    for sm in sdampk:

        if sm[3] > 0:
            val = sm[3]
        else:
            val = sm[2]

        # 2023
        if sm[1] == 210:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_402111=' + str(val) + '  WHERE id=' + str(sm[0]) # str(sm[2] + sm[3])
        elif sm[1] == 211:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_402112=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 240:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403161=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 241:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403162=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 242:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403163=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 243:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403164=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 244:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403165=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 245:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403166=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 246:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403167=' + str(val) + '  WHERE id=' + str(sm[0])
        # 2024
        elif sm[1] == 328:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_402111=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 329:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_402112=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 293:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403161=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 310:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403162=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 307:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403163=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 308:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403164=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 339:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403165=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 309:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403166=' + str(val) + '  WHERE id=' + str(sm[0])
        elif sm[1] == 340:
            dquery = 'UPDATE public.\"ORDERS_nrsde\" SET mpk_403167=' + str(val) + '  WHERE id=' + str(sm[0])

        if dquery != '':
            cur.execute(dquery)
            conn.commit()


def PrzeliczDelegacje(conn, cur, brok):
    dquery = 'SELECT kod_sde_targi1_id, kod_sde_targi2_id, sum(roznica_diet_pl), sum(sde_targi1_pln), sum(sde_targi2_pln) ' \
             'FROM public.\"DELEGATIONS_delegacja\" WHERE kod_sde_targi1_id IS NOT NULL OR kod_sde_targi2_id IS NOT NULL ' \
             'GROUP BY kod_sde_targi1_id, kod_sde_targi2_id;'
    cur.execute(dquery)
    delegacja = cur.fetchall()
    for dl in delegacja:
        q = 'UPDATE public.\"ORDERS_nrsde\" SET del_roznica=' + str(dl[2]) + ', del_wyjazd=' + str(dl[3]) +' WHERE id=' + str(dl[0])
        if dquery != '':
            cur.execute(q)
            conn.commit()


def OrderCashCalc():
    try:
        conn = psycopg2.connect(user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT, database = DB_DBAS)
        cur = conn.cursor()

        tst = TestChange(cur)

        brok = datetime.now().year    #2024 # 2023
        #tst = 1

        if tst > 0:
            Przelicz(conn, cur, (brok - 1))
            Przelicz(conn, cur, brok)
            PrzeliczSDEMPK(conn, cur, brok)
            PrzeliczDelegacje(conn, cur, brok)

    except (Exception, psycopg2.Error) as error:
        Logi(1, str(error),'sda')
    finally:
        if (conn):
            cur.close()
            conn.close()


'''
##################################################################################################
'''

# OrderCashCalc()


while(1):
    OrderCashCalc()
    time.sleep(15)
