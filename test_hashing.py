import unittest
from hashing import ConsistentHashing

class TestConsistentHashing(unittest.TestCase):
    def setUp(self):
        self.ch = ConsistentHashing()

    def test_add_server(self):
        self.ch.add_server("Server 4")
        self.assertIn("Server 4", self.ch.get_servers())

    def test_add_servers(self):
        self.ch.add_servers(2)
        self.assertIn("Server 4", self.ch.get_servers())
        self.assertIn("Server 5", self.ch.get_servers())

    def test_remove_server(self):
        self.ch.remove_server("Server 1")
        self.assertNotIn("Server 1", self.ch.get_servers())

    def test_remove_servers(self):
        self.ch.remove_servers(2)
        self.assertNotIn("Server 3", self.ch.get_servers())
        self.assertNotIn("Server 2", self.ch.get_servers())

    def test_get_server(self):
        server = self.ch.get_server("key1")
        self.assertIn(server, self.ch.get_servers())

    def test_get_servers(self):
        servers = self.ch.get_servers()
        self.assertIsInstance(servers, list)
        self.assertGreater(len(servers), 0)

if __name__ == '__main__':
    unittest.main()