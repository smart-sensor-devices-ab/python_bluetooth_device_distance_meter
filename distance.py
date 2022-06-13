import serial
import time

your_com_port = "COM18"  # Change this to the com port your dongle is connected to.
connecting_to_dongle = True

print("Connecting to dongle...")
# Trying to connect to dongle until connected. Make sure the port and baudrate is the same as your dongle.
# You can check in the device manager to see what port then right-click and choose properties then the Port Settings
# tab to see the other settings

while connecting_to_dongle:
    try:
        console = serial.Serial(
            port=your_com_port,
            baudrate=57600,
            parity="N",
            stopbits=1,
            bytesize=8,
            timeout=0,
        )
        if console.is_open.__bool__():
            connecting_to_dongle = False
    except:
        print("Dongle not connected. Please reconnect Dongle.")
        time.sleep(5)

print("Connected to Dongle.")

# function to convert rssi to distance in meter
def rssiToDistance(rssi):    
  n=2
  mp=-69
  return round(10 ** ((mp - (int(rssi)))/(10 * n)),2)    

#put the dongle in dual role, so we can scan for nearby device
console.write(str.encode("AT+CENTRAL"))
console.write("\r".encode())
print("Putting dongle in Central role.")
time.sleep(0.1)
# Scan for nearby devices for 3 seconds
console.write(str.encode("AT+GAPSCAN=3"))
console.write("\r".encode())
time.sleep(0.1)
print("Looking for nearby Bluetooth devices ...")
dongle_output2 = console.read(console.in_waiting)
time.sleep(3)

filtered = []
# Filter out unncecssary outputs and keep only the list of devices (also remove index)
for dev in dongle_output2.decode().splitlines():
    if len(dev)>20:
        filtered.append(dev.split(maxsplit=1)[1])
# Get unique device by device id and add distance to each raw        
seen = set()
out = []
for elem in filtered:
    prefix = elem.split(' ')[1]
    if prefix not in seen:
        seen.add(prefix)
        out.append(elem + " Distance: "+str(rssiToDistance(elem.split()[3]))+" meter") 

# sort list by closest device
out.sort(key=lambda x:int(x.split()[3]),reverse=True)
print("Scan Completed! "+ str(len(out)) +" devices found.")

# print(out)
for i in range(0, len(out)):
    print (out[i]) 

time.sleep(0.1)
console.close()
