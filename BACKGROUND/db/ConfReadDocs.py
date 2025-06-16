# =============================================================================
# KONFIGURACJA PARAMETRÓW
# =============================================================================

# Parametry Google Sheets
# FILE_KEY = '1Dhv-v94sA_-Q7MgMem6Dd8lTIe6sJJUUMhVk-7Wqy-4'
FILE_KEY = '1xfmcCO41X3ZJ24xVi4Tjl6pYbVxXs4l7chAnmLCeB1U'
CREDENTIALS_FILE = '/opt/SD/SDA/BACKGROUND/sde-sda-credentials.json'

# Lista arkuszy do odczytu z przypisanymi latami
SHEETS_TO_READ = {
    # 'SDA [Kody SDE]': 2025
    # Przykład dla wielu arkuszy:
    #'kody_sde_2024': 2024,
    'kody_sde_2025': 2025
}

# Parametry bazy danych PostgreSQL
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'sda',
    'user': 'django',
    'password': 'JAroslaw71!',
    'port': 5432
}

# Definicja kolumn do odczytu (numery kolumn - indeksowanie od 0)
REQUIRED_COLUMNS = {
    0: 'Nr zlecenia',
    1: 'Nazwa Klienta/Agencja',
    2: 'Nazwa Targów',
    3: 'Nazwa STOISKA',
    4: 'Project Manager',
    5: 'Powierzchnia stoiska',
    6: 'Powierzchnia piętra'
}

# Numer wiersza od którego zaczynają się dane (indeksowanie od 0, więc wiersz 3 = indeks 2)
DATA_START_ROW = 2

# Zakres uprawnień Google API
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]
