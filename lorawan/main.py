import time
from pycoproc_1 import Pycoproc
import machine
from network import LoRa
import socket
import ubinascii
from SI7006A20 import SI7006A20

# Initialize the Pycoproc object for the Pysense board
py = Pycoproc(Pycoproc.PYSENSE)

# Initialize the SI7006A20 sensor with the Pycoproc object
si = SI7006A20(py)

def get_temp():
    """
    Retrieves the current temperature using the si.temperature() function and prints it.

    Returns:
        float: The current temperature in Celsius.
    """
    # Get the temperature from the SI7006A20 sensor
    temperature = si.temperature()
    
    # Print the temperature
    print("Temperature: " + str(temperature) + " C")
    
    # Return the temperature
    return temperature

# Initialize LoRa in LORAWAN mode for the Asia region
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923)

# Create an OTAA authentication parameters
app_eui = ubinascii.unhexlify("0000000000000000")
app_key = ubinascii.unhexlify("8048D9E1C1D2144E49071F7C81526DEE")

# Join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# Wait until the module has joined the network
while not lora.has_joined():
    # Sleep for 2.5 seconds before checking again
    time.sleep(2.5)
    # Print a message indicating that the module has not yet joined
    print("Not yet joined...")

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# Make the socket blocking (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# Initialize a counter
i = 0

# Loop to send temperature data 100 times
while i < 100:
    # Get the current temperature
    temp = get_temp()
    
    # Create a packet with the device ID and temperature
    packet = "Temperature: {}".format(temp)
    
    # Send the packet via LoRa
    s.send(packet)
    
    # Print the sent packet
    print("Sending {}".format(packet))
    
    # Increment the counter
    i += 1
    
    # Wait for 5 seconds before sending the next packet
    time.sleep(5)