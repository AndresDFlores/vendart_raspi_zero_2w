import threading
import logging

import webhook_http_server
import webhook_secure_tunnel
from vendart import *


#  display nmessages
literal = False


# Shared stop signal for all threads
stop_event = threading.Event()


# Wrap each target so they receive the stop_event
def secure_tunnel_wrapper():
    webhook_secure_tunnel.run_secure_tunnel(stop_event)

def http_server_wrapper():
    webhook_http_server.run(stop_event)

def vendart_wrapper():
    VendArt(literal).main(stop_event)


#  define threads
webhook_secure_tunnel_thread = threading.Thread(target=webhook_secure_tunnel.run_secure_tunnel, args=(stop_event,))
webhook_http_server_thread = threading.Thread(target=webhook_http_server.run, args=(stop_event,))
vendart_thread = threading.Thread(target=VendArt(literal).main, args=(stop_event,))


#  execute threads
webhook_secure_tunnel_thread.start()
webhook_http_server_thread.start()
vendart_thread.start()


try:
    # Wait for threads to finish
    webhook_secure_tunnel_thread.join()
    webhook_http_server_thread.join()
    vendart_thread.join()

except KeyboardInterrupt:
    print("\nKeyboard interrupt received — stopping all threads...")
    stop_event.set()

    # Wait for clean shutdown
    webhook_secure_tunnel_thread.join()
    webhook_http_server_thread.join()
    vendart_thread.join()

print("All threads stopped cleanly.")
