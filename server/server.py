from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route("/hello")
def index():
  return jsonify({
    "Hello world": f"Hello from server {socket.gethostbyname(socket.gethostname())}"
  })

@app.route("/home")
def home():
  i = 0
  return jsonify({
    "message": f"Hello from {socket.gethostbyname(socket.gethostname())}",
    "status": "successful"
  }), 200

@app.route("/heartbeat")
def heartbeat():
  return jsonify({
    "message": f"Heart beating ~^~",
    "status": "successful"
  }), 200


if __name__ == "__main__":
  app.run("0.0.0.0", port=5000, debug=True)

  