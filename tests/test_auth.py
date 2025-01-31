import unittest
import requests

BASE_URL = "http://localhost:8098"

class TestSecurity(unittest.TestCase):

    def test_auth_protection(self):
        headers = {"X-API-KEY": "wrong_key"}
        response = requests.put(f"{BASE_URL}/state", data="RUNNING", headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_valid_auth(self):
        headers = {"X-API-KEY": "my_secure_key"}
        response = requests.put(f"{BASE_URL}/state", data="RUNNING", headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
