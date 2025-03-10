import paho.mqtt.client as mqtt
import json
import base64

def on_message(client, userdata, msg):
    # Decode the JSON payload from the message
    data = json.loads(msg.payload.decode())
    # Extract the base64 encoded payload
    payload_base64 = data["uplink_message"]["frm_payload"]
    
    # Decode the base64 payload to a UTF-8 string
    payload = base64.b64decode(payload_base64).decode()
    
    # Print the received message
    print(f"Received message: {payload}")
    

# MQTT client setup
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
# Set the on_message callback function
client.on_message = on_message

# MQTT broker username
USERNAME = "testapp"
# MQTT broker password
PASSWORD = "NNSXS.2MU7ZTKELP3KSVXBWU7RRBFVRCF3H2KVCA7NI"

# Set the username and password for the MQTT client
client.username_pw_set(USERNAME, PASSWORD)

# MQTT broker address
BROKER = "ttn.hazemon.in.th"
# MQTT broker port
PORT = 1883

# Connect to the MQTT broker
client.connect(BROKER, PORT)

# Application name
APP_NAME = "testapp"
# Device ID
DEVICE_ID = "lopy-120049"

# Subscribe to the topic for the device uplink messages
client.subscribe(f"v3/{APP_NAME}/devices/{DEVICE_ID}/up")

# Start the MQTT client loop to process messages
client.loop_forever()

