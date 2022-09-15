from ppadb.client import Client as AdbClient

applay = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037
devices = applay.devices()
if len(devices) == 0:
    print('No devices')
    quit()
print(devices)
device = devices[0]

result = device.screencap()
print(result)
with open("screen.png", "wb") as fp:
    fp.write(result)