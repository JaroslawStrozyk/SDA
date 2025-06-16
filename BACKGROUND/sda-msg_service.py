#!/opt/SD/env/bin/python3
#
#  wersja 0.6.0 z 2022.03.13
#
#  pip3 install SkPy
#  pip3 install psycopg2-binary
#
# Uwaga! pole adresata ma ograniczoną ilość znaków < 38znaków
#

import time
import psycopg2
from skpy import Skype
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pass_file import SKY_USER, SKY_PASS, EMAIL_USER, EMAIL_PASS, EMAIL_SMTP, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DBAS



def Logi(i, s, kto):
    modul_id = 11
    now = datetime.now()
    data = now.strftime("%Y-%m-%d")
    godz = now.strftime("%H:%M:%S")

    komunikat_id = 3 + int(i)

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


def msg_skype(to_send, content):
    sk = Skype(SKY_USER, SKY_PASS)
    sk.user
    sk.contacts
    sk.chats
    ch = sk.contacts[to_send].chat
    ch.sendMsg(content)
    return ch.getMsgs()


def msg_email(send_to, subject, body):
    msg = MIMEMultipart()
    sender = EMAIL_USER
    password = EMAIL_PASS
    msg['From'] = sender
    msg['To'] = send_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    text=msg.as_string()
    server = smtplib.SMTP(EMAIL_SMTP)
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender, send_to, text)
    server.close()


def del_db():
    try:
        conn = psycopg2.connect(user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT, database = DB_DBAS)
        cur = conn.cursor()
        sql_delete_query = """Delete from public.\"TaskAPI_asp\""""
        cur.execute(sql_delete_query)
        conn.commit()
    except (Exception, psycopg2.Error) as error :
        Logi(3, str(error),'sda')
    finally:
        if(conn):
            cur.close()
            conn.close()


def read_db():
    try:
        conn = psycopg2.connect(user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT, database = DB_DBAS)
        cur = conn.cursor()
        cur.execute('SELECT * FROM public."TaskAPI_asp"')
        rows = cur.fetchall()

        for r in rows:
           if r[1]==1:
               if r[2]!="":
                  msg_skype(r[2], r[4])
                  Logi(0, r[2],'sda')
                  time.sleep(5)

           if r[1]==2:
               if r[2]!="":
                  i = r[0]
                  msg_email( r[2], r[3], r[4])
                  Logi(1, r[2],'sda')
                  time.sleep(1)

    except (Exception, psycopg2.Error) as error :
        print("ERR=> ",error)
        Logi(2, str(error),'sda')
    finally:
        if(conn):
            cur.close()
            conn.close()
    del_db()


while( 1 ):
     read_db()
     time.sleep( 20 )


