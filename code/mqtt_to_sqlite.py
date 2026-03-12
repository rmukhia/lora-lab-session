"""
MQTT to SQLite Client (Part 2)

Enhanced MQTT client that subscribes to TTN uplink messages,
extracts temperature/RSSI/SNR data, and stores it in a SQLite database.

Run this script on your laptop (not on the LoPy device).
Requires: pip install paho-mqtt

IMPORTANT: Replace the three placeholder values below with your
TTN credentials. Run create_db.py first to create the database.
"""

import paho.mqtt.client as mqtt
import json
import base64
import sqlite3
import re

# Configuration (replace with your values)
DB_FILE = "sensor_data.db"
BROKER = "ttn.hazemon.in.th"
PORT = 1883
USERNAME = "YOUR_TTN_APP_ID"       # Your TTN Application ID
PASSWORD = "YOUR_TTN_API_KEY"      # Your TTN API key
DEVICE_ID = "YOUR_DEVICE_ID"      # Your TTN end device ID

def extract_temperature(payload):
    """Extract the numeric temperature from a 'Temperature: 25.3' string."""
    match = re.search(r"Temperature: ([\d.]+)", payload)
    if match:
        return float(match.group(1))
    return None

def on_connect(client, userdata, flags, rc, properties=None):
    """Subscribe to the device topic once connected."""
    print(f"Connected with result code {rc}")
    client.subscribe(f"v3/{USERNAME}/devices/{DEVICE_ID}/up")

def on_message(client, userdata, msg):
    """Process each incoming message and store it in the database."""
    try:
        data = json.loads(msg.payload.decode())
        
        # Decode the device payload (base64-encoded by TTN)
        payload_base64 = data["uplink_message"]["frm_payload"]
        payload = base64.b64decode(payload_base64).decode()
        
        # Extract signal quality metadata from the gateway
        rssi = data["uplink_message"]["rx_metadata"][0]["rssi"]
        snr = data["uplink_message"]["rx_metadata"][0]["snr"]
        
        temperature = extract_temperature(payload)
        
        if temperature is not None:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO temperature_readings "
                "(device_id, temperature, rssi, snr) VALUES (?, ?, ?, ?)",
                (DEVICE_ID, temperature, rssi, snr)
            )
            conn.commit()
            conn.close()
            print(f"Stored: Temp={temperature} C, RSSI={rssi}, SNR={snr}")
        else:
            print(f"Could not parse temperature from: {payload}")
    
    except Exception as e:
        print(f"Error processing message: {e}")

# Set up and start the MQTT client
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, PORT)

print(f"Listening for data from device {DEVICE_ID}...")
print("Press Ctrl+C to stop")
client.loop_forever()
