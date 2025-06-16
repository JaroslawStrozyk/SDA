#!/opt/SD/env/bin/python3

"""
ReadDocs.py - Szybki odczyt danych z Google Sheets z porównaniem z bazą PostgreSQL
Optymalizowany pod kątem minimalnego czasu odczytu dla zachowania integralności danych
"""

import pandas as pd
from google.oauth2.service_account import Credentials
import gspread
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Tuple, List, Dict, Any
import time
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import re

from ConfReadDocs import SCOPES, FILE_KEY, CREDENTIALS_FILE, SHEETS_TO_READ, REQUIRED_COLUMNS, \
    DATA_START_ROW, DB_CONFIG
from db_set import db_insert


# =============================================================================
# KONFIGURACJA LOGOWANIA
# =============================================================================

def setup_logging():
    """
    Konfiguruje system logowania TYLKO do pliku ReadDocs.log z rotacją (max 5MB)
    """
    # Pobierz katalog w którym znajduje się skrypt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, 'ReadDocs.log')

    # Usuń wszystkie istniejące handlery
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Konfiguracja RotatingFileHandler z maksymalnym rozmiarem 5MB
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,  # Zachowaj 3 stare pliki (ReadDocs.log.1, ReadDocs.log.2, ReadDocs.log.3)
        encoding='utf-8'
    )

    # Konfiguracja loggera - TYLKO plik, bez konsoli
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[rotating_handler]
    )

    return logging.getLogger(__name__)


def log_session_start(logger):
    """
    Zapisuje nagłówek sesji w logu
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    separator = "=" * 80

    logger.info(f"\n{separator}")
    logger.info(f"NOWA SESJA READOCS - {timestamp}")
    logger.info(f"PID: {os.getpid()}")
    logger.info(separator)


def log_session_end(logger, success: bool, start_time: float):
    """
    Zapisuje podsumowanie sesji w logu
    """
    end_time = time.time()
    duration = end_time - start_time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    status = "SUKCES" if success else "BŁĄD"
    logger.info(f"\nZAKOŃCZENIE SESJI - {timestamp}")
    logger.info(f"Status: {status}")
    logger.info(f"Czas wykonania: {duration:.2f} sekund")
    logger.info("=" * 80)


# =============================================================================
# GŁÓWNA FUNKCJA ODCZYTU GOOGLE SHEETS
# =============================================================================

def ReadGdocs(file_key: str, credentials_file: str, sheets_dict: Dict[str, int],
              required_columns: Dict[int, str], data_start_row: int, logger) -> Tuple[Dict[int, pd.DataFrame], bool]:
    """
    Funkcja do szybkiego odczytu danych z arkuszy Google Sheets.
    Zoptymalizowana pod kątem minimalnego czasu wykonania.

    Args:
        file_key (str): Klucz pliku Google Sheets
        credentials_file (str): Ścieżka do pliku credentials JSON
        sheets_dict (Dict[str, int]): Słownik mapujący nazwy arkuszy na lata
        required_columns (Dict[int, str]): Słownik mapujący numery kolumn na nazwy
        data_start_row (int): Numer wiersza od którego zaczynają się dane (indeks od 0)
        logger: Logger do zapisywania komunikatów

    Returns:
        Tuple[Dict[int, pd.DataFrame], bool]: Słownik DataFrames per rok i status powodzenia operacji
    """

    start_time = time.time()
    tables_by_year = {}
    success = True

    try:
        logger.info(f"🔗 Łączenie z Google Sheets...")

        # Szybka autoryzacja
        creds = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
        client = gspread.authorize(creds)

        # Otwórz dokument raz dla wszystkich arkuszy
        spreadsheet = client.open_by_key(file_key)

        logger.info(f"📊 Odczytywanie {len(sheets_dict)} arkuszy...")

        for sheet_name, year in sheets_dict.items():
            try:
                logger.info(f"   📋 Przetwarzanie arkusza: {sheet_name} (rok {year})")

                # Pobierz arkusz
                worksheet = spreadsheet.worksheet(sheet_name)

                # Szybki odczyt wszystkich danych jednym zapytaniem
                all_values = worksheet.get_all_values()

                if len(all_values) <= data_start_row:
                    logger.info(f"   ⚠️  Arkusz '{sheet_name}' ma za mało wierszy!")
                    tables_by_year[year] = pd.DataFrame()
                    continue

                # Wyodrębnij tylko potrzebne kolumny i wiersze
                data_rows = []
                for row_idx in range(data_start_row, len(all_values)):
                    row = all_values[row_idx]
                    # Pobierz tylko wymagane kolumny
                    filtered_row = []
                    for col_idx in sorted(required_columns.keys()):
                        if col_idx < len(row):
                            filtered_row.append(row[col_idx])
                        else:
                            filtered_row.append('')  # Pusta wartość jeśli kolumna nie istnieje
                    data_rows.append(filtered_row)

                # Utwórz DataFrame z odpowiednimi nagłówkami
                column_names = [required_columns[i] for i in sorted(required_columns.keys())]
                df = pd.DataFrame(data_rows, columns=column_names)

                # Usuń całkowicie puste wiersze
                df = df.dropna(how='all')

                # Usuń wiersze gdzie 'Nr zlecenia' jest pusty (kluczowa kolumna)
                df = df[df['Nr zlecenia'].str.strip() != '']

                tables_by_year[year] = df
                logger.info(f"   ✅ Arkusz '{sheet_name}': {len(df)} wierszy odczytanych")

            except gspread.exceptions.WorksheetNotFound:
                logger.info(f"   ❌ Nie znaleziono arkusza: {sheet_name}")
                tables_by_year[year] = pd.DataFrame()
                success = False

            except Exception as e:
                logger.info(f"   ❌ Błąd odczytu arkusza '{sheet_name}': {str(e)}")
                tables_by_year[year] = pd.DataFrame()
                success = False

        elapsed_time = time.time() - start_time
        logger.info(f"⏱️  Całkowity czas odczytu: {elapsed_time:.2f} sekund")

        return tables_by_year, success

    except FileNotFoundError:
        logger.info(f"❌ Nie znaleziono pliku credentials: {credentials_file}")
        return {}, False

    except Exception as e:
        logger.info(f"❌ Błąd krytyczny: {str(e)}")
        return {}, False


# =============================================================================
# FUNKCJE BAZY DANYCH
# =============================================================================

def get_orders_from_db(year: int, db_config: Dict[str, Any], logger) -> pd.DataFrame:
    """
    Pobiera zamówienia z bazy danych PostgreSQL dla określonego roku.

    Args:
        year (int): Rok do filtrowania
        db_config (Dict[str, Any]): Konfiguracja połączenia z bazą danych
        logger: Logger do zapisywania komunikatów

    Returns:
        pd.DataFrame: DataFrame z danymi z bazy danych
    """

    try:
        # Połączenie z bazą danych
        conn = psycopg2.connect(**db_config)

        # SQL Query
        query = """
        SELECT id, rokk, rok, nazwa, klient, targi, stoisko, opis, mcs, rks, pm, pow_stoisko, pow_pietra 
        FROM public."ORDERS_nrsde" 
        WHERE rokk = %s;
        """

        # Wykonaj zapytanie i zwróć DataFrame
        df = pd.read_sql_query(query, conn, params=[year])

        conn.close()
        return df

    except Exception as e:
        logger.info(f"❌ Błąd odczytu z bazy danych dla roku {year}: {str(e)}")
        return pd.DataFrame()


def extract_stoisko_from_nazwa(nazwa_stoiska: str) -> str:
    """
    Wyodrębnia część pomiędzy znakami '/' z 'Nazwa STOISKA'.

    Args:
        nazwa_stoiska (str): Pełna nazwa stoiska

    Returns:
        str: Część pomiędzy znakami '/' lub pusta jeśli nie znaleziono
    """
    if not nazwa_stoiska or not isinstance(nazwa_stoiska, str):
        return ''

    # Szukaj wzorca pomiędzy znakami '/'
    match = re.search(r'/([^/]+)/', nazwa_stoiska)
    if match:
        return match.group(1).strip()

    # Jeśli nie ma wzorca z '/', spróbuj znaleźć pojedynczy znak '/'
    parts = nazwa_stoiska.split('/')
    if len(parts) >= 2:
        # Zwróć część po pierwszym '/' lub przed ostatnim '/'
        return parts[1].strip() if len(parts) == 2 else parts[-2].strip()

    return ''


def prepare_new_record_for_db(google_row: pd.Series, year: int) -> Dict[str, Any]:
    """
    Przygotowuje nowy rekord z Google Sheets do zapisu w bazie danych zgodnie z mapowaniem.

    Args:
        google_row (pd.Series): Wiersz danych z Google Sheets
        year (int): Rok dla którego przygotowywany jest rekord

    Returns:
        Dict[str, Any]: Słownik z danymi gotowymi do wstawienia do bazy
    """

    # Dokładne mapowanie zgodnie z wymaganiami
    new_record = {
        # Rok - z parametru
        'rokk': year,
        'rok': str(year),

        # Mapowanie kolumn Google Sheets -> PostgreSQL
        'nazwa': google_row.get('Nr zlecenia', '').strip(),
        'klient': google_row.get('Nazwa Klienta/Agencja', '').strip(),
        'targi': google_row.get('Nazwa Targów', '').strip(),
        'opis': google_row.get('Nazwa STOISKA', '').strip(),  # Pełna nazwa stoiska do opis
        'stoisko': extract_stoisko_from_nazwa(google_row.get('Nazwa STOISKA', '')),  # Część pomiędzy '/'
        'pm': google_row.get('Project Manager', '').strip(),
        'pow_stoisko': google_row.get('Powierzchnia stoiska', '').strip(),
        'pow_pietra': google_row.get('Powierzchnia piętra', '').strip(),

        # Pozostałe pola - wartości domyślne
        'mcs': None,
        'rks': None
    }

    # Konwersja powierzchni na liczby (jeśli możliwe)
    try:
        if new_record['pow_stoisko']:
            # Zamień przecinek na kropkę i usuń białe znaki
            pow_stoisko_clean = str(new_record['pow_stoisko']).replace(',', '.').strip()
            if pow_stoisko_clean:
                new_record['pow_stoisko'] = float(pow_stoisko_clean)
            else:
                new_record['pow_stoisko'] = None
        else:
            new_record['pow_stoisko'] = None

        if new_record['pow_pietra']:
            # Zamień przecinek na kropkę i usuń białe znaki
            pow_pietra_clean = str(new_record['pow_pietra']).replace(',', '.').strip()
            if pow_pietra_clean:
                new_record['pow_pietra'] = float(pow_pietra_clean)
            else:
                new_record['pow_pietra'] = None
        else:
            new_record['pow_pietra'] = None

    except (ValueError, AttributeError):
        # Jeśli konwersja się nie uda, zostaw jako None
        new_record['pow_stoisko'] = None
        new_record['pow_pietra'] = None

    return new_record


# Usuń zbędne funkcje diagnostyczne
def get_table_structure(db_config: Dict[str, Any], logger) -> Dict[str, str]:
    """
    FUNKCJA USUNIĘTA - nie jest już potrzebna przy użyciu ORM
    """
    pass


def insert_new_records_to_db(new_records: List[Dict[str, Any]], db_config: Dict[str, Any], logger) -> bool:
    """
    Wstawia nowe rekordy do bazy danych używając funkcji db_insert z db_set.py.

    Args:
        new_records (List[Dict[str, Any]]): Lista nowych rekordów do wstawienia
        db_config (Dict[str, Any]): Konfiguracja połączenia z bazą danych (nie używana)
        logger: Logger do zapisywania komunikatów

    Returns:
        bool: True jeśli operacja się powiodła, False w przeciwnym razie
    """

    if not new_records:
        logger.info("📝 Brak nowych rekordów do wstawienia")
        return True

    logger.info(f"💾 Przygotowanie do wstawienia {len(new_records)} nowych rekordów...")

    inserted_count = 0
    for record in new_records:
        try:
            # Konwersja typów dla db_insert
            rokk = int(record.get('rokk', 2025))
            rok = int(record.get('rok', 2025))
            nazwa = str(record.get('nazwa', ''))
            klient = str(record.get('klient', ''))
            targi = str(record.get('targi', ''))
            stoisko = str(record.get('stoisko', ''))
            opis = str(record.get('opis', ''))
            pm = str(record.get('pm', ''))

            # Konwersja powierzchni na int
            pow_stoisko = record.get('pow_stoisko', 0)
            if pow_stoisko:
                pow_stoisko = int(float(str(pow_stoisko).replace(',', '.')))
            else:
                pow_stoisko = 0

            pow_pietra = record.get('pow_pietra', 0)
            if pow_pietra:
                pow_pietra = int(float(str(pow_pietra).replace(',', '.')))
            else:
                pow_pietra = 0

            # WYWOŁANIE FUNKCJI Z BIBLIOTEKI db_set.py
            db_insert(rokk, rok, nazwa, klient, targi, stoisko, opis, pm, pow_stoisko, pow_pietra)

            inserted_count += 1
            logger.info(f"   ✅ Wstawiono rekord: {nazwa} | Stoisko: {stoisko} | Klient: {klient}")

        except Exception as e:
            logger.info(f"   ❌ Błąd wstawienia rekordu {record.get('nazwa', 'UNKNOWN')}: {str(e)}")
            continue

    logger.info(f"💾 Pomyślnie wstawiono {inserted_count} z {len(new_records)} rekordów")
    return inserted_count > 0


def compare_tables(google_df: pd.DataFrame, db_df: pd.DataFrame, year: int, logger) -> List[Dict[str, Any]]:
    """
    Porównuje tabele z Google Sheets i bazy danych pod względem kolumny 'Nr zlecenia' vs 'nazwa'.
    Zwraca listę nowych rekordów gotowych do wstawienia do bazy.

    Args:
        google_df (pd.DataFrame): DataFrame z Google Sheets
        db_df (pd.DataFrame): DataFrame z bazy danych
        year (int): Rok dla którego wykonywane jest porównanie
        logger: Logger do zapisywania komunikatów

    Returns:
        List[Dict[str, Any]]: Lista nowych rekordów do wstawienia do bazy
    """

    new_records_for_db = []

    if google_df.empty and db_df.empty:
        logger.info(f"✅ ROK {year}: Tabele są równe - obie puste")
        return new_records_for_db

    if google_df.empty:
        logger.info(f"⚠️  ROK {year}: Google Sheets pusty, baza danych ma {len(db_df)} rekordów")
        return new_records_for_db

    if db_df.empty:
        logger.info(f"⚠️  ROK {year}: Baza danych pusta, Google Sheets ma {len(google_df)} rekordów")
        # Przygotuj wszystkie wiersze z Google Sheets do wstawienia
        for _, row in google_df.iterrows():
            row_dict = row.to_dict()
            logger.info(f"   NOWY: {row_dict}")

            # Przygotuj rekord do wstawienia do bazy
            db_record = prepare_new_record_for_db(row, year)
            new_records_for_db.append(db_record)

        return new_records_for_db

    # Pobierz wartości z kolumn porównania (czyść białe znaki)
    google_orders = set(google_df['Nr zlecenia'].astype(str).str.strip())
    db_orders = set(db_df['nazwa'].astype(str).str.strip())

    # Usuń puste wartości
    google_orders.discard('')
    db_orders.discard('')

    # Znajdź różnice
    new_in_google = google_orders - db_orders

    if not new_in_google:
        logger.info(f"✅ ROK {year}: Tabele są równe - {len(google_orders)} identycznych rekordów")
    else:
        logger.info(f"📈 ROK {year}: Znaleziono {len(new_in_google)} nowych rekordów w Google Sheets:")

        # Wyświetl pełne wiersze dla nowych rekordów i przygotuj do wstawienia
        for order_nr in new_in_google:
            matching_rows = google_df[google_df['Nr zlecenia'].astype(str).str.strip() == order_nr]
            for _, row in matching_rows.iterrows():
                row_dict = row.to_dict()
                logger.info(f"   NOWY: {row_dict}")

                # Przygotuj rekord do wstawienia do bazy
                db_record = prepare_new_record_for_db(row, year)
                new_records_for_db.append(db_record)

    return new_records_for_db


# =============================================================================
# GŁÓWNA FUNKCJA PROGRAMU
# =============================================================================

def main():
    """
    Główna funkcja programu
    """
    # Zapisz czas rozpoczęcia sesji
    session_start_time = time.time()

    # Skonfiguruj logowanie
    logger = setup_logging()

    # Zaloguj rozpoczęcie sesji
    log_session_start(logger)

    logger.info("🚀 PORÓWNANIE DANYCH GOOGLE SHEETS Z BAZĄ POSTGRESQL")
    logger.info("=" * 65)

    # Wywołaj główną funkcję odczytu Google Sheets
    google_tables, google_success = ReadGdocs(
        file_key=FILE_KEY,
        credentials_file=CREDENTIALS_FILE,
        sheets_dict=SHEETS_TO_READ,
        required_columns=REQUIRED_COLUMNS,
        data_start_row=DATA_START_ROW,
        logger=logger
    )

    if not google_success:
        logger.info("❌ Błąd odczytu Google Sheets - przerywanie")
        log_session_end(logger, False, session_start_time)
        return False

    logger.info("\n🗃️  Pobieranie danych z bazy PostgreSQL i porównanie...")

    all_new_records = []

    # Dla każdego roku pobierz dane z bazy i porównaj
    for year in SHEETS_TO_READ.values():
        db_df = get_orders_from_db(year, DB_CONFIG, logger)
        google_df = google_tables.get(year, pd.DataFrame())

        # Porównaj tabele i zbierz nowe rekordy
        new_records = compare_tables(google_df, db_df, year, logger)
        all_new_records.extend(new_records)

    # Wstaw nowe rekordy do bazy danych - NOWA METODA
    if all_new_records:
        logger.info(f"\n💾 Rozpoczęcie wstawiania {len(all_new_records)} nowych rekordów do bazy...")
        insert_success = insert_new_records_to_db(all_new_records, DB_CONFIG, logger)

    logger.info(f"\n📊 PODSUMOWANIE: Znaleziono {len(all_new_records)} nowych rekordów gotowych do wstawienia")

    # Zaloguj zakończenie sesji
    log_session_end(logger, True, session_start_time)
    return True


# =============================================================================
# URUCHOMIENIE SKRYPTU
# =============================================================================

if __name__ == "__main__":
    success = main()

    if success:
        exit(0)
    else:
        exit(1)







































# #!/opt/PROJEKTY/SDA/env/bin/python3
#
# """
# ReadDocs.py - Szybki odczyt danych z Google Sheets z porównaniem z bazą PostgreSQL
# Optymalizowany pod kątem minimalnego czasu odczytu dla zachowania integralności danych
# """
#
# import pandas as pd
# from google.oauth2.service_account import Credentials
# import gspread
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from typing import Tuple, List, Dict, Any
# import time
# import os
# import logging
# from logging.handlers import RotatingFileHandler
# from datetime import datetime
# import re
#
# from ConfReadDocs import SCOPES, FILE_KEY, CREDENTIALS_FILE, SHEETS_TO_READ, REQUIRED_COLUMNS, \
#     DATA_START_ROW, DB_CONFIG
# from db_set import db_insert
#
#
# # =============================================================================
# # KONFIGURACJA LOGOWANIA
# # =============================================================================
#
# def setup_logging():
#     """
#     Konfiguruje system logowania TYLKO do pliku ReadDocs.log z rotacją (max 5MB)
#     """
#     # Pobierz katalog w którym znajduje się skrypt
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     log_file = os.path.join(script_dir, 'ReadDocs.log')
#
#     # Usuń wszystkie istniejące handlery
#     for handler in logging.root.handlers[:]:
#         logging.root.removeHandler(handler)
#
#     # Konfiguracja RotatingFileHandler z maksymalnym rozmiarem 5MB
#     rotating_handler = RotatingFileHandler(
#         log_file,
#         maxBytes=5 * 1024 * 1024,  # 5MB
#         backupCount=3,  # Zachowaj 3 stare pliki (ReadDocs.log.1, ReadDocs.log.2, ReadDocs.log.3)
#         encoding='utf-8'
#     )
#
#     # Konfiguracja loggera - TYLKO plik, bez konsoli
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(message)s',
#         handlers=[rotating_handler]
#     )
#
#     return logging.getLogger(__name__)
#
#
# def log_session_start(logger):
#     """
#     Zapisuje nagłówek sesji w logu
#     """
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     separator = "=" * 80
#
#     logger.info(f"\n{separator}")
#     logger.info(f"NOWA SESJA READOCS - {timestamp}")
#     logger.info(f"PID: {os.getpid()}")
#     logger.info(separator)
#
#
# def log_session_end(logger, success: bool, start_time: float):
#     """
#     Zapisuje podsumowanie sesji w logu
#     """
#     end_time = time.time()
#     duration = end_time - start_time
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     status = "SUKCES" if success else "BŁĄD"
#     logger.info(f"\nZAKOŃCZENIE SESJI - {timestamp}")
#     logger.info(f"Status: {status}")
#     logger.info(f"Czas wykonania: {duration:.2f} sekund")
#     logger.info("=" * 80)
#
#
# # =============================================================================
# # GŁÓWNA FUNKCJA ODCZYTU GOOGLE SHEETS
# # =============================================================================
#
# def ReadGdocs(file_key: str, credentials_file: str, sheets_dict: Dict[str, int],
#               required_columns: Dict[int, str], data_start_row: int, logger) -> Tuple[Dict[int, pd.DataFrame], bool]:
#     """
#     Funkcja do szybkiego odczytu danych z arkuszy Google Sheets.
#     Zoptymalizowana pod kątem minimalnego czasu wykonania.
#
#     Args:
#         file_key (str): Klucz pliku Google Sheets
#         credentials_file (str): Ścieżka do pliku credentials JSON
#         sheets_dict (Dict[str, int]): Słownik mapujący nazwy arkuszy na lata
#         required_columns (Dict[int, str]): Słownik mapujący numery kolumn na nazwy
#         data_start_row (int): Numer wiersza od którego zaczynają się dane (indeks od 0)
#         logger: Logger do zapisywania komunikatów
#
#     Returns:
#         Tuple[Dict[int, pd.DataFrame], bool]: Słownik DataFrames per rok i status powodzenia operacji
#     """
#
#     start_time = time.time()
#     tables_by_year = {}
#     success = True
#
#     try:
#         logger.info(f"🔗 Łączenie z Google Sheets...")
#
#         # Szybka autoryzacja
#         creds = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
#         client = gspread.authorize(creds)
#
#         # Otwórz dokument raz dla wszystkich arkuszy
#         spreadsheet = client.open_by_key(file_key)
#
#         logger.info(f"📊 Odczytywanie {len(sheets_dict)} arkuszy...")
#
#         for sheet_name, year in sheets_dict.items():
#             try:
#                 logger.info(f"   📋 Przetwarzanie arkusza: {sheet_name} (rok {year})")
#
#                 # Pobierz arkusz
#                 worksheet = spreadsheet.worksheet(sheet_name)
#
#                 # Szybki odczyt wszystkich danych jednym zapytaniem
#                 all_values = worksheet.get_all_values()
#
#                 if len(all_values) <= data_start_row:
#                     logger.info(f"   ⚠️  Arkusz '{sheet_name}' ma za mało wierszy!")
#                     tables_by_year[year] = pd.DataFrame()
#                     continue
#
#                 # Wyodrębnij tylko potrzebne kolumny i wiersze
#                 data_rows = []
#                 for row_idx in range(data_start_row, len(all_values)):
#                     row = all_values[row_idx]
#                     # Pobierz tylko wymagane kolumny
#                     filtered_row = []
#                     for col_idx in sorted(required_columns.keys()):
#                         if col_idx < len(row):
#                             filtered_row.append(row[col_idx])
#                         else:
#                             filtered_row.append('')  # Pusta wartość jeśli kolumna nie istnieje
#                     data_rows.append(filtered_row)
#
#                 # Utwórz DataFrame z odpowiednimi nagłówkami
#                 column_names = [required_columns[i] for i in sorted(required_columns.keys())]
#                 df = pd.DataFrame(data_rows, columns=column_names)
#
#                 # Usuń całkowicie puste wiersze
#                 df = df.dropna(how='all')
#
#                 # Usuń wiersze gdzie 'Nr zlecenia' jest pusty (kluczowa kolumna)
#                 df = df[df['Nr zlecenia'].str.strip() != '']
#
#                 tables_by_year[year] = df
#                 logger.info(f"   ✅ Arkusz '{sheet_name}': {len(df)} wierszy odczytanych")
#
#             except gspread.exceptions.WorksheetNotFound:
#                 logger.info(f"   ❌ Nie znaleziono arkusza: {sheet_name}")
#                 tables_by_year[year] = pd.DataFrame()
#                 success = False
#
#             except Exception as e:
#                 logger.info(f"   ❌ Błąd odczytu arkusza '{sheet_name}': {str(e)}")
#                 tables_by_year[year] = pd.DataFrame()
#                 success = False
#
#         elapsed_time = time.time() - start_time
#         logger.info(f"⏱️  Całkowity czas odczytu: {elapsed_time:.2f} sekund")
#
#         return tables_by_year, success
#
#     except FileNotFoundError:
#         logger.info(f"❌ Nie znaleziono pliku credentials: {credentials_file}")
#         return {}, False
#
#     except Exception as e:
#         logger.info(f"❌ Błąd krytyczny: {str(e)}")
#         return {}, False
#
#
# # =============================================================================
# # FUNKCJE BAZY DANYCH
# # =============================================================================
#
# def get_orders_from_db(year: int, db_config: Dict[str, Any], logger) -> pd.DataFrame:
#     """
#     Pobiera zamówienia z bazy danych PostgreSQL dla określonego roku.
#
#     Args:
#         year (int): Rok do filtrowania
#         db_config (Dict[str, Any]): Konfiguracja połączenia z bazą danych
#         logger: Logger do zapisywania komunikatów
#
#     Returns:
#         pd.DataFrame: DataFrame z danymi z bazy danych
#     """
#
#     try:
#         # Połączenie z bazą danych
#         conn = psycopg2.connect(**db_config)
#
#         # SQL Query
#         query = """
#         SELECT id, rokk, rok, nazwa, klient, targi, stoisko, opis, mcs, rks, pm, pow_stoisko, pow_pietra
#         FROM public."ORDERS_nrsde"
#         WHERE rokk = %s;
#         """
#
#         # Wykonaj zapytanie i zwróć DataFrame
#         df = pd.read_sql_query(query, conn, params=[year])
#
#         conn.close()
#         return df
#
#     except Exception as e:
#         logger.info(f"❌ Błąd odczytu z bazy danych dla roku {year}: {str(e)}")
#         return pd.DataFrame()
#
#
# def extract_stoisko_from_nazwa(nazwa_stoiska: str) -> str:
#     """
#     Wyodrębnia część pomiędzy znakami '/' z 'Nazwa STOISKA'.
#
#     Args:
#         nazwa_stoiska (str): Pełna nazwa stoiska
#
#     Returns:
#         str: Część pomiędzy znakami '/' lub pusta jeśli nie znaleziono
#     """
#     if not nazwa_stoiska or not isinstance(nazwa_stoiska, str):
#         return ''
#
#     # Szukaj wzorca pomiędzy znakami '/'
#     match = re.search(r'/([^/]+)/', nazwa_stoiska)
#     if match:
#         return match.group(1).strip()
#
#     # Jeśli nie ma wzorca z '/', spróbuj znaleźć pojedynczy znak '/'
#     parts = nazwa_stoiska.split('/')
#     if len(parts) >= 2:
#         # Zwróć część po pierwszym '/' lub przed ostatnim '/'
#         return parts[1].strip() if len(parts) == 2 else parts[-2].strip()
#
#     return ''
#
#
# def prepare_new_record_for_db(google_row: pd.Series, year: int) -> Dict[str, Any]:
#     """
#     Przygotowuje nowy rekord z Google Sheets do zapisu w bazie danych zgodnie z mapowaniem.
#
#     Args:
#         google_row (pd.Series): Wiersz danych z Google Sheets
#         year (int): Rok dla którego przygotowywany jest rekord
#
#     Returns:
#         Dict[str, Any]: Słownik z danymi gotowymi do wstawienia do bazy
#     """
#
#     # Dokładne mapowanie zgodnie z wymaganiami
#     new_record = {
#         # Rok - z parametru
#         'rokk': year,
#         'rok': str(year),
#
#         # Mapowanie kolumn Google Sheets -> PostgreSQL
#         'nazwa': google_row.get('Nr zlecenia', '').strip(),
#         'klient': google_row.get('Nazwa Klienta/Agencja', '').strip(),
#         'targi': google_row.get('Nazwa Targów', '').strip(),
#         'opis': google_row.get('Nazwa STOISKA', '').strip(),  # Pełna nazwa stoiska do opis
#         'stoisko': extract_stoisko_from_nazwa(google_row.get('Nazwa STOISKA', '')),  # Część pomiędzy '/'
#         'pm': google_row.get('Project Manager', '').strip(),
#         'pow_stoisko': google_row.get('Powierzchnia stoiska', '').strip(),
#         'pow_pietra': google_row.get('Powierzchnia piętra', '').strip(),
#
#         # Pozostałe pola - wartości domyślne
#         'mcs': None,
#         'rks': None
#     }
#
#     # Konwersja powierzchni na liczby (jeśli możliwe)
#     try:
#         if new_record['pow_stoisko']:
#             # Zamień przecinek na kropkę i usuń białe znaki
#             pow_stoisko_clean = str(new_record['pow_stoisko']).replace(',', '.').strip()
#             if pow_stoisko_clean:
#                 new_record['pow_stoisko'] = float(pow_stoisko_clean)
#             else:
#                 new_record['pow_stoisko'] = None
#         else:
#             new_record['pow_stoisko'] = None
#
#         if new_record['pow_pietra']:
#             # Zamień przecinek na kropkę i usuń białe znaki
#             pow_pietra_clean = str(new_record['pow_pietra']).replace(',', '.').strip()
#             if pow_pietra_clean:
#                 new_record['pow_pietra'] = float(pow_pietra_clean)
#             else:
#                 new_record['pow_pietra'] = None
#         else:
#             new_record['pow_pietra'] = None
#
#     except (ValueError, AttributeError):
#         # Jeśli konwersja się nie uda, zostaw jako None
#         new_record['pow_stoisko'] = None
#         new_record['pow_pietra'] = None
#
#     return new_record
#
#
# # Usuń zbędne funkcje diagnostyczne
# def get_table_structure(db_config: Dict[str, Any], logger) -> Dict[str, str]:
#     """
#     FUNKCJA USUNIĘTA - nie jest już potrzebna przy użyciu ORM
#     """
#     pass
#
#
# def insert_new_records_to_db(new_records: List[Dict[str, Any]], db_config: Dict[str, Any], logger) -> bool:
#     """
#     Wstawia nowe rekordy do bazy danych używając funkcji db_insert z db_set.py.
#
#     Args:
#         new_records (List[Dict[str, Any]]): Lista nowych rekordów do wstawienia
#         db_config (Dict[str, Any]): Konfiguracja połączenia z bazą danych (nie używana)
#         logger: Logger do zapisywania komunikatów
#
#     Returns:
#         bool: True jeśli operacja się powiodła, False w przeciwnym razie
#     """
#
#     if not new_records:
#         logger.info("📝 Brak nowych rekordów do wstawienia")
#         return True
#
#     logger.info(f"💾 Przygotowanie do wstawienia {len(new_records)} nowych rekordów...")
#
#     inserted_count = 0
#     for record in new_records:
#         print(">>> ", record)
#         try:
#             # Konwersja typów dla db_insert
#             rokk = int(record.get('rokk', 2025))
#             rok = int(record.get('rok', 2025))
#             nazwa = str(record.get('nazwa', ''))
#             klient = str(record.get('klient', ''))
#             targi = str(record.get('targi', ''))
#             stoisko = str(record.get('stoisko', ''))
#             opis = str(record.get('opis', ''))
#             pm = str(record.get('pm', ''))
#
#             # Konwersja powierzchni na int
#             pow_stoisko = record.get('pow_stoisko', 0)
#             if pow_stoisko:
#                 pow_stoisko = int(float(str(pow_stoisko).replace(',', '.')))
#             else:
#                 pow_stoisko = 0
#
#             pow_pietra = record.get('pow_pietra', 0)
#             if pow_pietra:
#                 pow_pietra = int(float(str(pow_pietra).replace(',', '.')))
#             else:
#                 pow_pietra = 0
#
#             # WYWOŁANIE FUNKCJI Z BIBLIOTEKI db_set.py
#             #db_insert(rokk, rok, nazwa, klient, targi, stoisko, opis, pm, pow_stoisko, pow_pietra)
#
#             inserted_count += 1
#             logger.info(f"   ✅ Wstawiono rekord: {nazwa} | Stoisko: {stoisko} | Klient: {klient}")
#
#         except Exception as e:
#             logger.info(f"   ❌ Błąd wstawienia rekordu {record.get('nazwa', 'UNKNOWN')}: {str(e)}")
#             continue
#
#     logger.info(f"💾 Pomyślnie wstawiono {inserted_count} z {len(new_records)} rekordów")
#     return inserted_count > 0
#
#
# def compare_tables(google_df: pd.DataFrame, db_df: pd.DataFrame, year: int, logger) -> List[Dict[str, Any]]:
#     """
#     Porównuje tabele z Google Sheets i bazy danych pod względem kolumny 'Nr zlecenia' vs 'nazwa'.
#     Zwraca listę nowych rekordów gotowych do wstawienia do bazy.
#
#     Args:
#         google_df (pd.DataFrame): DataFrame z Google Sheets
#         db_df (pd.DataFrame): DataFrame z bazy danych
#         year (int): Rok dla którego wykonywane jest porównanie
#         logger: Logger do zapisywania komunikatów
#
#     Returns:
#         List[Dict[str, Any]]: Lista nowych rekordów do wstawienia do bazy
#     """
#
#     new_records_for_db = []
#
#     if google_df.empty and db_df.empty:
#         logger.info(f"✅ ROK {year}: Tabele są równe - obie puste")
#         return new_records_for_db
#
#     if google_df.empty:
#         logger.info(f"⚠️  ROK {year}: Google Sheets pusty, baza danych ma {len(db_df)} rekordów")
#         return new_records_for_db
#
#     if db_df.empty:
#         logger.info(f"⚠️  ROK {year}: Baza danych pusta, Google Sheets ma {len(google_df)} rekordów")
#         # Przygotuj wszystkie wiersze z Google Sheets do wstawienia
#         for _, row in google_df.iterrows():
#             row_dict = row.to_dict()
#             logger.info(f"   NOWY: {row_dict}")
#
#             # Przygotuj rekord do wstawienia do bazy
#             db_record = prepare_new_record_for_db(row, year)
#             new_records_for_db.append(db_record)
#
#         return new_records_for_db
#
#     # Pobierz wartości z kolumn porównania (czyść białe znaki)
#     google_orders = set(google_df['Nr zlecenia'].astype(str).str.strip())
#     db_orders = set(db_df['nazwa'].astype(str).str.strip())
#
#     # Usuń puste wartości
#     google_orders.discard('')
#     db_orders.discard('')
#
#     # Znajdź różnice
#     new_in_google = google_orders - db_orders
#
#     if not new_in_google:
#         logger.info(f"✅ ROK {year}: Tabele są równe - {len(google_orders)} identycznych rekordów")
#     else:
#         logger.info(f"📈 ROK {year}: Znaleziono {len(new_in_google)} nowych rekordów w Google Sheets:")
#
#         # Wyświetl pełne wiersze dla nowych rekordów i przygotuj do wstawienia
#         for order_nr in new_in_google:
#             matching_rows = google_df[google_df['Nr zlecenia'].astype(str).str.strip() == order_nr]
#             for _, row in matching_rows.iterrows():
#                 row_dict = row.to_dict()
#                 logger.info(f"   NOWY: {row_dict}")
#
#                 # Przygotuj rekord do wstawienia do bazy
#                 db_record = prepare_new_record_for_db(row, year)
#                 new_records_for_db.append(db_record)
#
#     return new_records_for_db
#
#
# # =============================================================================
# # GŁÓWNA FUNKCJA PROGRAMU
# # =============================================================================
#
# def main():
#     """
#     Główna funkcja programu
#     """
#     # Zapisz czas rozpoczęcia sesji
#     session_start_time = time.time()
#
#     # Skonfiguruj logowanie
#     logger = setup_logging()
#
#     # Zaloguj rozpoczęcie sesji
#     log_session_start(logger)
#
#     logger.info("🚀 PORÓWNANIE DANYCH GOOGLE SHEETS Z BAZĄ POSTGRESQL")
#     logger.info("=" * 65)
#
#     # Wywołaj główną funkcję odczytu Google Sheets
#     google_tables, google_success = ReadGdocs(
#         file_key=FILE_KEY,
#         credentials_file=CREDENTIALS_FILE,
#         sheets_dict=SHEETS_TO_READ,
#         required_columns=REQUIRED_COLUMNS,
#         data_start_row=DATA_START_ROW,
#         logger=logger
#     )
#
#     if not google_success:
#         logger.info("❌ Błąd odczytu Google Sheets - przerywanie")
#         log_session_end(logger, False, session_start_time)
#         return False
#
#     logger.info("\n🗃️  Pobieranie danych z bazy PostgreSQL i porównanie...")
#
#     all_new_records = []
#
#     # Dla każdego roku pobierz dane z bazy i porównaj
#     for year in SHEETS_TO_READ.values():
#         db_df = get_orders_from_db(year, DB_CONFIG, logger)
#         google_df = google_tables.get(year, pd.DataFrame())
#
#         # Porównaj tabele i zbierz nowe rekordy
#         new_records = compare_tables(google_df, db_df, year, logger)
#         all_new_records.extend(new_records)
#
#     # Wstaw nowe rekordy do bazy danych - NOWA METODA
#     if all_new_records:
#         logger.info(f"\n💾 Rozpoczęcie wstawiania {len(all_new_records)} nowych rekordów do bazy...")
#         insert_success = insert_new_records_to_db(all_new_records, DB_CONFIG, logger)
#
#     logger.info(f"\n📊 PODSUMOWANIE: Znaleziono {len(all_new_records)} nowych rekordów gotowych do wstawienia")
#
#     # Zaloguj zakończenie sesji
#     log_session_end(logger, True, session_start_time)
#     return True
#
#
# # =============================================================================
# # URUCHOMIENIE SKRYPTU
# # =============================================================================
#
# if __name__ == "__main__":
#     success = main()
#
#     if success:
#         exit(0)
#     else:
#         exit(1)
