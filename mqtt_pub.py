#This is a working prototype. DO NOT USE IT IN LIVE PROJECTS
import paho.mqtt.client as mqtt
import time
import ScanUtility
import bluetooth._bluetooth as bluez

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

#Set bluetooth device. Default 0.
dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print ("\n *** Looking for BLE Beacons ***\n")
	print ("\n *** CTRL-C to Cancel ***\n")
except:
	print ("Error accessing bluetooth")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)


ScanUtility.hci_enable_le_scan(sock)
#Scans for iBeacons
try:
	while True:
		returnedList = ScanUtility.parse_events(sock, 10)
		client.publish('raspberry/topic', payload=returnedList, qos=0, retain=False)
		for item in returnedList:
			print(item)
			print("")
except KeyboardInterrupt:
    pass
