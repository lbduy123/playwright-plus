import unittest
from pprint import pprint
from playwright_plus import (
    with_page,
    set_json_to_page,
    intercept_json_playwright,
    intercept_json_playwright_old,
    intercept_json_playwright_multiple,
    request_json_playwright,
)


class CustomPage:
    def __init__(self, target_json):
        self.target_json = target_json


def custom_json_detect_error(result):
    is_error = False
    result = result["data"]
    return is_error, result


def custom_json_parse_result(result):
    return result["status"] + " " + result["message"]


def custom_json_detect_error_for_intercept_json_old(result):
    is_error = False
    return is_error, result


def custom_json_parse_result_for_intercept_json_old(result):
    return result["data"]


# class TestInterceptJsonPlaywrightMultiple(unittest.TestCase):
# def test_intercept_json_playwright_multiple(self):
#     json = intercept_json_playwright_multiple(
#         "https://dummyjson.com/http/200", "dummyjson"
#     )
#     self.assertTrue(type(json) is dict)
#     self.assertEqual(json["error"], None)
#     self.assertEqual(json["error_message"], None)
#     self.assertEqual(json["data"]["status"], "200")
#     self.assertEqual(json["data"]["message"], "OK")

# def test_intercept_json_playwright_multiple_with_wrong_sub_part(self):
#     json = intercept_json_playwright_multiple(
#         "https://dummyjson.com/http/200", "wrong_sub_part"
#     )
#     self.assertTrue(type(json) is dict)
#     self.assertEqual(json["error"], "PlaywrightInterceptError")
#     self.assertEqual(
#         json["error_message"],
#         "An empty json was collected after calling the hidden API.",
#     )
#     self.assertEqual(json["data"], {})

# def test_intercept_json_playwright_multiple_with_response_json_error(self):
#     json = intercept_json_playwright_multiple("https://www.python.org/", "python")
#     self.assertEqual(json["data"]["error"], "PlaywrightInterceptError")
#     self.assertTrue(
#         "exception when trying to intercept" in json["data"]["error_message"]
#     )
#     self.assertEqual(json["data"]["data"], {})

# def test_intercept_json_playwright_multiple_with_wrong_url_error(self):
#     json = intercept_json_playwright_multiple("wrong_url", "wrong")
#     self.assertEqual(json["error"], "PlaywrightGotoError")
#     self.assertTrue(json["error_message"] is not None)
#     self.assertEqual(json["data"], {})

# def test_intercept_json_playwright_multiple_with_callable_json_detect_error(self):
#     json = intercept_json_playwright_multiple(
#         "https://dummyjson.com/http/200",
#         "dummyjson",
#         json_detect_error=custom_json_detect_error,
#     )
#     self.assertEqual(json["status"], "200")
#     self.assertEqual(json["message"], "OK")

# def test_intercept_json_playwright_multiple_with_callable_json_parse_result(self):
# result = intercept_json_playwright_multiple(
#     "https://dummyjson.com/http/200",
#     "dummyjson",
#     json_detect_error=custom_json_detect_error,
#     json_parse_result=custom_json_parse_result,
# )
# self.assertEqual(result, "200 OK")


# class TestRequestJsonPlaywright(unittest.TestCase):
# def test_request_json_playwright(self):
#     json = request_json_playwright("https://dummyjson.com/http/200")
#     self.assertTrue(type(json) is dict)
#     self.assertEqual(json["error"], None)
#     self.assertEqual(json["error_message"], None)
#     self.assertEqual(json["data"]["status"], "200")
#     self.assertEqual(json["data"]["message"], "OK")


# class TestInterceptJsonPlaywright(unittest.TestCase):
#     def test_intercept_json_playwright(self):
#         json = intercept_json_playwright("https://dummyjson.com/http/200", "dummyjson")
#         self.assertTrue(type(json) is dict)
#         self.assertEqual(json["error"], None)
#         self.assertEqual(json["error_message"], None)
#         self.assertEqual(json["data"]["status"], "200")
#         self.assertEqual(json["data"]["message"], "OK")

#     def test_intercept_json_playwright_with_wrong_sub_part(self):
#         json = intercept_json_playwright(
#             "https://dummyjson.com/http/200", "wrong_sub_part"
#         )
#         self.assertTrue(type(json) is dict)
#         self.assertEqual(json["error"], "PlaywrightInterceptError")
#         self.assertEqual(
#             json["error_message"],
#             "An empty json was collected after calling the hidden API.",
#         )
#         self.assertEqual(json["data"], {})

#     def test_intercept_json_playwright_with_response_json_error(self):
#         json = intercept_json_playwright("https://www.python.org/", "python")
#         self.assertEqual(json["data"]["error"], "PlaywrightInterceptError")
#         self.assertTrue(
#             "exception when trying to intercept" in json["data"]["error_message"]
#         )
#         self.assertEqual(json["data"]["data"], {})

#     def test_intercept_json_playwright_with_wrong_url_error(self):
#         json = intercept_json_playwright("wrong_url", "wrong")
#         self.assertEqual(json["error"], "PlaywrightInterceptError")
#         self.assertEqual(
#             json["error_message"],
#             "An empty json was collected after calling the hidden API.",
#         )
#         self.assertEqual(json["data"], {})

#     def test_intercept_json_playwright_with_callable_json_detect_error(self):
#         json = intercept_json_playwright(
#             "https://dummyjson.com/http/200",
#             "dummyjson",
#             json_detect_error=custom_json_detect_error,
#         )
#         self.assertEqual(json["status"], "200")
#         self.assertEqual(json["message"], "OK")

#     def test_intercept_json_playwright_with_callable_json_parse_result(self):
#         result = intercept_json_playwright(
#             "https://dummyjson.com/http/200",
#             "dummyjson",
#             json_detect_error=custom_json_detect_error,
#             json_parse_result=custom_json_parse_result,
#         )
#         self.assertEqual(result, "200 OK")


# class TestInterceptJSONPlaywrightOld(unittest.TestCase):
#     def test_intercept_json_playwright_old(self):
#         json = intercept_json_playwright_old(
#             "https://dummyjson.com/http/200",
#             "dummyjson",
#             json_detect_error=custom_json_detect_error_for_intercept_json_old,
#         )
#         self.assertTrue(type(json) is dict)
#         self.assertEqual(json["error"], None)
#         self.assertEqual(json["error_message"], None)
#         self.assertEqual(json["data"]["status"], "200")
#         self.assertEqual(json["data"]["message"], "OK")

#     def test_intercept_json_playwright_old_with_wrong_sub_part(self):
#         json = intercept_json_playwright_old(
#             "https://dummyjson.com/http/200",
#             "wrong_sub_part",
#             json_detect_error=custom_json_detect_error_for_intercept_json_old,
#         )
#         self.assertTrue(type(json) is dict)
#         self.assertEqual(json["error"], "PlaywrightInterceptError")
#         self.assertEqual(
#             json["error_message"],
#             "An empty json was collected after calling the hidden API.",
#         )
#         self.assertEqual(json["data"], {})

#     def test_intercept_json_playwright_old_with_response_json_error(self):
#         json = intercept_json_playwright_old(
#             "https://www.python.org/",
#             "python",
#             json_detect_error=custom_json_detect_error_for_intercept_json_old,
#         )
#         self.assertEqual(json["data"]["error"], "PlaywrightInterceptError")
#         self.assertTrue(
#             "exception when trying to intercept" in json["data"]["error_message"]
#         )
#         self.assertEqual(json["data"]["data"], {})

#     def test_intercept_json_playwright_old_with_wrong_url_error(self):
#         json = intercept_json_playwright_old("wrong_url", "wrong")
#         self.assertEqual(json["error"], "PlaywrightGotoError")
#         self.assertTrue(json["error_message"] is not None)
#         self.assertEqual(json["data"], {})

#     def test_intercept_json_playwright_old_with_callable_json_parse_result(self):
#         result = intercept_json_playwright_old(
#             "https://dummyjson.com/http/200",
#             "dummyjson",
#             json_detect_error=custom_json_detect_error_for_intercept_json_old,
#             json_parse_result=custom_json_parse_result_for_intercept_json_old,
#         )
#         self.assertEqual(result["status"], "200")
#         self.assertEqual(result["message"], "OK")


# class TestSetJsonToPage(unittest.TestCase):
#     def test_set_json_to_page(self):
#         page = CustomPage({})
#         set_json_to_page(
#             page,
#             {
#                 "error": None,
#                 "error_message": None,
#                 "data": {},
#             },
#         )
#         result = vars(page)
#         self.assertEqual(result["target_json"]["error"], None)
#         self.assertEqual(result["target_json"]["error_message"], None)
#         self.assertEqual(result["target_json"]["data"], {})

#     def test_set_json_to_page_with_error(self):
#         page = CustomPage({})
#         set_json_to_page(
#             page,
#             {
#                 "error": "JsonError",
#                 "error_message": "Something wrong",
#                 "data": {},
#             },
#         )
#         result = vars(page)
#         self.assertEqual(result["target_json"]["error"], "PlaywrightInterceptError")
#         self.assertEqual(result["target_json"]["error_message"], "JsonError")
#         self.assertEqual(result["target_json"]["data"], {})


if __name__ == "__main__":
    unittest.main()
