from datetime import datetime


# def Logi(i, s, kto):
#     modul_id = 10
#     shift = 1
#     now = datetime.now()
#     data = now.strftime("%Y-%m-%d")
#     godz = now.strftime("%H:%M:%S")
#
#     komunikat_id = shift + int(i)
#
#     try:
#         conn = psycopg2.connect(user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT, database = DB_DBAS)
#         cur = conn.cursor()
#         sql = 'INSERT INTO public.\"LOG_log\"(data, godz, modul_id, komunikat_id, opis, kto) VALUES (\'' \
#               + data + '\', \'' + godz + '\', ' + str(modul_id) + ', ' + str(komunikat_id) + ', \'' + s + '\', \''+str(kto)+'\');'
#         cur.execute(sql)
#         conn.commit()
#
#     except (Exception, psycopg2.Error) as error:
#         print(error)
#     finally:
#         if (conn):
#             cur.close()
#             conn.close()