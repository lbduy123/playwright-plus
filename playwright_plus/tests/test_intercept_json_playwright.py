import unittest
from playwright_plus import intercept_json_playwright


def custom_json_detect_error(result):
    is_error = False
    result = result["data"]
    return is_error, result


def custom_json_parse_result(result):
    return result["status"] + " " + result["message"]


class TestInterceptJsonPlaywright(unittest.TestCase):
    def test_intercept_json_playwright(self):
        json = intercept_json_playwright("https://dummyjson.com/http/200", "dummyjson")
        self.assertTrue(type(json) is dict)
        self.assertEqual(json["error"], None)
        self.assertEqual(json["error_message"], None)
        self.assertEqual(json["data"]["status"], "200")
        self.assertEqual(json["data"]["message"], "OK")

    def test_intercept_json_playwright_with_wrong_sub_part(self):
        json = intercept_json_playwright(
            "https://dummyjson.com/http/200", "wrong_sub_part"
        )
        self.assertTrue(type(json) is dict)
        self.assertEqual(json["error"], "PlaywrightInterceptError")
        self.assertEqual(
            json["error_message"],
            "An empty json was collected after calling the hidden API.",
        )
        self.assertEqual(json["data"], {})

    def test_intercept_json_playwright_with_response_json_error(self):
        json = intercept_json_playwright("https://www.python.org/", "python")
        self.assertEqual(json["data"]["error"], "PlaywrightInterceptError")
        self.assertTrue(
            "exception when trying to intercept" in json["data"]["error_message"]
        )
        self.assertEqual(json["data"]["data"], {})

    def test_intercept_json_playwright_with_wrong_url_error(self):
        json = intercept_json_playwright("wrong_url", "wrong")
        self.assertEqual(json["error"], "PlaywrightInterceptError")
        self.assertEqual(
            json["error_message"],
            "An empty json was collected after calling the hidden API.",
        )
        self.assertEqual(json["data"], {})

    def test_intercept_json_playwright_with_callable_json_detect_error(self):
        json = intercept_json_playwright(
            "https://dummyjson.com/http/200",
            "dummyjson",
            json_detect_error=custom_json_detect_error,
        )
        self.assertEqual(json["status"], "200")
        self.assertEqual(json["message"], "OK")

    def test_intercept_json_playwright_with_callable_json_parse_result(self):
        result = intercept_json_playwright(
            "https://dummyjson.com/http/200",
            "dummyjson",
            json_detect_error=custom_json_detect_error,
            json_parse_result=custom_json_parse_result,
        )
        self.assertEqual(result, "200 OK")


if __name__ == "__main__":
    unittest.main()
