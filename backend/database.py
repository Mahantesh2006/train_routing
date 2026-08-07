import sqlite3
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DB_PATH = os.path.join(BASE_DIR, "railway.db")
TMP_DB_PATH = "/tmp/railway.db"

def is_vercel_env():
    return bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV") or "var/task" in __file__.replace("\\", "/"))

def get_target_db_path():
    if is_vercel_env():
        if not os.path.exists(TMP_DB_PATH):
            if os.path.exists(REPO_DB_PATH):
                try:
                    shutil.copyfile(REPO_DB_PATH, TMP_DB_PATH)
                except Exception as e:
                    print(f"Error copying DB to /tmp: {e}")
        return TMP_DB_PATH if os.path.exists(TMP_DB_PATH) else REPO_DB_PATH
    return REPO_DB_PATH

def get_db_connection():
    target_path = get_target_db_path()
    try:
        conn = sqlite3.connect(target_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError:
        # Fallback connection to /tmp if primary path is read-only
        if target_path != TMP_DB_PATH:
            try:
                if os.path.exists(REPO_DB_PATH) and not os.path.exists(TMP_DB_PATH):
                    shutil.copyfile(REPO_DB_PATH, TMP_DB_PATH)
                conn = sqlite3.connect(TMP_DB_PATH)
                conn.row_factory = sqlite3.Row
                return conn
            except Exception as e:
                print(f"Fallback connection error: {e}")
        raise

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
