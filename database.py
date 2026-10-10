import sqlite3
from datetime import datetime

DB_NAME = "scams.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        village TEXT,
        message TEXT,
        scam_type TEXT,
        risk TEXT,
        score INTEGER
    )
""")    

    conn.commit()
    conn.close()

def save_incident(village, message, scam_type, risk, score):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents
        (timestamp, village, message, scam_type, risk, score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        village,
        message,
        scam_type,
        risk,
        score
    ))

    conn.commit()
    conn.close()

def get_incidents():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, village, message,
               scam_type, risk, score
        FROM incidents
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data