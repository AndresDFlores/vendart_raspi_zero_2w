from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json
import threading

UDP_IP = "127.0.0.1"
UDP_PORT = 8080

# Track highest processed version per payment ID
processed_versions = {}
lock = threading.Lock()

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            body_dict = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            body_dict = {"raw": body.decode("utf-8", errors="replace")}

        payment = body_dict['data']['object']['payment']
        payment_id = payment['id']
        version = payment.get('version', 0)

        status = payment.get('status')  # completed when successful, canceled when failed
        receipt_id = payment.get('receipt_url')  # returns none when transaction failed


        # --- IDEMPOTENCY + FINAL VERSION FILTER ---
        with lock:
            last_version = processed_versions.get(payment_id, -1)

            # Ignore if this version is not newer
            if version <= last_version:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
                return

            # Update stored version
            processed_versions[payment_id] = version

        # --- ONLY TRIGGER ON FINAL COMPLETED VERSION ---
        if status == "COMPLETED":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"1", (UDP_IP, UDP_PORT))
            sock.close()

        # --- ACKNOWLEDGE WEBHOOK ---
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


def run():
    server = HTTPServer(("0.0.0.0", 9999), WebhookHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()