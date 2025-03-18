import sqlite3
import os

# Database file path
DB_FILE = "sensor_data.db"

# Check if database already exists
db_exists = os.path.exists(DB_FILE)

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS temperature_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    temperature REAL,
    rssi INTEGER,
    snr REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices (device_id)
)
""")

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Database created successfully at {DB_FILE}")