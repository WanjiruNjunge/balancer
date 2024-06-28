import time
from flask import Flask, jsonify, request, Response, g
from hashing import ConsistentHashing, Server
import random
import uuid
import requests
import logging
import subprocess
from threading import Thread, Lock

app = Flask(__name__)
consistentHashing =  ConsistentHashing()
PORT: int = 32000
SERVER_NAME = 'server'
lock = Lock()
REQUEST_DICT : dict[str, int] = {}


logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_hostnames(n = random.randint(1,6)):
  ids = [str(uuid.uuid4()).replace("-","") for _ in range(n)]
  return n, ids


def create_container(name):
  global PORT
  try:
    cmd = f'docker run -d --name {name} -p {PORT}:5000 -P {SERVER_NAME}'
    output = subprocess.check_output(cmd, shell=True, text=True).strip()  # Get container ID
    PORT += 1
    return output  # Return container ID for IP retrieval
  except subprocess.CalledProcessError as e:
    logging.error(f"Error creating Docker container: {e}")
    return None

def get_host_ip(container_id):
  try:
    cmd = f'docker inspect -f "{{{{.NetworkSettings.IPAddress}}}}" {container_id}'
    ip = subprocess.check_output(cmd, shell=True, text=True).strip()
    return ip
  except subprocess.CalledProcessError as e:
    logging.error(f"Error getting IP address for container {container_id}: {e}")
    return None
  


@app.route("/rep")
def rep():
  servers = consistentHashing.get_servers()
  return jsonify({
    "message": {
      "N" : consistentHashing.num_servers,
      "replicas": servers
    }
  }), 200

@app.route("/add", methods=['POST'])
def add():
  n, ids = generate_hostnames(1)
  server_id = ids[0]

  container_id = create_container(server_id)
  if container_id is None:
      return jsonify({"message": "Failed to create container"}), 500

  ip = get_host_ip(container_id)
  if ip is None:
      return jsonify({"message": "Failed to get container IP"}), 500

  server = Server(server_id, ip, PORT - 1)  
  logging.info(f"Server created: {server}")
  consistentHashing.add_server(server)
  return jsonify({
      "message": {
          "N": n,
          "replicas": server_id
      }
  }), 200
  
  
@app.route("/rm", methods=['DELETE'])
def rm():
  """Randomly remove a server

  Returns:
      Response: jsonified number of servers removed and response code
  """
  if request.method != 'DELETE':
    return jsonify({
      "message": "Invalid Request"
    }), 400
  
  servers = consistentHashing.get_servers()
  if len(servers) == 0:
    return jsonify({
      "message": "No servers to remove"
    }), 404
  
  removed_server = random.choice(servers)
  consistentHashing.remove_server(removed_server)

  logging.info(f"Removed server: {removed_server}")
  return jsonify({
    "message": {
      "N": 1,
      "removed_server": removed_server
    }
  }), 200

# @app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def assign(path):
  global REQUEST_DICT
  servers = consistentHashing.get_servers()
  server_id = random.choice(servers)
  server = consistentHashing.get_server(str(server_id))
  logging.info(f"chosen server is {server}")

  logging.info(server)
  if server is None:
    return Response(status=500)
  
  if not isinstance(server, Server):
    return "Wrong Server chosen", 500
      
  # Make a request to the selected server
  url = f"http://{server.ip}:5000/{path}"
  logging.info(url)
  print(url)
  try:
    response = requests.get(url, timeout=30)
    return Response(response.content, status=response.status_code)
  except requests.exceptions.RequestException as e:
    logging.error(f"Error making request to server: {e}")
    return Response(status=500)

if __name__ == "__main__":
  app.run("0.0.0.0", port=7432, debug=True, use_reloader=False)

