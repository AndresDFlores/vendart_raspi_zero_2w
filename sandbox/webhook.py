import threading

import webhook_server
import secure_tunnel

t1 = threading.Thread(target=webhook_server.start_server, args=())
t2 = threading.Thread(target=secure_tunnel.open_secure_tunnel, args=())

t1.start()
t2.start()

t1.join()
t2.join()