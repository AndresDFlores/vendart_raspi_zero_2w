import network
import time
from wifi_credentials import credentials


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(credentials['ssid'], credentials['password'])

    # Wait for connection
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        print('network connection failed')
    else:
        print('connected')
        print(wlan.ifconfig())
