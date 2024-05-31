import hashlib

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











































# import hashlib

# class ConsistentHashing:
#     def __init__(self, num_slots=512, num_virtual_servers=9):
#         self.num_slots = num_slots
#         self.num_virtual_servers = num_virtual_servers
#         self.hash_map = [None] * self.num_slots
#         self.servers = {}

#     def hash_request(self, i):
#         #hash fxn for request mapping.
#         return int(hashlib.md5(str(i).encode()).hexdigest(), 16) % self.num_slots

#     def hash_virtual_server(self, i, j):
#         #virtual server mapping."
#         hash_input = f"{i}-{j}"
#         return int(hashlib.md5(hash_input.encode()).hexdigest(), 16) % self.num_slots

#     def add_server(self, server_id):
#         #multiple virtual servers
#         if server_id in self.servers:
#             return
#         self.servers[server_id] = []
#         for j in range(self.num_virtual_servers):
#             slot = self.hash_virtual_server(server_id, j)
#             while self.hash_map[slot] is not None:
#                 slot = (slot + 1) % self.num_slots
#             self.hash_map[slot] = server_id
#             self.servers[server_id].append(slot)

#     def remove_server(self, server_id):
#         #Remove server + virtual servers
#         if server_id not in self.servers:
#             return
#         for slot in self.servers[server_id]:
#             self.hash_map[slot] = None
#         del self.servers[server_id]

#     def get_server(self, request_id):
#         #Get the server handling the given request.
#         slot = self.hash_request(request_id)
#         while self.hash_map[slot] is None:
#             slot = (slot + 1) % self.num_slots
#         return self.hash_map[slot]




#if all else fails code that kinda worked before?
# import hashlib

# class ConsistentHashMap:
#     def __init__(self, num_servers=3, num_slots=512, virtual_nodes=9):
#         self.num_servers = num_servers
#         self.num_slots = num_slots
#         self.virtual_nodes = virtual_nodes
#         self.ring = [None] * num_slots
#         self.servers = {}
#         self.populate_ring()

#     def populate_ring(self):
#         for server_id in range(self.num_servers):
#             for vnode in range(self.virtual_nodes):
#                 vnode_id = f"{server_id}:{vnode}"
#                 vnode_hash = self.get_vnode_hash(server_id, vnode)
#                 self.add_node(vnode_hash, server_id)

#     def add_node(self, node_hash, server_id):
#         index = node_hash % self.num_slots
#         while self.ring[index] is not None:
#             index = (index + 1) % self.num_slots

#         self.ring[index] = server_id
#         self.servers.setdefault(server_id, []).append(node_hash)

#     def remove_node(self, node_hash, server_id):
#         index = node_hash % self.num_slots
#         while self.ring[index] != server_id:
#             index = (index + 1) % self.num_slots

#         self.ring[index] = None
#         self.servers[server_id].remove(node_hash)

#     def get_request_hash(self, request_id):
#         return (request_id ** 2 + 2 * request_id + 17) % self.num_slots

#     def get_vnode_hash(self, server_id, vnode):
#         return (server_id ** 2 + vnode ** 2 + 2 * vnode + 25) % self.num_slots

#     def get_server(self, request_id):
#         hash_key = self.get_request_hash(request_id)
#         index = hash_key

#         while self.ring[index] is None:
#             index = (index + 1) % self.num_slots

#         return self.ring[index]

#     def get_stats(self):
#         stats = {}
#         for server_id, nodes in self.servers.items():
#             stats[server_id] = len(nodes)
#         return stats


