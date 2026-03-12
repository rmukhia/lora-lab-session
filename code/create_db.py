"""
Create SQLite Database (Part 2)

Creates the sensor_data.db database with a temperature_readings table.

Run this script once on your laptop before running mqtt_to_sqlite.py.
"""

import sqlite3

DB_FILE = "sensor_data.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS temperature_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    temperature REAL,
    rssi INTEGER,
    snr REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print(f"Database created successfully at {DB_FILE}")
