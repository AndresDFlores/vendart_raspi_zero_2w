from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data= request.json
    print(f"\n\nReceived:\n{data}")
    return jsonify({"status": "received"}), 200

def start_server():
    app.run(host="0.0.0.0", port=5000)
    

if __name__ == "__main__":
    start_server()

