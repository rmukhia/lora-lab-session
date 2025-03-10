from network import LoRa
import socket
import time

# Initialize LoRa in LORA mode for the AS923 region
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923)

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the socket to non-blocking mode
s.setblocking(False)

# Infinite loop to continuously check for incoming messages
while True:
    # Receive data from the socket (up to 64 bytes)
    rx = s.recv(64)
    
    # If data is received, process it
    if len(rx) > 0:
        # Print the received message and LoRa statistics
        print('Received message:', rx.decode() , '| RSSI:', lora.stats().rssi, '| SNR:', lora.stats().snr)
    
    # Sleep for 1 second before checking again
    time.sleep(1)