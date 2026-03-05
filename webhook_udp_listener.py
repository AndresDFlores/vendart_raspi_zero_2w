import socket


class PiZeroClient:

    @classmethod
    def set_bool_state(cls, bool_state):
        cls.bool_state = bool_state
        print(f'Bool State: {bool_state}')


    def __init__(self):
        self.set_bool_state(False)

        # Create UDP socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to all interfaces on port 8080
        self.s.bind(("0.0.0.0", 8080))

        # CPython uses socket.timeout instead of OSError
        self.s.settimeout(0.1)


    def get_data(self):
        try:
            data, addr = self.s.recvfrom(1024)
            self.set_bool_state(bool(data))
            print(f"RECEIVED: {bool(data)} from {addr}")

        except socket.timeout:
            # No packet received within timeout
            pass


if __name__ == "__main__":
    client = PiZeroClient()

    while True:
        print(client.bool_state)
        client.get_data()