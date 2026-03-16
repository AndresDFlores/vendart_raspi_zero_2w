import threading

import webhook_http_server
import webhook_secure_tunnel


class DPPClass:

    #  define local server (webhook endpoint) thread
    def start_server(self):
        self.server_thread = threading.Thread(target=webhook_http_server.run, args=())

    #  define secure tunnel thread
    def start_secure_tunnel(self):
        self.tunnel_thread = threading.Thread(target=webhook_secure_tunnel.run_secure_tunnel, args=())


    def main(self):
        
        #  define threads
        self.start_server()
        self.start_secure_tunnel()

        #  execute thread
        self.server_thread.start()
        self.tunnel_thread.start()

        #  code stops here until the threads finish running
        self.server_thread.join()
        self.tunnel_thread.join()



if __name__=="__main__":
    dpp_class=DPPClass()
    dpp_class.main()