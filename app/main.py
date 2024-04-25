from flask import Flask, jsonify, request
from os import environ
import socket

app = Flask(__name__)

# server_id = environ.get("SERVER_ID")

#internal endpoints

@app.route("/api/home", methods=["GET"])
def home():
  """
  Returns a message with the server ID.
  """
  return jsonify({"message": f"Hello from Server: {socket.gethostbyname(socket.gethostname())}", "status": "successful"}), 200

@app.route("/api/heartbeat", methods=["GET"])
def heartbeat():
  """
  Sends a heartbeat response.
  """
  return jsonify({"keya": "value"}), 200

#external endpoints
@app.route('/', methods=["GET"])
def index():
  """
  Returns a message with the server ID.
  """
  return jsonify({"message": f"Hello from Server: {socket.gethostbyname()}", "status": "successful"}), 200

@app.route('/rep', methods=["GET"])
def rep():
  return jsonify({"message": "Hello from GET rep"})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=61616, debug=True)