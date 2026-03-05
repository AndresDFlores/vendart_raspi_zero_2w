import threading

from webhook import *
from vendart import *


#  define threads
webhook_thread = threading.Thread(target=DPPClass().main, args=())
vendart_thread = threading.Thread(target=VendArt().main, args=())


#  execute threads
webhook_thread.start()
vendart_thread.start()


#  code stops here until the threads finish running
webhook_thread.join()
vendart_thread.join()

