"""
LoRa Transmitter (Part 1A)

Reads temperature from the Pysense SI7006A20 sensor and transmits it
over raw LoRa along with the device ID. Sends 10 packets at 5-second intervals.

Upload this file as main.py to the transmitter LoPy4 device.
The lib/ folder (from pysense.zip) must also be on the device.
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

# Initialize LoRa in raw LORA mode for the AS923 frequency region
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923)

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

# Get the unique device ID
device_id = ubinascii.hexlify(machine.unique_id()).decode()

# Send 10 temperature readings
i = 0
while i < 10:
    temp = get_temp()
    packet = "{}:{}".format(device_id, temp)
    s.send(packet)
    print("Sending {}".format(packet))
    i += 1
    time.sleep(5)
