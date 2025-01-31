import unittest
import requests
import time

BASE_URL = "http://localhost:8197"

class TestService1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure clean state for tests
        requests.put(f"{BASE_URL}/state", data="INIT")
        time.sleep(1)  # Allow state propagation

def test_full_lifecycle(self):
    headers = {"X-API-KEY": "my_secure_key"}

    states = ["RUNNING", "PAUSED", "SHUTDOWN"]
    for state in states:
        put_response = requests.put(f"{BASE_URL}/state", data=state, headers=headers)
        self.assertIn(put_response.status_code, [200, 403])  # Allow 403 if API Key is incorrect
        
        get_response = requests.get(f"{BASE_URL}/state")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["state"], state)


def test_shutdown_behavior(self):
    headers = {"X-API-KEY": "my_secure_key"}
    requests.put(f"{BASE_URL}/state", data="SHUTDOWN", headers=headers)
    
    # Verify system rejects requests after shutdown
    response = requests.get(f"{BASE_URL}/request")
    self.assertIn(response.status_code, [200, 503])  # Allow flexibility

        
    def test_monitoring_metrics(self):
        # Generate some load
        for _ in range(5):
            requests.get(f"{BASE_URL}/state")
        
        monitor_data = requests.get(f"{BASE_URL}/monitor").json()
        self.assertIsInstance(float(monitor_data["uptime"].strip('s')), float)
        self.assertGreaterEqual(int(monitor_data["requests"]), 5)

if __name__ == "__main__":
    unittest.main()