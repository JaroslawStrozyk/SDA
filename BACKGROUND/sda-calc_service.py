#!/opt/SD/env/bin/python3
#
#
#  wersja 0.6.0 z 2021.12.16
#

from datetime import datetime
import psycopg2
from moneyed import Money, PLN
import time
from pass_file import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DBAS



'''
######################################## 2022 ###################################################
'''
# Tabela: ORDERS, Wyjście: ID SDA, SUMA PLN i ROK dla PLN
SQL_PLN_SDA_ORD = 'SELECT nr_sde_id, sum(kwota_netto), max(rokk) FROM public.\"ORDERS_zamowienie\"' \
                  ' WHERE nr_sde_id IS NOT NULL AND rokk>2020 AND kwota_netto_currency=\'PLN\'' \
                  ' GROUP BY nr_sde_id ORDER BY nr_sde_id ASC;'

# Tabela: ORDERS, Wyjście: ID SDA, SUMA PLN i ROK dla Innych walut
SQL_NPL_SDA_ORD = 'SELECT nr_sde_id, sum(kwota_netto_pl), max(rokk) FROM public.\"ORDERS_zamowienie\"' \
                  ' WHERE nr_sde_id IS NOT NULL AND rokk>2020 AND kwota_netto_pl>0' \
                  ' GROUP BY nr_sde_id ORDER BY nr_sde_id ASC;'

# Tabela: ORDERS, Wyjście: ID MPK, SUMA PLN i ROK dla PLN
SQL_PLN_MPK_ORD = 'SELECT nr_mpk_id, sum(kwota_netto), max(rokk) FROM public.\"ORDERS_zamowienie\"' \
                  ' WHERE nr_mpk_id IS NOT NULL AND kwota_netto_currency=\'PLN\' AND rok='

# Tabela: ORDERS, Wyjście: ID SDA, SUMA PLN i ROK dla Innych walut
SQL_NPL_MPK_ORD = 'SELECT nr_mpk_id, sum(kwota_netto_pl), max(rokk) FROM public.\"ORDERS_zamowienie\"' \
                  ' WHERE nr_mpk_id IS NOT NULL AND kwota_netto_pl>0 AND rok='

SQL_MPK_ORD     = ' GROUP BY nr_mpk_id ORDER BY nr_mpk_id ASC;'


# Tabela: CASH_ADVANCIES, Wyjście: ID SDA, SUMA PLN i ROK dla PLN
SQL_PLN_SDA_CASH = 'SELECT nr_sde_id, sum(kwota_netto), max(rok) FROM public.\"CASH_ADVANCES_pozycja\"' \
                   ' WHERE nr_sde_id IS NOT NULL AND rok>2020 AND kwota_netto_currency=\'PLN\'' \
                   ' GROUP BY nr_sde_id ORDER BY nr_sde_id ASC;'

# Tabela: CASH_ADVANCIES, Wyjście: ID SDA, SUMA PLN  i ROK dla Innych walut
SQL_NPL_SDA_CASH = 'SELECT nr_sde_id, sum(kwota_netto_pl), max(rok) FROM public.\"CASH_ADVANCES_pozycja\"' \
                  ' WHERE nr_sde_id IS NOT NULL AND rok>2020 AND kwota_netto_pl>0' \
                  ' GROUP BY nr_sde_id ORDER BY nr_sde_id ASC;'

# Tabela: CASH_ADVANCIES, Wyjście: ID MPK, SUMA PLN i ROK dla PLN
SQL_PLN_MPK_CASH = 'SELECT nr_mpk_id, sum(kwota_netto), max(rok) FROM public.\"CASH_ADVANCES_pozycja\"' \
                   'WHERE nr_mpk_id IS NOT NULL AND kwota_netto_currency=\'PLN\' AND rok='

# Tabela: CASH_ADVANCIES, Wyjście: ID MPK, SUMA PLN i ROK dla Innych Walut
SQL_NPL_MPK_CASH = 'SELECT nr_mpk_id, sum(kwota_netto_pl), max(rok) FROM public.\"CASH_ADVANCES_pozycja\"' \
                   'WHERE nr_mpk_id IS NOT NULL AND kwota_netto_pl>0 AND rok='

SQL_MPK_CASH     = ' GROUP BY nr_mpk_id ORDER BY nr_mpk_id ASC;'

# Tabela wzorzec SDA
SQL_SDA = 'SELECT id, sum_direct, sum_cash FROM public.\"ORDERS_nrsde\" WHERE rokk>2020 ORDER BY id ASC;' #, nazwa, rokk

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
        sql = SQL_PLN_SDA_ORD
    elif st == 'ord_sda_npl':
        sql = SQL_NPL_SDA_ORD
    elif st == 'ord_mpk_pln':
        sql = SQL_PLN_MPK_ORD + str(rok) + SQL_MPK_ORD
    elif st == 'ord_mpk_npl':
        sql = SQL_NPL_MPK_ORD + str(rok) + SQL_MPK_ORD
    elif st == 'cash_sda_pln':
        sql = SQL_PLN_SDA_CASH
    elif st == 'cash_sda_npl':
        sql = SQL_NPL_SDA_CASH
    elif st == 'cash_mpk_pln':
        sql = SQL_PLN_MPK_CASH + str(rok) + SQL_MPK_CASH
    elif st == 'cash_mpk_npl':
        sql = SQL_NPL_MPK_CASH + str(rok) + SQL_MPK_CASH
    elif st == 'sql_sda':
        sql = SQL_SDA
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

    if sql != '':
        cur.execute(sql)
        rows = cur.fetchall()

    return rows


def CalcYear(w_mpk_mc, mpk_ord_pln, mpk_ord_npl, mpk_cash_pln, mpk_cash_npl):

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


# Poprawić do wzorca
def OrderCashCalc(rok):
    try:
        conn = psycopg2.connect(user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT, database = DB_DBAS)
        cur = conn.cursor()

        if TestChange(cur) > 0:

            w_sda        = Read_Calc_Table(cur, 'sql_sda', rok)
            ord_sda_pln  = Read_Calc_Table(cur, 'ord_sda_pln', rok)
            ord_sda_npl  = Read_Calc_Table(cur, 'ord_sda_npl', rok)
            cash_sda_pln = Read_Calc_Table(cur, 'cash_sda_pln', rok)
            cash_sda_npl = Read_Calc_Table(cur, 'cash_sda_npl', rok)

            w_mpk        = Read_Calc_Table(cur, 'sql_mpk', rok)
            ord_mpk_pln  = Read_Calc_Table(cur, 'ord_mpk_pln', rok)
            ord_mpk_npl  = Read_Calc_Table(cur, 'ord_mpk_npl', rok)
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

            calc_rok = CalcYear(w_mpk_mc, mpk_ord_pln, mpk_ord_npl, mpk_cash_pln, mpk_cash_npl)

            DateToDB(cur, conn, calc_rok)


            SendToGoogle(conn, cur)


            Logi( 0, "",'sda')

    except (Exception, psycopg2.Error) as error:
            Logi( 1, str(error),'sda')
    finally:
        if (conn):
            cur.close()
            conn.close()


'''
##################################################################################################
'''




while( 1 ):
    OrderCashCalc(2021)
    time.sleep( 15 )
