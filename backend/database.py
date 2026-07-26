import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "railway.db")

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
    # day_number: 1 = start day, 2 = 2nd day of journey, 3 = 3rd day, etc.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_no TEXT NOT NULL,
        station_code TEXT NOT NULL,
        stop_seq INTEGER NOT NULL,
        arrival_time TEXT, -- HH:MM or NULL for origin
        departure_time TEXT, -- HH:MM or NULL for terminal
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
