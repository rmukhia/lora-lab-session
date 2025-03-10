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
    """
    Retrieves the current temperature using the si.temperature() function and prints it.

    Returns:
        float: The current temperature in Celsius.
    """
    temperature = si.temperature()
    print("Temperature: " + str(temperature) + " C")
    return temperature

# Initialize LoRa in LORA mode for the AS923 region
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923)

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the socket to non-blocking mode
s.setblocking(False)

# Initialize a counter
i = 0

# Get the unique device ID
device_id = ubinascii.hexlify(machine.unique_id()).decode()

# Loop to send temperature data 10 times
while i < 10:
    # Get the current temperature
    temp = get_temp()
    
    # Create a packet with the device ID and temperature
    packet = "{}:{}".format(device_id, temp)
    
    # Send the packet via LoRa
    s.send(packet)
    
    # Print the sent packet
    print("Sending {}".format(packet))
    
    # Increment the counter
    i += 1
    
    # Wait for 5 seconds before sending the next packet
    time.sleep(5)
