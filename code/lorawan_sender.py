"""
LoRaWAN Sender (Part 1B)

Joins the TTN LoRaWAN network using OTAA and transmits temperature
readings from the Pysense SI7006A20 sensor.

Upload this file as main.py to the LoPy4 device.
The lib/ folder (from pysense.zip) must also be on the device.

IMPORTANT: Replace YOUR_APP_KEY_HERE with the AppKey from TTN.
"""

import time
from pycoproc_1 import Pycoproc
import machine
from network import LoRa
import socket
import ubinascii
from SI7006A20 import SI7006A20

py = Pycoproc(Pycoproc.PYSENSE)
si = SI7006A20(py)

def get_temp():
    """Read temperature from the SI7006A20 sensor."""
    temperature = si.temperature()
    print("Temperature: " + str(temperature) + " C")
    return temperature

# Initialize LoRa in LORAWAN mode
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923)

# OTAA authentication credentials from TTN
app_eui = ubinascii.unhexlify("0000000000000000")
app_key = ubinascii.unhexlify("YOUR_APP_KEY_HERE")  # Replace with your AppKey

# Join the network (OTAA)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# Wait for the join to complete
while not lora.has_joined():
    time.sleep(2.5)
    print("Not yet joined...")

print("Joined the network!")

# Create a LoRa socket and configure it
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)  # Set data rate
s.setblocking(True)  # Wait for TX to complete before returning

# Send 100 temperature readings
i = 0
while i < 100:
    temp = get_temp()
    packet = "Temperature: {}".format(temp)
    s.send(packet)
    print("Sending {}".format(packet))
    i += 1
    time.sleep(5)
