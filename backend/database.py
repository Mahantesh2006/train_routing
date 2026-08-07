import sqlite3
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DB_PATH = os.path.join(BASE_DIR, "railway.db")

# In Vercel serverless environment, filesystem is read-only except /tmp
if os.environ.get("VERCEL"):
    TMP_DB_PATH = "/tmp/railway.db"
    if not os.path.exists(TMP_DB_PATH) and os.path.exists(REPO_DB_PATH):
        try:
            shutil.copyfile(REPO_DB_PATH, TMP_DB_PATH)
        except Exception as e:
            print(f"Error copying DB to /tmp: {e}")
    DB_PATH = TMP_DB_PATH if os.path.exists(TMP_DB_PATH) else REPO_DB_PATH
else:
    DB_PATH = REPO_DB_PATH

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Stations Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stations (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        lat REAL,
        lng REAL,
        is_junction BOOLEAN NOT NULL DEFAULT 0
    )
    ''')

    # Trains Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trains (
        train_no TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        train_type TEXT NOT NULL,
        runs_mon BOOLEAN DEFAULT 1,
        runs_tue BOOLEAN DEFAULT 1,
        runs_wed BOOLEAN DEFAULT 1,
        runs_thu BOOLEAN DEFAULT 1,
        runs_fri BOOLEAN DEFAULT 1,
        runs_sat BOOLEAN DEFAULT 1,
        runs_sun BOOLEAN DEFAULT 1
    )
    ''')

    # Schedules / Stops Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_no TEXT NOT NULL,
        station_code TEXT NOT NULL,
        stop_seq INTEGER NOT NULL,
        arrival_time TEXT,
        departure_time TEXT,
        day_number INTEGER NOT NULL DEFAULT 1,
        distance_km INTEGER NOT NULL DEFAULT 0,
        platform INTEGER DEFAULT 1,
        FOREIGN KEY (train_no) REFERENCES trains (train_no),
        FOREIGN KEY (station_code) REFERENCES stations (code)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
