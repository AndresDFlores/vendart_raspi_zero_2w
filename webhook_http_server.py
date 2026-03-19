from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 8080

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return


    def do_POST(self):
        
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)


        # parse JSON
        body_dict = None
        try:
            body_dict = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            body_dict = {"raw": body.decode("utf-8", errors="replace")}


        payment = body_dict['data']['object']['payment']
        status = payment.get('status')  # completed when successful, canceled when failed
        receipt_id = payment.get('receipt_url')  # returns none when transaction failed


        # Forward a UDP packet to your listener if payment is successfully received
        if status == "COMPLETED":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"1", (UDP_IP, UDP_PORT))
            sock.close()


        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


def run():
    server = HTTPServer(("0.0.0.0", 9999), WebhookHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()