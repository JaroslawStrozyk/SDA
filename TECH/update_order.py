#!/opt/SD/env/bin/python3


import psycopg2
from pass_file import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DBAS


def conn_db(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DBAS):
    stat = 0
    try:

        conn = psycopg2.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_DBAS)

    except (Exception, psycopg2.Error) as error:
        print(error)
        stat = 1

    return conn, stat


def dconn_db(conn):
    conn.close()


def read_company(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM public."ORDERS_nip"')
    rows = cur.fetchall()
    return rows

#
# UPDATE public."ORDERS_zamowienie" SET nip='5213614786', nip_ind_id=12	WHERE kontrahent ILIKE '%eTravel%';
#
def update_order(conn, kid, nip, kontrahent):
    cur = conn.cursor()
    sql = 'UPDATE public.\"ORDERS_zamowienie\" SET kontrahent=\'' + str(kontrahent) + '\', nip=\'' + str(nip) + '\', nip_ind_id=' + str(kid) + ' WHERE kontrahent ILIKE \'%' + str(kontrahent) + '%\''
    cur.execute(sql)
    conn.commit()


def update_order_in(conn, kid, nip, kontrahent, skontrahent):
    cur = conn.cursor()
    sql = 'UPDATE public.\"ORDERS_zamowienie\" SET kontrahent=\'' + str(kontrahent) + '\', nip=\'' + str(nip) + '\', nip_ind_id=' + str(kid) + ' WHERE kontrahent ILIKE \'%' + str(skontrahent) + '%\''
    cur.execute(sql)
    conn.commit()

#
#
#


conn, stat = conn_db(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DBAS)

update_order_in(conn, 1, '7861009035', 'EdataBit Jarosław Stróżyk', 'edatabit')

if stat == 0:
    rows = read_company(conn)

    for r in rows:
        print(f">>> {r[0]}, {r[1]}, {r[2]}.")
        kid = r[0]
        nip = r[1]
        kontrahent = r[2]
        update_order(conn, kid, nip, kontrahent)

dconn_db(conn)