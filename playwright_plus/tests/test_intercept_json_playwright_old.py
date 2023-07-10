import unittest
from playwright_plus import intercept_json_playwright_old


def custom_json_detect_error_for_intercept_json_old(result):
    is_error = False
    return is_error, result


def custom_json_parse_result_for_intercept_json_old(result):
    return result["data"]


class TestInterceptJSONPlaywrightOld(unittest.TestCase):
    def test_intercept_json_playwright_old(self):
        json = intercept_json_playwright_old(
            "https://dummyjson.com/http/200",
            "dummyjson",
            json_detect_error=custom_json_detect_error_for_intercept_json_old,
        )
        self.assertTrue(type(json) is dict)
        self.assertEqual(json["error"], None)
        self.assertEqual(json["error_message"], None)
        self.assertEqual(json["data"]["status"], "200")
        self.assertEqual(json["data"]["message"], "OK")

    def test_intercept_json_playwright_old_with_wrong_sub_part(self):
        json = intercept_json_playwright_old(
            "https://dummyjson.com/http/200",
            "wrong_sub_part",
            json_detect_error=custom_json_detect_error_for_intercept_json_old,
        )
        self.assertTrue(type(json) is dict)
        self.assertEqual(json["error"], "PlaywrightInterceptError")
        self.assertEqual(
            json["error_message"],
            "An empty json was collected after calling the hidden API.",
        )
        self.assertEqual(json["data"], {})

    def test_intercept_json_playwright_old_with_response_json_error(self):
        json = intercept_json_playwright_old(
            "https://www.python.org/",
            "python",
            json_detect_error=custom_json_detect_error_for_intercept_json_old,
        )
        self.assertEqual(json["data"]["error"], "PlaywrightInterceptError")
        self.assertTrue(
            "exception when trying to intercept" in json["data"]["error_message"]
        )
        self.assertEqual(json["data"]["data"], {})

    def test_intercept_json_playwright_old_with_wrong_url_error(self):
        json = intercept_json_playwright_old("wrong_url", "wrong")
        self.assertEqual(json["error"], "PlaywrightGotoError")
        self.assertTrue(json["error_message"] is not None)
        self.assertEqual(json["data"], {})

    def test_intercept_json_playwright_old_with_callable_json_parse_result(self):
        result = intercept_json_playwright_old(
            "https://dummyjson.com/http/200",
            "dummyjson",
            json_detect_error=custom_json_detect_error_for_intercept_json_old,
            json_parse_result=custom_json_parse_result_for_intercept_json_old,
        )
        self.assertEqual(result["status"], "200")
        self.assertEqual(result["message"], "OK")


if __name__ == "__main__":
    unittest.main()
