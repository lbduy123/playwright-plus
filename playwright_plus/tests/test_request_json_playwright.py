import unittest
from playwright_plus import request_json_playwright


class TestRequestJsonPlaywright(unittest.TestCase):
    def test_request_json_playwright(self):
        json = request_json_playwright("https://dummyjson.com/http/200")
        self.assertTrue(type(json) is dict)
        self.assertEqual(json["error"], None)
        self.assertEqual(json["error_message"], None)
        self.assertEqual(json["data"]["status"], "200")
        self.assertEqual(json["data"]["message"], "OK")


if __name__ == "__main__":
    unittest.main()
