from vendart import *
from pico_network import connect_wifi


connect_wifi()

vendart=VendArt()
vendart.main()

