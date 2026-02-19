import socket


class PicoClient:
    
    @classmethod
    def set_bool_state(cls, bool_state):
        cls.bool_state = bool_state
        print(f'Bool State: {bool_state}')
        

    def __init__(self):
        self.set_bool_state(bool_state=False)
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('0.0.0.0', 8080))
        
        #  keeps loop running even when no packets arrive
        self.s.settimeout(0.1)  # if nothing arrives at recvfrom() within 0.1 seconds, raise a socket.timeout exception and continue
        

    def get_data(self):
        #  MicroPython uses OSError for timeouts instead of socket.timeout
        try:
            data, addr = self.s.recvfrom(1024)  # this line waits indefinitely until data is received from the webhook endpoint
            self.set_bool_state(bool(data))
            print(f'RECEIVED: {bool(data)} from {addr}')
        
        except OSError:
            pass        


if __name__=="__main__":
    pico_client_class = PicoClient()
    
    while True:
        print(pico_client_class.bool_state)
        pico_client_class.get_data()
