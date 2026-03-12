"""
MQTT Client (Part 1B)

Subscribes to TTN MQTT uplink messages from a registered device
and prints the decoded payload.

Run this script on your laptop (not on the LoPy device).
Requires: pip install paho-mqtt

IMPORTANT: Replace the three placeholder values below with your
TTN credentials.
"""

import paho.mqtt.client as mqtt
import json
import base64

# TTN credentials (replace these with your values)
USERNAME = "YOUR_TTN_APP_ID"       # Your TTN Application ID
PASSWORD = "YOUR_TTN_API_KEY"      # The API key generated above
DEVICE_ID = "YOUR_DEVICE_ID"      # The end device ID from TTN

def on_connect(client, userdata, flags, rc, properties=None):
    """Subscribe once connected (ensures re-subscription on reconnect)."""
    print(f"Connected with result code {rc}")
    client.subscribe(f"v3/{USERNAME}/devices/{DEVICE_ID}/up")

def on_message(client, userdata, msg):
    """Called each time a message arrives from TTN."""
    data = json.loads(msg.payload.decode())
    
    # TTN encodes the device payload in base64
    payload_base64 = data["uplink_message"]["frm_payload"]
    payload = base64.b64decode(payload_base64).decode()
    
    print(f"Received message: {payload}")

# MQTT client setup
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(USERNAME, PASSWORD)

# Connect to the TTN MQTT broker
BROKER = "ttn.hazemon.in.th"
PORT = 1883
client.connect(BROKER, PORT)

# Listen forever (press Ctrl+C to stop)
client.loop_forever()
