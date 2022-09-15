from http import client
import time
import socket
# pure-python-adb loading
# pip install -U pure-python-adb
from ppadb.client import Client as AdbClient
# pip install psutil
import psutil

applay = None
device = None

def connect():
    global applay
    global device
    applay = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037
    devices = applay.devices()
    

    if len(devices) == 0:
        print('No devices')
        quit()
    print(devices)
    device = devices[0]
    print(f'Connected to {device}')
    return device, applay


connect()

res = device.screencap()
with open("screen.png","wb") as fp:
    fp.write(res)


for proc in psutil.process_iter():
    processName=proc.name()
    processID=proc.pid
    
    print(processName)
    print(processID)