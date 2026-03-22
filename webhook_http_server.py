from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json

from transaction_logs import *


#  https://developer.squareup.com/forums/t/webhook-payment-updated-triggers-2-responses/10871


class WebhookHandler(BaseHTTPRequestHandler):


    def do_POST(self):

        # Read the raw body
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length)


        # Respond to webhook sender
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


        # parse received JSON data package 
        body_dict = None
        try:
            body_dict = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            body_dict = {"raw": raw_body.decode("utf-8", errors="replace")}

        
        #  confirm that the webhook POST is unique
        transaction_logger_class = TransactionLogger("vendart_transactions_log.jsonl")
        transaction_logger_class.main(body_dict)


        #  if POST is unique, publish to UDP
        if transaction_logger_class.publish_to_udp:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"1", ("127.0.0.1", 8080))
            sock.close()


def run(stop_event):
    server = HTTPServer(("0.0.0.0", 9999), WebhookHandler)
    server.timeout = 0.5  # allows periodic checks of stop_event

    print("[webhook_http_server] Server started on port 9999")

    try:
        while not stop_event.is_set():
            server.handle_request()  # processes one request or times out
    finally:
        print("[webhook_http_server] Shutting down...")
        server.server_close()
        print("[webhook_http_server] Server stopped.")


if __name__ == "__main__":
    run()