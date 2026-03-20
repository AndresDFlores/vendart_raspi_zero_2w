import threading

import webhook_http_server
import webhook_secure_tunnel
from vendart import *


#  display nmessages
literal = False

#  define threads
webhook_secure_tunnel_thread = threading.Thread(target=webhook_secure_tunnel.run_secure_tunnel, args=())
webhook_http_server_thread = threading.Thread(target=webhook_http_server.run, args=())
vendart_thread = threading.Thread(target=VendArt(literal).main, args=())


#  execute threads
webhook_secure_tunnel_thread.start()
webhook_http_server_thread.start()
vendart_thread.start()


#  code stops here until the threads finish running
webhook_secure_tunnel_thread.join()
webhook_http_server_thread.join()
vendart_thread.join()