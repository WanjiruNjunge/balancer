import hashlib
from dataclasses import dataclass
import random
import uuid
import subprocess
import logging

logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass(repr=True)
class Server:
  name: str
  ip: str
  port: str

  def output(self):
    return f'id = {self.name} \n ip = {self.ip} \n port={self.port}'

class ConsistentHashing:
  def __init__(self, num_slots=512, num_virtual_nodes=9, num_servers=3):
    self.num_slots = num_slots
    self.num_virtual_nodes = num_virtual_nodes
    self.num_servers = 0
    self.servers : dict[str, Server] = {}
    self.hash_ring = {}
    # self.create_image('server')
    self.PORT = 54000


    for _ in range(num_servers):
      server_id = str(uuid.uuid4()).replace('-', '')
      container_id = self.create_container(server_id)
      if container_id is None:
          logging.error("Failed to create container")

      ip = self.get_host_ip(container_id)
      if ip is None:
          logging.error("Failed to get container IP")

      server = Server(server_id, ip, self.PORT - 1)  
      logging.info(f"Server created: {server}")
      self.add_server(server=server)
     
    
  def create_container(self,name):
    try:
      cmd = f'docker run -d --name {name} -p {self.PORT}:5000 server'
      output = subprocess.check_output(cmd, shell=True, text=True).strip()  # Get container ID
      self.PORT += 1
      return output  # Return container ID for IP retrieval
    except subprocess.CalledProcessError as e:
      logging.error(f"Error creating Docker container: {e}")
      return None

  def get_host_ip(self,container_id):
    try:
      cmd = f'docker inspect -f "{{{{.NetworkSettings.IPAddress}}}}" {container_id}'
      ip = subprocess.check_output(cmd, shell=True, text=True).strip()
      return ip
    except subprocess.CalledProcessError as e:
      logging.error(f"Error getting IP address for container {container_id}: {e}")
      return None

  def _hash(self, key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.num_slots

  def hash_name(self, server_id):
    for i in range(self.num_virtual_nodes):
      virtual_node = f"{server_id}#{i}"
      hash_val = self._hash(virtual_node)
      self.hash_ring[hash_val] = f'{server_id}'

  def add_server(self, server: Server):
    self.hash_name(server.name)
    self.servers[server.name] = server
    self.num_servers += 1

  def add_servers(self, n):
    for i in range(n):
      self.add_server(f"Server_{self.num_servers + 1}")
      self.num_servers += n

  def remove_server(self, server_id=None):
    if server_id is None:
      server_id = str(random.choice(list(self.servers.keys())))
    for i in range(self.num_virtual_nodes):
      virtual_node = f"{server_id}#{i}"
      hash_val = self._hash(virtual_node)
      if hash_val in self.hash_ring:
          del self.hash_ring[hash_val]
    del self.servers[server_id]

    subprocess.run(['docker', 'stop', server_id])
    subprocess.run(['docker', 'rm', '--force', server_id])
    self.num_servers -= 1


  def remove_servers(self, n):
    for i in range(n):
        self.remove_server(f"Server_{self.num_servers}")

  def get_server(self, key) -> Server:
    hash_val = self._hash(key)
    sorted_hashes = sorted(self.hash_ring.keys())
    for h in sorted_hashes:
        if hash_val <= h:
            server_id = self.hash_ring[h]  
            return self.servers.get(server_id)  # Retrieve the Server object from the dictionary
    server_id = self.hash_ring[sorted_hashes[0]]
    return self.servers.get(server_id)   

  def get_servers(self):
    return list(set(self.hash_ring.values()))



