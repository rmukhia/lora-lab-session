"""
LoRa Receiver (Part 1A)

Listens for raw LoRa packets and prints each received message
along with RSSI and SNR signal quality metrics.

Upload this file as main.py to the receiver LoPy4 device.
"""

from network import LoRa
import socket
import time

# Initialize LoRa in raw LORA mode (must match transmitter settings)
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923)

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

# Listen continuously for incoming packets
while True:
    rx = s.recv(64)
    if len(rx) > 0:
        print("Received message:", rx.decode(), 
            "| RSSI:", lora.stats().rssi, "| SNR:", lora.stats().snr)
    time.sleep(1)
