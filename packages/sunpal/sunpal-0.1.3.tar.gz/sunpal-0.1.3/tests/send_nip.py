import sunpal
import unittest

api_key = "test_aa40511dd7fe42bfb807090de8a942e5"
site = "sunwise"
sunpal.configure(api_key, site)


class SendNipTestCase(unittest.TestCase):
    def test_send_new_nip(self):
        entry = sunpal.Customer.send_nip({"rfc": "EAEN6506051Y8"})
        self.assertTrue(entry.customer, True)


if __name__ == "__main__":
    unittest.main()
