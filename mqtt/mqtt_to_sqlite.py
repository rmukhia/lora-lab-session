import paho.mqtt.client as mqtt
import json
import base64
import sqlite3
import time
import re
from datetime import datetime

# Database configuration
DB_FILE = "sensor_data.db"

# MQTT configuration
BROKER = "ttn.hazemon.in.th"
PORT = 1883
USERNAME = "test-app"  # Replace with your TTN application name
PASSWORD = "NNSXS.FTPUVIQ5KVHLPKER7FLIU7DBWXVAFX5O"   # Replace with your TTN API key
APP_NAME = USERNAME
DEVICE_ID = "lopy-120049"  # Replace with your device ID

def extract_temperature(payload):
    """Extract temperature value from the payload string"""
    match = re.search(r"Temperature: ([\d.]+)", payload)
    if match:
        return float(match.group(1))
    return None

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback for when the client connects to the broker"""
    print(f"Connected with result code {rc}")
    # Subscribe to the topic for the device uplink messages
    client.subscribe(f"v3/{APP_NAME}/devices/{DEVICE_ID}/up")

def on_message(client, userdata, msg):
    """Callback for when a message is received from the broker"""
    try:
        # Decode the JSON payload from the message
        data = json.loads(msg.payload.decode())
        
        # Extract the base64 encoded payload
        payload_base64 = data["uplink_message"]["frm_payload"]
        
        # Decode the base64 payload to a UTF-8 string
        payload = base64.b64decode(payload_base64).decode()
        
        # Extract metadata
        rssi = data["uplink_message"]["rx_metadata"][0]["rssi"]
        snr = data["uplink_message"]["rx_metadata"][0]["snr"]
        
        # Extract temperature from payload
        temperature = extract_temperature(payload)
        
        if temperature is not None:
            # Connect to the database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            # Insert temperature reading
            cursor.execute(
                "INSERT INTO temperature_readings (device_id, temperature, rssi, snr) VALUES (?, ?, ?, ?)",
                (DEVICE_ID, temperature, rssi, snr)
            )
            
            # Commit changes and close connection
            conn.commit()
            conn.close()
            
            # Print the received message
            print(f"Stored: Device={DEVICE_ID}, Temp={temperature}°C, RSSI={rssi}, SNR={snr}")
        else:
            print(f"Could not extract temperature from payload: {payload}")
    
    except Exception as e:
        print(f"Error processing message: {e}")

# Set up MQTT client
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Set authentication
client.username_pw_set(USERNAME, PASSWORD)

# Connect to the broker
client.connect(BROKER, PORT)

# Start the loop
print(f"Starting MQTT client, listening for data from device {DEVICE_ID}...")
print("Press Ctrl+C to stop")
client.loop_forever()