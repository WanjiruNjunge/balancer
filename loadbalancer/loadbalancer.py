from flask import Flask, request, jsonify
import hashlib
import requests

app = Flask(__name__)

class ConsistentHashing:
    def __init__(self, num_slots=512, num_virtual_nodes=9, num_servers=3):
        self.num_slots = num_slots
        self.num_virtual_nodes = num_virtual_nodes
        self.num_servers = num_servers
        self.hash_ring = {}

        for i in range(num_servers):
            self.add_server(f"Server {i + 1}")

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.num_slots

    def add_server(self, server_id):
        for i in range(self.num_virtual_nodes):
            virtual_node = f"{server_id}#{i}"
            hash_val = self._hash(virtual_node)
            self.hash_ring[hash_val] = server_id

    def add_servers(self, n):
        for i in range(n):
            self.add_server(f"Server {self.num_servers + 1}")
            self.num_servers += 1

    def remove_server(self, server_id):
        for i in range(self.num_virtual_nodes):
            virtual_node = f"{server_id}#{i}"
            hash_val = self._hash(virtual_node)
            if hash_val in self.hash_ring:
                del self.hash_ring[hash_val]

    def remove_servers(self, n):
        for i in range(n):
            self.remove_server(f"Server {self.num_servers}")
            self.num_servers -= 1

    def get_server(self, key):
        hash_val = self._hash(key)
        sorted_hashes = sorted(self.hash_ring.keys())
        for h in sorted_hashes:
            if hash_val <= h:
                return self.hash_ring[h]
        return self.hash_ring[sorted_hashes[0]]

    def get_servers(self):
        return list(set(self.hash_ring.values()))

# Task 3
# Load Balancer

load_balancer = ConsistentHashing()
replicas = []

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    })

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.json
    n = data['n']
    hostnames = data['hostnames']
    for hostname in hostnames[:n]:
        load_balancer.add_server(hostname)
        replicas.append(hostname)
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    })

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.json
    n = data['n']
    hostnames = data['hostnames']
    for hostname in hostnames[:n]:
        load_balancer.remove_server(hostname)
        replicas.remove(hostname)
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    })

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    node = load_balancer.get_server(path)
    if node:
        response = requests.get(f'http://{node}/{path}')
        return response.content, response.status_code, response.headers.items()
    return 'No available replicas', 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)