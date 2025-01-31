import unittest
import requests

SERVICE1_URL = "http://localhost:8098"

class TestIntegration(unittest.TestCase):

    def test_service2_info_from_service1(self):
        """
        Test if Service1 fetches data from Service2 correctly.
        Accepts both wrapped and unwrapped responses.
        """
        response = requests.get(f"{SERVICE1_URL}/info")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Allow both wrapped (`"Service2"`) and unwrapped responses
        if "Service2" in data:
            self.assertIn("ip_address", data["Service2"])
        else:
            self.assertIn("ip_address", data)  # Accept raw Service2 response

if __name__ == "__main__":
    unittest.main()
