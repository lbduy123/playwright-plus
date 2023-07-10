import unittest
from playwright_plus import set_json_to_page


class CustomPage:
    def __init__(self, target_json):
        self.target_json = target_json


class TestSetJsonToPage(unittest.TestCase):
    def test_set_json_to_page(self):
        page = CustomPage({})
        set_json_to_page(
            page,
            {
                "error": None,
                "error_message": None,
                "data": {},
            },
        )
        result = vars(page)
        self.assertEqual(result["target_json"]["error"], None)
        self.assertEqual(result["target_json"]["error_message"], None)
        self.assertEqual(result["target_json"]["data"], {})

    def test_set_json_to_page_with_error(self):
        page = CustomPage({})
        set_json_to_page(
            page,
            {
                "error": "JsonError",
                "error_message": "Something wrong",
                "data": {},
            },
        )
        result = vars(page)
        self.assertEqual(result["target_json"]["error"], "PlaywrightInterceptError")
        self.assertEqual(result["target_json"]["error_message"], "JsonError")
        self.assertEqual(result["target_json"]["data"], {})


if __name__ == "__main__":
    unittest.main()
