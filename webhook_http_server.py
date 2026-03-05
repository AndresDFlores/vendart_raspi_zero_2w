from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 8080

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        print("\n=== Incoming Webhook ===")
        print("Headers:", dict(self.headers))
        print("Body:", body.decode())
        print("========================\n")

        # Forward a UDP packet to your listener
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"1", (UDP_IP, UDP_PORT))
        sock.close()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run():
    server = HTTPServer(("0.0.0.0", 9999), WebhookHandler)
    print("Webhook server running on port 9999")
    server.serve_forever()

if __name__ == "__main__":
    run()