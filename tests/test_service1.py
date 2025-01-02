import unittest
import requests
import time

BASE_URL = "http://localhost:8197"

class TestService1(unittest.TestCase):

    def test_get_state(self):
        response = requests.get(f"{BASE_URL}/state")
        self.assertEqual(response.status_code, 200)
        self.assertIn("state", response.json())

    def test_set_state(self):
        response = requests.put(f"{BASE_URL}/state", data="RUNNING")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["state"], "RUNNING")

    def test_invalid_state(self):
        response = requests.put(f"{BASE_URL}/state", data="INVALID")
        self.assertEqual(response.status_code, 400)

    def test_request_when_not_running(self):
        requests.put(f"{BASE_URL}/state", data="PAUSED")
        response = requests.get(f"{BASE_URL}/request")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.text, "System not in RUNNING state")

    def test_request_when_running(self):
        requests.put(f"{BASE_URL}/state", data="RUNNING")
        response = requests.get(f"{BASE_URL}/request")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Request processed successfully")

    def test_get_run_log(self):
        requests.put(f"{BASE_URL}/state", data="RUNNING")
        requests.put(f"{BASE_URL}/state", data="PAUSED")
        response = requests.get(f"{BASE_URL}/run-log")
        self.assertEqual(response.status_code, 200)
        logs = response.json()["state_log"]
        self.assertGreater(len(logs), 0)
        self.assertTrue(any("RUNNING -> PAUSED" in log for log in logs))

    def test_monitor(self):
        # Set the state to RUNNING first
        requests.put(f"{BASE_URL}/state", data="RUNNING")
        
        # Make some requests to increment request count
        for _ in range(3):
            requests.get(f"{BASE_URL}/state")
        
        response = requests.get(f"{BASE_URL}/monitor")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("uptime", data)
        self.assertIn("total_requests", data)
        self.assertIn("current_state", data)
        self.assertEqual(data["current_state"], "RUNNING")


if __name__ == "__main__":
    unittest.main()
