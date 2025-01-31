import unittest
import requests

SERVICE1_URL = "http://localhost:8197"
SERVICE2_URL = "http://localhost:8199"

class TestIntegration(unittest.TestCase):

    def test_service2_info_from_service1(self):
        response = requests.get(f"{SERVICE1_URL}/info")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Service2", response.json())
        self.assertIn("ip_address", response.json()["Service2"])


    def test_system_monitor_interaction(self):
        # Interact with both services and validate `/monitor` data
        requests.get(f"{SERVICE1_URL}/state")  # Trigger a request to increment count
        monitor_data = requests.get(f"{SERVICE1_URL}/monitor").json()
        self.assertGreater(int(monitor_data["total_requests"]), 0)
        self.assertIn("uptime", monitor_data)

if __name__ == "__main__":
    unittest.main()
